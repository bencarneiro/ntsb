from django.core.management.base import BaseCommand
from fatalities.models import Vehicle, Accident, Person, ParkedVehicle
from fatalities.data_processing import get_data_source
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Person.objects.filter(accident__year=2022).delete()
        person_model_fields = [
            'person_number',
            'age',
            'sex',
            'person_type',
            'injury_severity',
            'seating_position',
            'restraint_system_use',
            'restraint_system_misuse',
            'helmet_use',
            'helmet_misuse',
            'airbag_deployed',
            'ejection',
            'ejection_path',
            'extrication',
            'police_reported_alcohol_involvement',
            'alcohol_test_given',
            'alcohol_test_type',
            'alcohol_test_result',
            'police_reported_drug_involvement',
            'drug_tested',
            'transported_to_medical_facility_by',
            'died_en_route',
            'month_of_death',
            'day_of_death',
            'year_of_death',
            'hour_of_death',
            'minute_of_death',
            'lag_hours',
            'lag_minutes',
            'non_motorist_device_type',
            'non_motorist_device_motorization',
            'non_motorist_location',
            'at_work',
            'hispanic'
        ]
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/person.csv", encoding='latin-1', low_memory=False).fillna(0)
        for x in csv.index:
            accident = Accident.objects.get(st_case=csv['ST_CASE'][x])
            data_to_save = {
                "accident": accident,
            }
            try:
                vehicle = Vehicle.objects.get(accident=accident, vehicle_number=csv['VEH_NO'][x])
            except:
                vehicle = None
            data_to_save['vehicle'] = vehicle
            try:
                parked_vehicle = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv['VEH_NO'][x])
            except:
                parked_vehicle = None
            data_to_save['parked_vehicle'] = parked_vehicle

            try: 
                vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv['STR_VEH'][x])
            except: 
                vehicle_which_struck_non_motorist = None
            
            data_to_save['vehicle_which_struck_non_motorist'] = vehicle_which_struck_non_motorist

            for model_field_name in person_model_fields:
                data_source = get_data_source("person." + model_field_name, 2022)
                csv_field_name = data_source.split(".")[1]
                data_to_save[model_field_name] = csv[csv_field_name][x]

            print(data_to_save)
            # if data_to_save['vehicle_which_struck_non_motorist'] == 0:
            #     data_to_save['vehicle_which_struck_non_motorist'] = None
            # print(data_to_save)
            Person.objects.create(**data_to_save)
            # break