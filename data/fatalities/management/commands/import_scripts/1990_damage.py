from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import area_of_impact_converter
from fatalities.models import Damage, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Damage.objects.filter(vehicle__accident__year=1990).delete()
        csv = pd.read_csv(f"{CSV_PATH}1990/VEHICLE.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_damage_object)
                Damage.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            vehicle = Vehicle.objects.get(accident__year=1990, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])


            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            number_saved = len(Damage.objects.filter(vehicle=vehicle))
            new_damage_id = str(number_saved + 1)
            while len(new_damage_id) < 3:
                new_damage_id = "0" + new_damage_id
            primary_key = f"1990{st_case}{veh_no}{new_damage_id}"
            
            impact_1 = area_of_impact_converter(csv['IMPACT1'][x], 1990)
            impact_2 = area_of_impact_converter(csv['IMPACT2'][x], 1990)
            new_damage_object = Damage(
                id=primary_key,
                vehicle=vehicle,
                area_of_impact=impact_1
            )
            bulk_data_upload += [new_damage_object]

            if impact_1 != impact_2:
                primary_key = primary_key[:-1] + "2"
                new_damage_object = Damage(
                    id=primary_key,
                    vehicle=vehicle,
                    area_of_impact=impact_2
                )
                bulk_data_upload += [new_damage_object]
        print(new_damage_object)
        Damage.objects.bulk_create(bulk_data_upload)
        # bulk_data_upload = []
        print("WE HIT THE DB one last time")