

from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import Race, Person
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Race.objects.filter(person__accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/race.csv", encoding='latin-1')
        for x in csv.index:
            if csv['VEH_NO'][x] == 0:
                person = Person.objects.get(accident__year=2022, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            else:
                person = Person.objects.get(Q(accident__year=2022), Q(person_number=csv['PER_NO'][x]),  Q(accident__st_case=csv['ST_CASE'][x]), Q(vehicle__vehicle_number=csv['VEH_NO'][x])|Q(parked_vehicle__vehicle_number=csv['VEH_NO'][x]))
            data_to_save = {"person": person}
            data_to_save['race'] = csv['RACE'][x]
            data_to_save['is_multiple_races'] = csv['MULTRACE'][x]
            data_to_save['order'] = csv['ORDER'][x]
            print(data_to_save)
            Race.objects.create(**data_to_save)
