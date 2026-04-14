from django.core.management.base import BaseCommand
from fatalities.models import State, County, Accident

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        for county in County.objects.filter(state_id=48):
            print(f"<p style='display:none'>{county.name} County accident, {county.name} County crash, Fatal car accident data, serious car accident report, car accident map</p>")
        cities = Accident.objects.filter(state_id=48).values('city__name').distinct()
        for city in cities:
            print(f"<p style='display:none'>{city['city__name']}, TX accident, {city['city__name']}, TX crash, Fatal car accident data, serious car accident report, car accident map</p>")
        print(len(cities))