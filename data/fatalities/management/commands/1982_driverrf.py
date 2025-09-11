from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import driver_related_factor_converter, get_data_source
from fatalities.models import DriverRelatedFactor, Vehicle

#multiple sources before 1982

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverRelatedFactor.objects.filter(vehicle__accident__year=1982).delete()
        csv = pd.read_csv(f"{CSV_PATH}1982/VEHICLE.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_factor_object)
                DriverRelatedFactor.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            vehicle = Vehicle.objects.get(accident__year=1982, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            number_of_factors_saved = 0
            for factor in ["DR_CF1", "DR_CF2", "DR_CF3"]:

                new_factor_id = str(number_of_factors_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"1982{st_case}{veh_no}{new_factor_id}"
                # data_source = get_data_source("driver_related_factor.driver_related_factor", 1982)
                # csv_field_name = data_source.split(".")[1]
                factor_code = driver_related_factor_converter(csv[factor][x], 1982)
                if factor_code:
                    new_factor_object = DriverRelatedFactor(
                        id=primary_key,
                        vehicle=vehicle,
                        driver_related_factor=factor_code
                    )
                    bulk_data_upload += [new_factor_object]
                    number_of_factors_saved += 1
        
        DriverRelatedFactor.objects.bulk_create(bulk_data_upload)
        print("we hit the database one last time")