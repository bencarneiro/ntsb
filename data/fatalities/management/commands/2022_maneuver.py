from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import Maneuver, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Maneuver.objects.filter(vehicle__accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/maneuver.csv", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            data_to_save = {"vehicle": vehicle}
            data_to_save['driver_maneuvered_to_avoid'] = csv['MANEUVER'][x]
            print(data_to_save)
            Maneuver.objects.create(**data_to_save)