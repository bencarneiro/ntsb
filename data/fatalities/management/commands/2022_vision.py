from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import Vision, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Vision.objects.filter(vehicle__accident__year=2022).delete()
        csv = pd.read_csv(f"{CSV_PATH}2022/FARS2022NationalCSV/vision.csv", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__year=2022, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            number_saved = len(Vision.objects.filter(vehicle=vehicle))
            new_vision_id = str(number_saved + 1)
            while len(new_vision_id) < 3:
                new_vision_id = "0" + new_vision_id
            primary_key = f"2022{st_case}{veh_no}{new_vision_id}"

            data_to_save = {"vehicle": vehicle, "id": primary_key}
            data_to_save['visibility'] = csv['VISION'][x]
            print(data_to_save)
            Vision.objects.create(**data_to_save)