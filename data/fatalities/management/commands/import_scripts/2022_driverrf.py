from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import DriverRelatedFactor, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverRelatedFactor.objects.filter(vehicle__accident__year=2022).delete()
        csv = pd.read_csv(f"{CSV_PATH}2022/FARS2022NationalCSV/driverrf.csv", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__year=2022, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            number_saved = len(DriverRelatedFactor.objects.filter(vehicle=vehicle))
            new_factor_id = str(number_saved + 1)
            while len(new_factor_id) < 3:
                new_factor_id = "0" + new_factor_id
            primary_key = f"2022{st_case}{veh_no}{new_factor_id}"
            data_to_save = {
                "id": primary_key,
                "vehicle": vehicle,
                "driver_related_factor": csv['DRIVERRF'][x]
            }
            print(data_to_save)
            DriverRelatedFactor.objects.create(**data_to_save)