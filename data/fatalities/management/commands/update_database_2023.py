from django.core.management.base import BaseCommand
from fatalities.models import Accident
from data.settings import CSV_PATH

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # update accident.route_signing c11

        # crashes_with_unknown_route_signing = Accident.objects.filter(route_signing=9)
        # for c in crashes_with_unknown_route_signing:
        #     c.route_signing = 99
        # Accident.objects.bulk_update(crashes_with_unknown_route_signing, ['route_signing'])

        