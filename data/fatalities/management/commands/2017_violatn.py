from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, violation_converter
from fatalities.models import Violation, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Violation.objects.filter(vehicle__accident__year=2017).delete()
        csv = pd.read_csv(f"{CSV_PATH}2017/Violatn.CSV", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__year=2017, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            number_saved = len(Violation.objects.filter(vehicle=vehicle))
            new_violation_id = str(number_saved + 1)
            while len(new_violation_id) < 3:
                new_violation_id = "0" + new_violation_id
            primary_key = f"2017{st_case}{veh_no}{new_violation_id}"

            data_to_save = {"vehicle": vehicle, "id": primary_key}
            data_source = get_data_source("violation.moving_violation", 2017)
            csv_field_name = data_source.split(".")[1]
            data_to_save['moving_violation'] = violation_converter(csv[csv_field_name][x], 2017)
            print(data_to_save)
            Violation.objects.create(**data_to_save)