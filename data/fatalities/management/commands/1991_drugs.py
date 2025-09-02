from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import drug_test_type_converter, get_data_source
from fatalities.models import Drugs, Person
from django.db.models import Q

# first year of drug result data is in 1991

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Drugs.objects.filter(person__accident__year=1991).delete()
        csv = pd.read_csv(f"{CSV_PATH}1991/PERSON.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_drug_object)
                Drugs.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            if csv['VEH_NO'][x] == 0:
                person = Person.objects.get(accident__year=1991, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            else:
                person = Person.objects.get(Q(accident__year=1991), Q(person_number=csv['PER_NO'][x]),  Q(accident__st_case=csv['ST_CASE'][x]), Q(vehicle__vehicle_number=csv['VEH_NO'][x])|Q(parked_vehicle__vehicle_number=csv['VEH_NO'][x]))
            
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            per_no = str(csv['PER_NO'][x])
            while len(per_no) < 3:
                per_no = "0" + per_no
            primary_key = f"1991{st_case}{veh_no}{per_no}001"

            new_drug_object = Drugs(id=primary_key, 
                                    person=person, 
                                    drug_test_type=drug_test_type_converter(csv["DRUGTEST"][x], 1991), 
                                    drug_test_results=csv["DRUG_RES"][x]
                                    )
            
            bulk_data_upload += [new_drug_object]

        Drugs.objects.bulk_create(bulk_data_upload)
        print(f"we hit it again")