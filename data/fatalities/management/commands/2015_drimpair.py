from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, driver_impaired_converter
from fatalities.models import DriverImpaired, Vehicle


# found elsewhere before 2010

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverImpaired.objects.filter(vehicle__accident__year=2015).delete()
        csv = pd.read_csv(f"{CSV_PATH}2015/FARS2015NationalCSV/DrImpair.csv", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__year=2015, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            number_saved = len(DriverImpaired.objects.filter(vehicle=vehicle))
            new_impairment_id = str(number_saved + 1)
            while len(new_impairment_id) < 3:
                new_impairment_id = "0" + new_impairment_id
            primary_key = f"2015{st_case}{veh_no}{new_impairment_id}"

            data_to_save = {"vehicle": vehicle, "id": primary_key}
            data_source = get_data_source("driver_impaired.driver_impaired", 2015)
            csv_field_name = data_source.split(".")[1]
            data_to_save['driver_impaired'] = driver_impaired_converter(csv[csv_field_name][x] ,2015)
            print(data_to_save)
            DriverImpaired.objects.create(**data_to_save)