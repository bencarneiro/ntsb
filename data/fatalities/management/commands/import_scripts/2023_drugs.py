

from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import Drugs, Person
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Drugs.objects.filter(person__accident__year=2023).delete()
        csv = pd.read_csv(f"{CSV_PATH}2023/FARS2023NationalCSV/drugs.csv", encoding='latin-1')
        for x in csv.index:
            if csv['VEH_NO'][x] == 0:
                person = Person.objects.get(accident__year=2023, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            else:
                person = Person.objects.get(Q(accident__year=2023), Q(person_number=csv['PER_NO'][x]),  Q(accident__st_case=csv['ST_CASE'][x]), Q(vehicle__vehicle_number=csv['VEH_NO'][x])|Q(parked_vehicle__vehicle_number=csv['VEH_NO'][x]))
            
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            per_no = str(csv['PER_NO'][x])
            while len(per_no) < 3:
                per_no = "0" + per_no
            number_saved = len(Drugs.objects.filter(person=person))
            new_drugs_id = str(number_saved + 1)
            while len(new_drugs_id) < 3:
                new_drugs_id = "0" + new_drugs_id
            primary_key = f"2023{st_case}{veh_no}{per_no}{new_drugs_id}"
            
            data_to_save = {"id": primary_key, "person": person}
            data_to_save['drug_test_type'] = csv['DRUGSPEC'][x]
            data_to_save['drug_test_results'] = csv['DRUGRES'][x]
            data_to_save['drug_test_method'] = csv['DRUGMETHOD'][x]
            data_to_save['drug_quantity'] = csv['DRUGQTY'][x]
            data_to_save['actual_drug_quantity'] = csv['DRUGACTQTY'][x]
            data_to_save['unit_of_measure'] = csv['DRUGUOM'][x]
            print(data_to_save)
            Drugs.objects.create(**data_to_save)
