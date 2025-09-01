from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, violation_converter
from fatalities.models import Violation, Vehicle



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Violation.objects.filter(vehicle__accident__year=1999).delete()
        csv = pd.read_csv(f"{CSV_PATH}1999/VEHICLE.CSV", encoding='latin-1')
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
            vehicle = Vehicle.objects.get(accident__year=1999, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            number_of_factors_saved = 0
            for code in ["VIOLCHG1", "VIOLCHG2", "VIOLCHG3"]:
                # number_saved = len(Violation.objects.filter(vehicle=vehicle))
                new_factor_id = str(number_of_factors_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"1999{st_case}{veh_no}{new_factor_id}"
                violation_code = violation_converter(csv[code][x], 1999)
                if violation_code:
                    number_of_factors_saved += 1
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

                    