from django.core.management.base import BaseCommand
from fatalities.models import PodcastEpisode, PodcastDownload
from datetime import datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open("/var/log/nginx/access.log.1") as f:
            for x in f:
                if "/podcasts/" in x:
                    episode_slug = x.split("/podcasts/")[1].split(".mp3")[0]
                    time = x.split("[")[1].split("]")[0]
                    format_string = "%d/%b/%Y:%H:%M:%S %z"

                    # Convert the Nginx log timestamp string to a Python datetime object
                    python_datetime = datetime.strptime(time, format_string)

                    podcast_episode = PodcastEpisode.objects.get(slug=episode_slug)
                    try:
                        this_log_exists = PodcastDownload.objects.get(log=x)
                        print(f"That shit was found --- {x}")
                    except:
                        new_download = PodcastDownload(
                            episode = podcast_episode,
                            dt = python_datetime,
                            log = x
                        )
                        new_download.save()
                    print(episode_slug)
                    print(time)