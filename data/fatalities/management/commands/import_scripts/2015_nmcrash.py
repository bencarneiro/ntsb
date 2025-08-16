

from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.data_processing import get_data_source
from fatalities.models import NonmotoristContributingCircumstance, Person
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        NonmotoristContributingCircumstance.objects.filter(person__accident__year=2015).delete()
        csv = pd.read_csv(f"{CSV_PATH}2015/FARS2015NationalCSV/nmcrash.csv", encoding='latin-1')
        for x in csv.index:
            person = Person.objects.get(accident__year=2015, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            per_no = str(csv['PER_NO'][x])
            while len(per_no) < 3:
                per_no = "0" + per_no
            number_saved = len(NonmotoristContributingCircumstance.objects.filter(person=person))
            new_factor_id = str(number_saved + 1)
            while len(new_factor_id) < 3:
                new_factor_id = "0" + new_factor_id
            primary_key = f"2015{st_case}{veh_no}{per_no}{new_factor_id}"
            
            data_to_save = {"id": primary_key,"person": person}
            
            data_source = get_data_source("nonmotorist_contributing_circumstance.nonmotorist_contributing_circumstance", 2015)
            csv_field_name = data_source.split(".")[1]
            data_to_save['nonmotorist_contributing_circumstance'] = csv[csv_field_name][x]
            print(data_to_save)
            NonmotoristContributingCircumstance.objects.create(**data_to_save)
