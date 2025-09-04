from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, violation_converter
from fatalities.models import Violation, Vehicle



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Violation.objects.filter(vehicle__accident__year=1994).delete()
        csv = pd.read_csv(f"{CSV_PATH}1994/VEHICLE.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_violation_object)
                Violation.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            vehicle = Vehicle.objects.get(accident__year=1994, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            primary_key = f"1994{st_case}{veh_no}001"
            violation_code = violation_converter(csv["VIOL_CHG"][x], 1994)
            if violation_code:
                new_violation_object = Violation(
                    id=primary_key,
                    vehicle=vehicle,
                    moving_violation=violation_code
                )
                bulk_data_upload += [new_violation_object]
                    # data_to_save = {"vehicle": vehicle, "id": primary_key, "moving_violation": violation_code}
                    # print(data_to_save)
                    # Violation.objects.create(**data_to_save)
        Violation.objects.bulk_create(bulk_data_upload)
        bulk_data_upload = []
        print("WE HIT THE DB one last time")

                    