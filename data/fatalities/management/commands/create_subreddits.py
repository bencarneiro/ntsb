from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import Subreddit, MultiReddit, RedditPost

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):

        RedditPost.objects.all().delete()
        Subreddit.objects.all().delete()
        MultiReddit.objects.all().delete()
        scraped_reddits = pd.read_csv("https://gist.githubusercontent.com/bencarneiro/7dedcbf6698fd813661af99c5e36d5b7/raw/4b9a78fb8c1225e044f2a46b4e6c8b4a3ef2d1fb/gistfile1.txt")
        # start read subreddits
        # end read subreddits
        for x in scraped_reddits.index:
            new_sub = Subreddit(
                id=scraped_reddits["subreddit"][x].split("/r/")[1].lower()
            )
            new_sub.save()
        #start read multireddits
        multireddits = []
        current_multireddit = ""
        for x in scraped_reddits.index:
            print(scraped_reddits['subreddit'][x])
            reddit_name_string = scraped_reddits['subreddit'][x].split("/r/")[1].lower()
            current_multireddit += "+"
            current_multireddit += reddit_name_string
            if x % 100 == 99:
                multireddits += [current_multireddit[1:]]
                current_multireddit = ""
        multireddits += [current_multireddit[1:]]
        for mr in multireddits:
            new_multireddit = MultiReddit(slug=mr)
            new_multireddit.save()


        # end  read multireddits
