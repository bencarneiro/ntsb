from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import NonmotoristImpaired, Person
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        NonmotoristImpaired.objects.filter(person__accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/FARS2022NationalCSV/nmimpair.csv", encoding='latin-1')
        for x in csv.index:
            person = Person.objects.get(accident__year=2022, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            per_no = str(csv['ST_CASE'][x])
            while len(per_no) < 3:
                per_no = "0" + per_no
            number_saved = len(NonmotoristImpaired.objects.filter(person=person))
            new_impairment_id = str(number_saved + 1)
            while len(new_impairment_id) < 3:
                new_impairment_id = "0" + new_impairment_id
            primary_key = f"2022{st_case}{veh_no}{per_no}{new_impairment_id}"
            
            data_to_save = {"id": primary_key, "person": person}
            data_to_save['nonmotorist_impaired'] = csv['NMIMPAIR'][x]
            print(data_to_save)
            NonmotoristImpaired.objects.create(**data_to_save)
