from django.core.management.base import BaseCommand

from data.settings import MASTODON_FIRST_SECRET, MASTODON_LOGIN_PASSWORD, MASTODON_SECOND_SECRET
from mastodon import Mastodon
from datetime import *

api = Mastodon(MASTODON_FIRST_SECRET, MASTODON_SECOND_SECRET, api_base_url="https://its.bencarneiro.com")
api.log_in("shrek@bencarneiro.com", MASTODON_LOGIN_PASSWORD, scopes=["read", "write"])

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
    #     parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):

        # toot = f"{animal_type} alert! {name} is a {age_upon_intake} {sex_upon_intake} {color} {breed}. \nThey were found near {found_location} at {datetime}.\n\nIntake Type: {intake_type} \nIntake Condition: {intake_condition} \nID: {animal['animal_id']} \n\nThey are now at the Austin Animal Center - If unclaimed, the animal will be available for adoption in 3 days. \n\n#adopt #adoption #animals #cats #dogs #austin #austintx #animalshelter #shelter"

        today = date.today()
        future = date(2026,12,23)

        days_to_shrek_5 = (future - today).days
        api.toot(f"Only {days_to_shrek_5} more days until the release of Shrek 5! \n \n #shrek #shrek5 #dreamworks #dreamworkscinematicuniverse ")