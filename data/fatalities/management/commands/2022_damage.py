from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import Damage, ParkedVehicle, Vehicle, Accident

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Damage.objects.filter(vehicle__accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/damage.csv", encoding='latin-1')
        for x in csv.index:
            accident = Accident.objects.get(st_case=csv['ST_CASE'][x])
            vehicle = Vehicle.objects.get(accident=accident, vehicle_number=csv['VEH_NO'][x])
            data_to_save = {"vehicle": vehicle}
            data_to_save['area_of_impact'] = csv['DAMAGE'][x]
            print(data_to_save)
            Damage.objects.create(**data_to_save)