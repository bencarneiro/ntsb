from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import area_of_impact_converter
from fatalities.models import Damage, Vehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Damage.objects.filter(vehicle__accident__year=2009).delete()
        csv = pd.read_csv(f"{CSV_PATH}2009/FARS2009NationalCSV/VEHICLE.CSV", encoding='latin-1')
        for x in csv.index:
            vehicle = Vehicle.objects.get(accident__year=2009, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])


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
            primary_key = f"2009{st_case}{veh_no}{new_damage_id}"
            
            data_to_save = {"vehicle": vehicle, "id": primary_key}
            impact_1 = area_of_impact_converter(csv['IMPACT1'][x], 2009)
            impact_2 = area_of_impact_converter(csv['IMPACT2'][x], 2009)
            data_to_save['area_of_impact'] = impact_1
            Damage.objects.create(**data_to_save)
            print(data_to_save)
            if impact_1 != impact_2:
                data_to_save['area_of_impact'] = impact_2
                data_to_save['id'] = data_to_save['id'][:-1]
                data_to_save['id'] += "2"
                Damage.objects.create(**data_to_save)
                print(data_to_save)

            