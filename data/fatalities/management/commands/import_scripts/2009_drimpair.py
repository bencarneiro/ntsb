from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, driver_impaired_converter
from fatalities.models import DriverImpaired, Vehicle



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverImpaired.objects.filter(vehicle__accident__year=2009).delete()
        csv = pd.read_csv(f"{CSV_PATH}2009/FARS2009NationalCSV/VEHICLE.CSV", encoding='latin-1')
        for x in csv.index:
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            vehicle = Vehicle.objects.get(accident__year=2009, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            for factor in ["DR_CF1", "DR_CF2", "DR_CF3", "DR_CF4"]:

                number_saved = len(DriverImpaired.objects.filter(vehicle=vehicle))
                new_impairment_id = str(number_saved + 1)
                while len(new_impairment_id) < 3:
                    new_impairment_id = "0" + new_impairment_id
                primary_key = f"2009{st_case}{veh_no}{new_impairment_id}"

                impairment = driver_impaired_converter(csv[factor][x], 2009)
                if impairment:
                    data_to_save = {"vehicle": vehicle, "id": primary_key, "driver_impaired": impairment}
                    print(data_to_save)
                    DriverImpaired.objects.create(**data_to_save)

                    