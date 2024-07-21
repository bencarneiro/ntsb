from django.core.management.base import BaseCommand
from fatalities.models import City


class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        nyc = City.objects.get(id=360814170)
        nyc.name = "NEW YORK"
        nyc.save()