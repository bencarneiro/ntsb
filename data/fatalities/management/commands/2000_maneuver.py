from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, maneuver_converter
from fatalities.models import Maneuver, Vehicle



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Maneuver.objects.filter(vehicle__accident__year=2000).delete()
        csv = pd.read_csv(f"{CSV_PATH}2000/VEHICLE.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_maneuver_object)
                Maneuver.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            vehicle = Vehicle.objects.get(accident__year=2000, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            number_of_factors_saved = 0
            for code in ["DR_CF1", "DR_CF2", "DR_CF3", "DR_CF4"]:
                # number_saved = len(Maneuver.objects.filter(vehicle=vehicle))
                new_factor_id = str(number_of_factors_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"2000{st_case}{veh_no}{new_factor_id}"
                maneuver = maneuver_converter(csv[code][x], 2000)
                if maneuver:
                    number_of_factors_saved += 1
                    new_maneuver_object = Maneuver(
                        id=primary_key,
                        vehicle=vehicle,
                        driver_maneuvered_to_avoid=maneuver
                    )
                    bulk_data_upload += [new_maneuver_object]
        Maneuver.objects.bulk_create(bulk_data_upload)
        # bulk_data_upload = []
        print("WE HIT THE DB one last time")
                    # data_to_save = {"vehicle": vehicle, "id": primary_key, "driver_maneuvered_to_avoid": maneuver}
                    # print(data_to_save)
                    # Maneuver.objects.create(**data_to_save)

                    