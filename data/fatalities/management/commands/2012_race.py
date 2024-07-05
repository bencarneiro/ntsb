

from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import Race, Person
from django.db.models import Q

# before 2012, only one race recorded at person level

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Race.objects.filter(person__accident__year=2012).delete()
        csv = pd.read_csv(f"{CSV_PATH}2012/FARS2012NationalCSV/PERSON.CSV", encoding='latin-1')
        for x in csv.index:
            if csv['VEH_NO'][x] == 0:
                person = Person.objects.get(accident__year=2012, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            else:
                person = Person.objects.get(Q(accident__year=2012), Q(person_number=csv['PER_NO'][x]),  Q(accident__st_case=csv['ST_CASE'][x]), Q(vehicle__vehicle_number=csv['VEH_NO'][x])|Q(parked_vehicle__vehicle_number=csv['VEH_NO'][x]))
            
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            per_no = str(csv['PER_NO'][x])
            while len(per_no) < 3:
                per_no = "0" + per_no
            number_saved = len(Race.objects.filter(person=person))
            new_race_id = str(number_saved + 1)
            while len(new_race_id) < 3:
                new_race_id = "0" + new_race_id
            primary_key = f"2012{st_case}{veh_no}{per_no}{new_race_id}"
            
            data_to_save = {"id": primary_key, "person": person}

            data_to_save['race'] = csv['RACE'][x]
            data_to_save['is_multiple_races'] = 0
            data_to_save['order'] = 1
                
            print(data_to_save)
            Race.objects.create(**data_to_save)
