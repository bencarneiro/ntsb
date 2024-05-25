

from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import NonmotoristDistracted, Person
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        NonmotoristDistracted.objects.filter(person__accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/nmdistract.csv", encoding='latin-1')
        for x in csv.index:
            person = Person.objects.get(accident__year=2022, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            data_to_save = {"person": person}
            data_to_save['nonmotorist_distracted_by'] = csv['NMDISTRACT'][x]
            print(data_to_save)
            NonmotoristDistracted.objects.create(**data_to_save)
