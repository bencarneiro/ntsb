from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import ParkedVehicleRelatedFactor, Accident, ParkedVehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        ParkedVehicleRelatedFactor.objects.filter(parked_vehicle__accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/vehiclesf.csv", encoding='latin-1')
        for x in csv.index:
            accident = Accident.objects.get(year=2022, st_case=csv['ST_CASE'][x])
            parked_vehicle = ParkedVehicle.objects.get(accident__year=2022, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            data_to_save = {
                "accident": accident,
                "parked_vehicle": parked_vehicle,
                "vehicle_related_factor": csv['PVEHICLESF'][x]
            }
            print(data_to_save)
            ParkedVehicleRelatedFactor.objects.create(**data_to_save)