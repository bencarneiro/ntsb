from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import SafetyEquipment, Person
from django.db.models import Q

# 2010 - 2012 
# have to read all of these from the same field


class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        SafetyEquipment.objects.filter(person__accident__year=2012).delete()
        csv = pd.read_csv(f"{CSV_PATH}2012/FARS2012NationalCSV/SAFETYEQ.CSV", encoding='latin-1')
        for x in csv.index:
            person = Person.objects.get(accident__year=2012, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            equipment_code = csv['MSAFEQMT'][x]
            existing_safety_equipment_records = SafetyEquipment.objects.filter(person=person)
            if len(existing_safety_equipment_records) == 0:
                if csv['MSAFEQMT'][x] in {1}:
                    helmet = 1
                    pads = 1
                    reflective_equipment = 1
                    other_protective_equipment = 1
                    lights = 1
                    other_preventative_equipment = 8
                if csv['MSAFEQMT'][x] in {2}:
                    helmet = 2
                    pads = 1
                    reflective_equipment = 1
                    other_protective_equipment = 1
                    lights = 1
                    other_preventative_equipment = 8
                if csv['MSAFEQMT'][x] in {3}:
                    helmet = 1
                    pads = 1
                    reflective_equipment = 2
                    other_protective_equipment = 1
                    lights = 1
                    other_preventative_equipment = 1
                if csv['MSAFEQMT'][x] in {4}:
                    helmet = 1
                    pads = 2
                    reflective_equipment = 1
                    other_protective_equipment = 1
                    lights = 1
                    other_preventative_equipment = 8
                if csv['MSAFEQMT'][x] in {5}:
                    helmet = 1
                    pads = 1
                    reflective_equipment = 1
                    other_protective_equipment = 1
                    lights = 2
                    other_preventative_equipment = 1
                if csv['MSAFEQMT'][x] in {7}:
                    helmet = 1
                    pads = 1
                    reflective_equipment = 1
                    other_protective_equipment = 2
                    lights = 1
                    other_preventative_equipment = 8
                if csv['MSAFEQMT'][x] in {8}:
                    helmet = 8
                    pads = 8
                    reflective_equipment = 8
                    other_protective_equipment = 8
                    lights = 8
                    other_preventative_equipment = 8
                if csv['MSAFEQMT'][x] in {9}:
                    helmet = 9
                    pads = 9
                    reflective_equipment = 9
                    other_protective_equipment = 9
                    lights = 9
                    other_preventative_equipment = 8
                data_to_save = {
                    "id": person.id,
                    "person": person,
                    "helmet": helmet,
                    "pads": pads,
                    "other_protective_equipment": other_protective_equipment,
                    "reflective_equipment": reflective_equipment,
                    "lights": lights,
                    "other_preventative_equipment" : other_preventative_equipment
                }
                print(data_to_save)
                SafetyEquipment.objects.create(**data_to_save)
            if len(existing_safety_equipment_records) == 1:
                safety_equipment = existing_safety_equipment_records[0]
                if csv['MSAFEQMT'][x] in {2}:
                    safety_equipment.helmet = 2
                    safety_equipment.save()
                    print("update!")
                    print(safety_equipment.__dict__)
                elif csv['MSAFEQMT'][x] in {3}:
                    safety_equipment.reflective_equipment = 2
                    safety_equipment.save()
                    print("update!")
                    print(safety_equipment.__dict__)
                elif csv['MSAFEQMT'][x] in {4}:
                    safety_equipment.pads = 2
                    safety_equipment.save()
                    print("update!")
                    print(safety_equipment.__dict__)
                elif csv['MSAFEQMT'][x] in {5}:
                    safety_equipment.lights = 2
                    safety_equipment.save()
                    print("update!")
                    print(safety_equipment.__dict__)
                elif csv['MSAFEQMT'][x] in {7}:
                    safety_equipment.other_protective_equipment = 2
                    safety_equipment.save()
                    print("update!")
                    print(safety_equipment.__dict__)
                else:
                    print("BADBADNOTGOOD")
                    print("existing record")
                    print(safety_equipment.__dict__)
                    print("new code")