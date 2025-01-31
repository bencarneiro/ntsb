from django.core.management.base import BaseCommand
from data.settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
from fatalities.models import MultiReddit, Subreddit, RedditPost
import praw
from time import sleep

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # RedditPost.objects.all.delete()
        keywords = ["crash", "accident", "collision", "wreck", "dashcam", "hit-and-run", "pedestrian", "bicycle", "scooter"]
        # RedditPost.objects.all().delete()
        # Initialize the Reddit instance
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent='roadway.report/public-safety'
        )

        multireddits = MultiReddit.objects.all()
        for search_query in keywords:
            for multireddit in multireddits:
                mr = multireddit.slug
                print(mr)
                subreddit = reddit.subreddit(mr)
                sleep(1)
                posts = subreddit.search(search_query, sort="new", limit=500)  # Adjust limit as needed
                for post in posts:
                    print(f"{post.subreddit.display_name} - {post.title}")
                    sub = Subreddit.objects.get(id=post.subreddit.display_name.lower())
                    try:
                        post = RedditPost.objects.get(subreddit=sub, slug=post.id)
                    except:
                        new_post = RedditPost(

                            slug = post.id,
                            subreddit = sub,
                            title = post.title,
                            author = post.author,
                            score = post.score,
                            url = post.url,
                            created_utc = post.created_utc,
                            body = post.selftext
                        )
                        new_post.save()


