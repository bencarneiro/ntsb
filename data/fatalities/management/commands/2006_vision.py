from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, visibility_converter
from fatalities.models import Vision, Vehicle



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Vision.objects.filter(vehicle__accident__year=2006).delete()
        csv = pd.read_csv(f"{CSV_PATH}2006/FARS2006NationalCSV/VEHICLE.CSV", encoding='latin-1')
        for x in csv.index:
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            vehicle = Vehicle.objects.get(accident__year=2006, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            for code in ["DR_CF1", "DR_CF2", "DR_CF3", "DR_CF4"]:
                number_saved = len(Vision.objects.filter(vehicle=vehicle))
                new_factor_id = str(number_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"2006{st_case}{veh_no}{new_factor_id}"
                maneuver = visibility_converter(csv[code][x], 2006)
                if maneuver:
                    data_to_save = {"vehicle": vehicle, "id": primary_key, "visibility": maneuver}
                    print(data_to_save)
                    Vision.objects.create(**data_to_save)

                    