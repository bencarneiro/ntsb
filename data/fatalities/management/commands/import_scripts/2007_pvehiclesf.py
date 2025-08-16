from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, parked_vehicle_related_factor_converter
from fatalities.models import ParkedVehicleRelatedFactor, Accident, ParkedVehicle

# multiple sources before 2007

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        ParkedVehicleRelatedFactor.objects.filter(parked_vehicle__accident__year=2007).delete()
        csv = pd.read_csv(f"{CSV_PATH}2007/FARS2007NationalCSV/VEHNIT.CSV", encoding='latin-1')
        for x in csv.index:
            parked_vehicle = ParkedVehicle.objects.get(accident__year=2007, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            for factor in ["VEH_CF1", "VEH_CF2"]:
                number_saved = len(ParkedVehicleRelatedFactor.objects.filter(parked_vehicle=parked_vehicle))
                new_factor_id = str(number_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"2007{st_case}{veh_no}{new_factor_id}"
                # data_source = get_data_source("parked_vehicle_related_factor.vehicle_related_factor", 2007)
                # csv_field_name = data_source.split(".")[1]
                factor_code = parked_vehicle_related_factor_converter(csv[factor][x], 2007)
                if factor_code:
                    data_to_save = {
                        "id": primary_key,
                        "parked_vehicle": parked_vehicle,
                        "parked_vehicle_related_factor": factor_code
                    }
                    print(data_to_save)
                    ParkedVehicleRelatedFactor.objects.create(**data_to_save)