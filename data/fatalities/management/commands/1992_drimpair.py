from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, driver_impaired_converter
from fatalities.models import DriverImpaired, Vehicle



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverImpaired.objects.filter(vehicle__accident__year=1992).delete()
        csv = pd.read_csv(f"{CSV_PATH}1992/VEHICLE.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_impairment_object)
                DriverImpaired.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            vehicle = Vehicle.objects.get(accident__year=1992, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            number_of_factors_saved = 0
            for factor in ["DR_CF1", "DR_CF2", "DR_CF3"]:

                # number_saved = len(DriverImpaired.objects.filter(vehicle=vehicle))
                new_impairment_id = str(number_of_factors_saved + 1)
                while len(new_impairment_id) < 3:
                    new_impairment_id = "0" + new_impairment_id
                primary_key = f"1992{st_case}{veh_no}{new_impairment_id}"

                impairment = driver_impaired_converter(csv[factor][x], 1992)
                if impairment:
                    number_of_factors_saved += 1
                    new_impairment_object = DriverImpaired(
                        id=primary_key,
                        vehicle=vehicle,
                        driver_impaired=impairment
                    )
                    bulk_data_upload += [new_impairment_object]
                    # data_to_save = {"vehicle": vehicle, "id": primary_key, "driver_impaired": impairment}
                    # print(data_to_save)
                    # DriverImpaired.objects.create(**data_to_save)

                    
        print(new_impairment_object)
        DriverImpaired.objects.bulk_create(bulk_data_upload)
        # bulk_data_upload = []
        print("WE HIT THE DB one last time")