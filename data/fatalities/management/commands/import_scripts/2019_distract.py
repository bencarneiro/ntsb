from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source
from fatalities.models import DriverDistracted, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        DriverDistracted.objects.filter(vehicle__accident__year=2019).delete()
        csv = pd.read_csv(f"{CSV_PATH}2019/FARS2019NationalCSV/Distract.CSV", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__year=2019, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            number_saved = len(DriverDistracted.objects.filter(vehicle=vehicle))
            new_distraction_id = str(number_saved + 1)
            while len(new_distraction_id) < 3:
                new_distraction_id = "0" + new_distraction_id
            primary_key = f"2019{st_case}{veh_no}{new_distraction_id}"

            data_to_save = {"vehicle": vehicle, "id": primary_key}

            data_source = get_data_source("driver_distracted.distracted_by", 2019)
            csv_field_name = data_source.split(".")[1]
            data_to_save['distracted_by'] = csv[csv_field_name][x]
            print(data_to_save)
            DriverDistracted.objects.create(**data_to_save)