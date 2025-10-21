#!/bin/sh
cd /root/ntsb/data
python3 manage.py track_podcast_downloads > /var/log/podcast_downloads.log
