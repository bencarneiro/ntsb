from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import ParkedVehicle, Accident
from fatalities.data_processing import FARS_DATA_CONVERTERS, get_data_source
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        ParkedVehicle.objects.filter(accident__year=2009).delete()
        vehicle_model_fields = [
            'vehicle_number',
            'first_harmful_event',
            'manner_of_collision_of_first_harmful_event',
            'number_of_occupants',
            'unit_type',
            'hit_and_run',
            'registration_state',
            'registered_vehicle_owner',
            'vehicle_identification_number',
            'vehicle_model_year',
            'vpic_make',
            'vpic_model',
            'vpic_body_class',
            'ncsa_make',
            'ncsa_model',
            'body_type',
            'final_stage_body_class',
            'gross_vehicle_weight_rating_lower',
            'gross_vehicle_weight_rating_upper',
            'vehicle_trailing',
            'trailer_vin_1',
            'trailer_vin_2',
            'trailer_vin_3',
            'trailer_weight_rating_1',
            'trailer_weight_rating_2',
            'trailer_weight_rating_3',
            'motor_carrier_identification_number',
            'vehicle_configuration',
            'cargo_body_type',
            'hazardous_material_placard',
            'hazardous_material_id',
            'hazardous_material_class_number',
            'release_of_hazardous_material',
            'bus_use',
            'special_vehicle_use',
            'emergency_vehicle_use',
            'underride_override',
            'initial_contact_point',
            'extent_of_damage',
            'vehicle_towed',
            'most_harmful_event',
            'fire_occurence',
            'fatalities',
            # 'combined_make_model_id'
        ]
        csv = pd.read_csv(f"{CSV_PATH}2009/FARS2009NationalCSV/VEHNIT.CSV", encoding='latin-1')
        for x in csv.index:

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            primary_key = f"2009{st_case}{veh_no}"
            
            accident = Accident.objects.get(year=2009, st_case=csv['ST_CASE'][x])
            data_to_save = {
                "id": primary_key,
                "accident": accident,
                "hazardous_material_involvement": csv['HAZ_INV'][x] - 1
            }
            for model_field_name in vehicle_model_fields:
                data_source = get_data_source("parked_vehicle." + model_field_name, 2009)
                if data_source:
                    csv_field_name = data_source.split(".")[1]
                    data_converter_function = FARS_DATA_CONVERTERS["parked_vehicle." + model_field_name]
                    data_to_save[model_field_name] = data_converter_function(csv[csv_field_name][x], 2009)
            print(data_to_save)
            ParkedVehicle.objects.create(**data_to_save)