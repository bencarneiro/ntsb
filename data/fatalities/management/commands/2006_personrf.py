

from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source, person_related_factor_converter
from fatalities.models import PersonRelatedFactor, Person
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        PersonRelatedFactor.objects.filter(person__accident__year=2006).delete()
        csv = pd.read_csv(f"{CSV_PATH}2006/FARS2006NationalCSV/PERSON.CSV", encoding='latin-1')
        for x in csv.index:
            if csv['VEH_NO'][x] == 0:
                person = Person.objects.get(accident__year=2006, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            else:
                person = Person.objects.get(Q(accident__year=2006), Q(person_number=csv['PER_NO'][x]),  Q(accident__st_case=csv['ST_CASE'][x]), Q(vehicle__vehicle_number=csv['VEH_NO'][x])|Q(parked_vehicle__vehicle_number=csv['VEH_NO'][x]))
            
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            per_no = str(csv['PER_NO'][x])
            while len(per_no) < 3:
                per_no = "0" + per_no
            for factor in ["P_CF1", "P_CF2", "P_CF3"]:
                number_saved = len(PersonRelatedFactor.objects.filter(person=person))
                new_factor_id = str(number_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"2006{st_case}{veh_no}{per_no}{new_factor_id}"
                
                data_to_save = {"id": primary_key, "person": person}
                factor_code = person_related_factor_converter(csv[factor][x], 2006)
                if factor_code:
                    data_to_save['person_related_factor'] = factor_code
                    print(data_to_save)
                    PersonRelatedFactor.objects.create(**data_to_save)
