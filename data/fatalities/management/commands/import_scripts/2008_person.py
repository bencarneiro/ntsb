from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import Vehicle, Accident, Person, ParkedVehicle
from fatalities.data_processing import FARS_DATA_CONVERTERS, get_data_source, helmet_misuse_converter
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Person.objects.filter(accident__year=2008).delete()
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
            # 'helmet_misuse',
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
        csv = pd.read_csv(f"{CSV_PATH}2008/FARS2008NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv.index:
            
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            per_no = str(csv['PER_NO'][x])
            while len(per_no) < 3:
                per_no = "0" + per_no
            primary_key = f"2008{st_case}{veh_no}{per_no}"
            
            accident = Accident.objects.get(year=2008, st_case=csv['ST_CASE'][x])
            data_to_save = {
                "id": primary_key,
                "accident": accident
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
                vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv['N_MOT_NO'][x])
            except: 
                vehicle_which_struck_non_motorist = None
            try: 
                parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv['N_MOT_NO'][x])
            except: 
                parked_vehicle_which_struck_non_motorist = None
            
            data_to_save['vehicle_which_struck_non_motorist'] = vehicle_which_struck_non_motorist
            data_to_save['parked_vehicle_which_struck_non_motorist'] = parked_vehicle_which_struck_non_motorist

            for model_field_name in person_model_fields:
                data_source = get_data_source("person." + model_field_name, 2008)
                if data_source:
                    csv_field_name = data_source.split(".")[1]
                    data_converter_function = FARS_DATA_CONVERTERS["person." + model_field_name]
                    data_to_save[model_field_name] = data_converter_function(csv[csv_field_name][x], 2008)

            print(data_to_save)
            # if data_to_save['vehicle_which_struck_non_motorist'] == 0:
            #     data_to_save['vehicle_which_struck_non_motorist'] = None
            # print(data_to_save)
            Person.objects.create(**data_to_save)
            # break