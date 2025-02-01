from django.core.management.base import BaseCommand
from data.settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REFRESH_TOKEN
from fatalities.models import MultiReddit, Subreddit, RedditPost
import praw
from time import sleep

import logging

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # RedditPost.objects.all.delete()
        keywords = ["crash", "accident", "collision", "wreck", "dashcam", "hit-and-run", "car+hit", "truck+hit", "pedestrian", "bicycle", "bike", "cyclist", "scooter", "drunk+driver","drunk+driving"]
        # RedditPost.objects.all().delete()
        # Initialize the Reddit instance
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            refresh_token=REDDIT_REFRESH_TOKEN,
            user_agent='roadway.report/public-safety',
            ratelimit_seconds=600
        )

        multireddits = MultiReddit.objects.all()
        for search_query in keywords:
            print(f"Making requests for keyword: {search_query}")
            for multireddit in multireddits:
                mr = multireddit.slug
                print(mr)
                subreddit = reddit.subreddit(mr)
                sleep(.6)
                posts = subreddit.search(search_query, sort="new", limit=100)  # Adjust limit as needed
                for post in posts:
                    sub = Subreddit.objects.get(id=post.subreddit_name_prefixed.split("/")[1].lower())
                    try:
                        post = RedditPost.objects.get(subreddit=sub, slug=post.id)
                    except:
                        new_post = RedditPost(

                            slug = post.id,
                            subreddit = sub,
                            title = post.title,
                            # author = post.author,
                            score = post.score,
                            url = post.url,
                            created_utc = post.created_utc,
                            body = post.selftext
                        )
                        new_post.save()
                        print(post.permalink)


