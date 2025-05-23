from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import Vehicle, Accident
from fatalities.data_processing import get_data_source
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Vehicle.objects.filter(accident__year=2023).delete()
        vehicle_model_fields = [
            'vehicle_number',
            'number_of_occupants',
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
            'jackknife',
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
            'travel_speed',
            'underride_override',
            'rollover',
            'rollover_location',
            'initial_contact_point',
            'extent_of_damage',
            'vehicle_towed',
            'most_harmful_event',
            'fire_occurence',
            'combined_make_model_id',
            'fatalities',
            'driver_drinking',
            'driver_present',
            'drivers_license_state',
            'driver_zip_code',
            'non_cdl_license_type',
            'non_cdl_license_status',
            'cdl_license_status',
            'cdl_endorsements',
            'license_compliance_with_class_of_vehicle',
            'compliance_with_license_restrictions',
            'driver_height',
            'driver_weight',
            'previous_recorded_crashes',
            'previous_bac_suspensions_underage',
            'previous_bac_suspensions',
            'previous_other_suspensions',
            'previous_dwi_convictions',
            'previous_speeding_convictions',
            'previous_other_moving_violations',
            'month_of_oldest_violation',
            'year_of_oldest_violation',
            'month_of_newest_violation',
            'year_of_newest_violation',
            'speeding_related',
            'trafficway_description',
            'total_lanes_in_roadway',
            'speed_limit',
            'roadway_alignment',
            'roadway_grade',
            'roadway_surface_type',
            'roadway_surface_condition',
            'traffic_control_device',
            'traffic_control_device_functioning',
            'pre_event_movement',
            'critical_precrash_event',
            'attempted_avoidance_maneuver',
            'precrash_stability',
            'preimpact_location',
            'crash_type'
        ]
        csv = pd.read_csv(f"{CSV_PATH}2023/FARS2023NationalCSV/vehicle.csv", encoding='latin-1')
        for x in csv.index:

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            primary_key = f"2023{st_case}{veh_no}"
            
            accident = Accident.objects.get(year=2023, st_case=csv['ST_CASE'][x])
            data_to_save = {
                "id": primary_key,
                "accident": accident,
                "hazardous_material_involvement": csv['HAZ_INV'][x] - 1
            }
            for model_field_name in vehicle_model_fields:
                data_source = get_data_source("vehicle." + model_field_name, 2023)
                csv_field_name = data_source.split(".")[1]
                data_to_save[model_field_name] = csv[csv_field_name][x]
            print(data_to_save)
            Vehicle.objects.create(**data_to_save)
            # break