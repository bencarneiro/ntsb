from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, vehicle_factor_converter
from fatalities.models import VehicleFactor, Vehicle



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        VehicleFactor.objects.filter(vehicle__accident__year=1991).delete()
        csv = pd.read_csv(f"{CSV_PATH}1991/VEHICLE.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_factor_object)
                VehicleFactor.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            vehicle = Vehicle.objects.get(accident__year=1991, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            number_of_factors_saved = 0
            for code in ["VEH_CF1", "VEH_CF2"]:
                # number_saved = len(VehicleFactor.objects.filter(vehicle=vehicle))
                new_factor_id = str(number_of_factors_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"1991{st_case}{veh_no}{new_factor_id}"
                factor = vehicle_factor_converter(csv[code][x], 1991)
                if factor:
                    number_of_factors_saved += 1
                    new_factor_object = VehicleFactor(
                        id=primary_key,
                        vehicle=vehicle,
                        contributing_cause=factor
                    )
                    bulk_data_upload += [new_factor_object]
                    # data_to_save = {"vehicle": vehicle, "id": primary_key, "contributing_cause": factor}
                    # print(data_to_save)
                    # VehicleFactor.objects.create(**data_to_save)

                    
        print(new_factor_object)
        VehicleFactor.objects.bulk_create(bulk_data_upload)
        print("WE HIT THE DB one last time.")