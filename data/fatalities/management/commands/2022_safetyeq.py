from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import SafetyEquipment, Person
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        SafetyEquipment.objects.filter(person__accident__year=2022).delete()
        csv = pd.read_csv(f"{CSV_PATH}2022/FARS2022NationalCSV/safetyeq.csv", encoding='latin-1')
        for x in csv.index:
            person = Person.objects.get(accident__year=2022, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            data_to_save = {
                "id": person.id,
                "person": person,
                "helmet": csv['NMHELMET'][x],
                "pads": csv['NMPROPAD'][x],
                "other_protective_equipment": csv['NMOTHPRO'][x],
                "reflective_equipment": csv['NMREFCLO'][x],
                "lights": csv['NMLIGHT'][x],
                "other_preventative_equipment" : csv['NMOTHPRE'][x]
            }
            print(data_to_save)
            SafetyEquipment.objects.create(**data_to_save)
