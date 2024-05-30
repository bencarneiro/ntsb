from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import Accident
from decimal import Decimal
from django.contrib.gis.geos import Point

def get_point(lat, lon):
    if lat in {Decimal('77.7777000'), Decimal('88.8888000'), Decimal('99.9999000')} or lon in {Decimal('77.7777000'), Decimal('88.8888000'), Decimal('99.9999000')}:
        return None
    else:
        return Point(float(lat), float(lon), srid=4326)

    
class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        for a in Accident.objects.all().order_by("st_case"):
            latitude = a.latitude
            longitude = a.longitude
            print(f"{latitude}, {longitude}")
            point = get_point(latitude, longitude)
            print(point)
            if point:
                a.location = point
                a.save()
            else: 
                print("LOCAtION UNKNOWN")