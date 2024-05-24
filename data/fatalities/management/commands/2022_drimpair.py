from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import DriverImpaired, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverImpaired.objects.filter(vehicle__accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/drimpair.csv", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            data_to_save = {"vehicle": vehicle}
            data_to_save['driver_impaired'] = csv['DRIMPAIR'][x]
            print(data_to_save)
            DriverImpaired.objects.create(**data_to_save)