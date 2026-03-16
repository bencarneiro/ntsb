"""This module implements connection pooling, which is needed because PostgreSQL
requires separate TCP connections for concurrent sessions.
"""

from collections import deque
from time import perf_counter as uptime
from weakref import WeakSet

import psycopg2
from psycopg2 import extensions as _ext


class PoolError(Exception):
    pass


class ConnectionPool:
    """A pool of :class:`psycopg2:connection` objects.

    .. attribute:: minconn

        The minimum number of connections to keep in the pool. By default one
        connection is opened when the pool is created.

    .. attribute:: maxconn

        The maximum number of connections in the pool. By default the pool will
        attempt to open as many connections as requested.

    .. attribute:: idle_timeout

        How many seconds to keep an idle connection before closing it. The
        default value causes idle connections to be closed after 10 minutes
        (approximately, it depends on :meth:`putconn` being called).

    .. attribute:: connect_kwargs

        The keyword arguments to pass to :func:`psycopg2.connect`. If the `dsn`
        argument isn't specified, then it's set to an empty string by default.

    The following attributes are internal, they're documented here to provide
    insight into how the pool works.

    .. attribute:: connections_in_use

        The set of connections that have been checked out of the pool through
        :meth:`getconn`. Type: :class:`weakref.WeakSet`.

    .. attribute:: idle_connections

        The pool of unused connections, last in first out.
        Type: :class:`collections.deque`.

    .. attribute:: return_times

        A timestamp is stored in this dict when a connection is added to
        :attr:`.idle_connections`. That timestamp is used in :meth:`getconn` to
        compute how long the connection stayed idle in the pool.
        Type: :class:`dict`.

    This class provides two main methods (:meth:`getconn` and :meth:`putconn`),
    plus another one that you probably don't need (:meth:`clear`).

    """

    __slots__ = (
        'minconn', 'maxconn', 'idle_timeout', 'connect_kwargs',
        'idle_connections', 'connections_in_use', 'return_times',
        '__dict__'
    )

    def __init__(self, minconn=1, maxconn=float('inf'), idle_timeout=600, **connect_kwargs):
        self.minconn = minconn
        self.maxconn = maxconn
        self.idle_timeout = idle_timeout
        connect_kwargs.setdefault('dsn', '')
        self.connect_kwargs = connect_kwargs

        self.connections_in_use = WeakSet()
        self.idle_connections = deque()
        self.return_times = {}

        for i in range(self.minconn):
            self._connect()

    def _connect(self, for_immediate_use=False):
        """Open a new connection.
        """
        conn = psycopg2.connect(**self.connect_kwargs)
        if for_immediate_use:
            self.connections_in_use.add(conn)
        else:
            self.return_times[conn] = uptime()
            self.idle_connections.append(conn)
        return conn

    def getconn(self):
        """Get a connection from the pool.

        If there is no idle connection available, then a new one is opened;
        unless there are already :attr:`.maxconn` connections open, then a
        :class:`PoolError` exception is raised.

        Any connection that is broken, or has been idle for more than
        :attr:`.idle_timeout` seconds, is closed and discarded.
        """
        while True:
            try:
                # Attempt to take an idle connection from the pool.
                conn = self.idle_connections.pop()
            except IndexError:
                # We don't have any idle connection available, open a new one.
                if len(self.connections_in_use) >= self.maxconn:
                    raise PoolError("connection pool exhausted")
                conn = self._connect(for_immediate_use=True)
            else:
                # Close and discard the connection if it's broken or too old.
                idle_since = self.return_times.pop(conn, 0)
                close = (
                    conn.info.transaction_status != _ext.TRANSACTION_STATUS_IDLE or
                    self.idle_timeout and idle_since < (uptime() - self.idle_timeout)
                )
                if close:
                    conn.close()
                    continue
            break
        return conn

    def putconn(self, conn):
        """Return a connection to the pool.

        You should always return a connection to the pool, even if you've closed
        it. That being said, the pool only holds weak references to connections
        returned by :meth:`getconn`, so they should be garbage collected even if
        you fail to return them.
        """
        self.connections_in_use.discard(conn)

        # Determine if the connection should be kept or discarded.
        current_time = uptime()
        if self.idle_timeout == 0 and len(self.idle_connections) >= self.minconn:
            conn.close()
        else:
            status = conn.info.transaction_status
            if status == _ext.TRANSACTION_STATUS_UNKNOWN:
                # The connection is broken, discard it.
                conn.close()
            else:
                if status != _ext.TRANSACTION_STATUS_IDLE:
                    # The connection is still in a transaction, roll it back.
                    conn.rollback()
                self.return_times[conn] = current_time
                self.idle_connections.append(conn)

        # Clean up the idle connections.
        if self.idle_timeout:
            # We cap the number of iterations to ensure that we don't end up in
            # an infinite loop.
            for i in range(len(self.idle_connections)):
                try:
                    conn = self.idle_connections[0]
                except IndexError:
                    break
                return_time = self.return_times.get(conn)
                if return_time is None:
                    # The connection's return time is missing, give up.
                    break
                if return_time < (current_time - self.idle_timeout):
                    # This connection has been idle too long, attempt to drop it.
                    try:
                        popped_conn = self.idle_connections.popleft()
                    except IndexError:
                        # Another thread removed this connection from the queue.
                        continue
                    if popped_conn == conn:
                        # Okay, we can close and discard this connection.
                        self.return_times.pop(conn, None)
                        conn.close()
                    else:
                        # We got a different connection, put it back.
                        self.idle_connections.appendleft(popped_conn)
                    continue
                else:
                    # The leftmost connection isn't too old, so we can assume
                    # that the other ones aren't either.
                    break

        # Open new connections if we've dropped below minconn.
        while (len(self.idle_connections) + len(self.connections_in_use)) < self.minconn:
            self._connect()

    def clear(self):
        """Close and discard all idle connections in the pool (regardless of the
        values of :attr:`.minconn` and :attr:`.idle_timeout`).

        This method could be useful if you have periods of high activity that
        result in many connections being opened, followed by prolonged periods
        with zero activity (no calls to :meth:`getconn` or :meth:`putconn`),
        *and* you care about closing those extraneous connections during the
        inactivity period. It's up to you to call this method in that case.

        Alternatively you may want to run a cron task to `close idle connections
        from the server <https://stackoverflow.com/a/30769511/>`_.
        """
        for conn in list(self.idle_connections):
            try:
                self.idle_connections.remove(conn)
            except ValueError:
                continue
            self.return_times.pop(conn, None)
            conn.close()


class ThreadSafeConnectionPool(ConnectionPool):
    """
    This subclass of :class:`ConnectionPool` uses a :class:`threading.RLock`
    object to ensure that its methods are thread safe.
    """

    __slots__ = ('lock',)

    def __init__(self, **kwargs):
        import threading
        super().__init__(**kwargs)
        self.lock = threading.RLock()

    def getconn(self):
        """See :meth:`ConnectionPool.getconn`."""
        with self.lock:
            return super().getconn()

    def putconn(self, conn):
        """See :meth:`ConnectionPool.putconn`."""
        with self.lock:
            return super().putconn(conn)

    def clear(self):
        """See :meth:`ConnectionPool.clear`."""
        with self.lock:
            return super().clear()
