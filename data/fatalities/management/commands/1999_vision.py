from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, visibility_converter
from fatalities.models import Vision, Vehicle



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Vision.objects.filter(vehicle__accident__year=1999).delete()
        csv = pd.read_csv(f"{CSV_PATH}1999/VEHICLE.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_vision_object)
                Vision.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            vehicle = Vehicle.objects.get(accident__year=1999, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])

            number_of_factors_saved = 0
            for code in ["DR_CF1", "DR_CF2", "DR_CF3", "DR_CF4"]:
                # number_saved = len(Vision.objects.filter(vehicle=vehicle))
                new_factor_id = str(number_of_factors_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"1999{st_case}{veh_no}{new_factor_id}"
                
                visibility_code = visibility_converter(csv[code][x], 1999)
                if visibility_code:
                    number_of_factors_saved += 1
                    new_vision_object = Vision(
                        id=primary_key,
                        vehicle=vehicle,
                        visibility=visibility_code
                    )
                    bulk_data_upload += [new_vision_object]
                    # data_to_save = {"vehicle": vehicle, "id": primary_key, "visibility": visibility_code}
                    # print(data_to_save)
                    # Vision.objects.create(**data_to_save)
          
        Vision.objects.bulk_create(bulk_data_upload)
        # bulk_data_upload = []
        print("WE HIT THE DB one last time")