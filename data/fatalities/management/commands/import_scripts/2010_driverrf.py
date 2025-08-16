from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import driver_related_factor_converter, get_data_source
from fatalities.models import DriverRelatedFactor, Vehicle

#multiple sources before 2010

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverRelatedFactor.objects.filter(vehicle__accident__year=2010).delete()
        csv = pd.read_csv(f"{CSV_PATH}2010/FARS2010NationalCSV/VEHICLE.CSV", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__year=2010, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            for factor in ["DR_SF1", "DR_SF2", "DR_SF3", "DR_SF4"]:
                number_saved = len(DriverRelatedFactor.objects.filter(vehicle=vehicle))
                new_factor_id = str(number_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"2010{st_case}{veh_no}{new_factor_id}"
                # data_source = get_data_source("driver_related_factor.driver_related_factor", 2010)
                # csv_field_name = data_source.split(".")[1]
                factor_code = driver_related_factor_converter(csv[factor][x], 2010)
                if factor_code:
                    data_to_save = {
                        "id": primary_key,
                        "vehicle": vehicle,
                        "driver_related_factor": factor_code
                    }
                    print(data_to_save)
                    DriverRelatedFactor.objects.create(**data_to_save)