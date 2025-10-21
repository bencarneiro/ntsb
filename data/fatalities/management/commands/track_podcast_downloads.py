from django.core.management.base import BaseCommand
from fatalities.models import PodcastEpisode, PodcastDownload


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open("/home/tonydeals/app/ntsb/access.log.1") as f:
            for x in f:
                if "/podcasts/" in x:
                    episode_slug = x.split("/podcasts/")[1].split(".mp3")[0]
                    time = x.split("[")[1].split("]")[0]
                    podcast_episode = PodcastEpisode.objects.get(slug=episode_slug)
                    print(episode_slug)
                    print(time)