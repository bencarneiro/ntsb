from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import PedestrianType, Person
from fatalities.data_processing import FARS_DATA_CONVERTERS, get_data_source
import pandas as pd
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        PedestrianType.objects.filter(person__accident__year=2021).delete()
        model_fields = [
            'age',
            'sex',
            'person_type',
            'marked_crosswalk_present',
            'sidewalk_present',
            'in_school_zone',
            'pedestrian_crash_type',
            'bicycle_crash_type',
            'pedestrian_location',
            'bicycle_location',
            'pedestrian_position',
            'bicycle_position',
            'pedestrian_direction',
            'bicycle_direction',
            'motorist_direction',
            'motorist_maneuver',
            'intersection_leg',
            'pedestrian_scenario',
            'pedestrian_crash_group',
            'bike_crash_group'
        ]
        csv = pd.read_csv(f"{CSV_PATH}2021/FARS2021NationalCSV/pbtype.csv", encoding='latin-1')
        for x in csv.index:
            print(f"crash : {csv['ST_CASE'][x]} ----vehicle {csv['VEH_NO'][x]} --- person {csv['PER_NO'][x]}")
            if csv['VEH_NO'][x] == 0:
                person = Person.objects.get(accident__year=2021, person_number=csv['PER_NO'][x], accident__st_case=csv['ST_CASE'][x], vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)
            else:
                # q = Q(income__gte=5000) | Q(income__isnull=True)
                person = Person.objects.get(Q(accident__year=2021), Q(person_number=csv['PER_NO'][x]),  Q(accident__st_case=csv['ST_CASE'][x]), Q(vehicle__vehicle_number=csv['VEH_NO'][x])|Q(parked_vehicle__vehicle_number=csv['VEH_NO'][x]))
            data_to_save = {
                "id": person.id,
                "person": person,
            }
            for model_field_name in model_fields:
                data_source = get_data_source("pedestrian_type." + model_field_name, 2021)
                if data_source:
                    csv_field_name = data_source.split(".")[1]
                    data_converter_function = FARS_DATA_CONVERTERS["pedestrian_type." + model_field_name]
                    data_to_save[model_field_name] = data_converter_function(csv[csv_field_name][x], 2021)
            print(data_to_save)
            PedestrianType.objects.create(**data_to_save)
            # break
