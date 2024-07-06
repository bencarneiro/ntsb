from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, vehicle_factor_converter
from fatalities.models import VehicleFactor, Vehicle

#found at vehicle level before 2010

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        VehicleFactor.objects.filter(vehicle__accident__year=2010).delete()
        csv = pd.read_csv(f"{CSV_PATH}2010/FARS2010NationalCSV/FACTOR.CSV", encoding='latin-1')
        for x in csv.index:
            try:
                vehicle = Vehicle.objects.get(accident__year=2010, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            except Exception as e:
                print(f"Major fuckup --- this factor was linked to a parked car --- st_case: {csv['ST_CASE'][x]}")
                print(f"DISTRACTION VALUE IS {csv['MFACTOR'][x]}")
                print(e)
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            number_saved = len(VehicleFactor.objects.filter(vehicle=vehicle))
            new_factor_id = str(number_saved + 1)
            while len(new_factor_id) < 3:
                new_factor_id = "0" + new_factor_id
            primary_key = f"2010{st_case}{veh_no}{new_factor_id}"

            data_to_save = {"vehicle": vehicle, "id": primary_key}
            data_source = get_data_source("vehicle_factor.contributing_cause", 2010)
            csv_field_name = data_source.split(".")[1]
            data_to_save['contributing_cause'] = vehicle_factor_converter(csv[csv_field_name][x],2010)
            print(data_to_save)
            VehicleFactor.objects.create(**data_to_save)