from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import DriverRelatedFactor, Accident, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverRelatedFactor.objects.filter(vehicle__accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/driverrf.csv", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__year=2022, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            data_to_save = {
                "vehicle": vehicle,
                "driver_related_factor": csv['DRIVERRF'][x]
            }
            print(data_to_save)
            DriverRelatedFactor.objects.create(**data_to_save)