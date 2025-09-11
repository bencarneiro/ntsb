from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import Vehicle, Accident
from fatalities.data_processing import FARS_DATA_CONVERTERS, get_data_source, speeding_related_converter
import pandas as pd
import numpy as np

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Vehicle.objects.filter(accident__year=1989).delete()
        vehicle_model_fields = [
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
            'pre_event_movement',
            'critical_precrash_event',
            'attempted_avoidance_maneuver',
            'precrash_stability',
            'preimpact_location',
            'crash_type'
        ]
        accident_model_fields = [
            'trafficway_description',
            "total_lanes_in_roadway",
            "speed_limit",
            "roadway_alignment",
            'roadway_grade',
            'roadway_surface_type',
            'roadway_surface_condition',
            'traffic_control_device',
            'traffic_control_device_functioning'
        ]
        csv = pd.read_csv(f"{CSV_PATH}1989/VEHICLE.CSV", encoding='latin-1')
        csv = csv.replace({np.nan: None})
        accident_csv = pd.read_csv(f"{CSV_PATH}1989/ACCIDENT.CSV", encoding='latin-1')
        for x in csv.index:
            accident_temp_df = accident_csv[accident_csv['ST_CASE']==csv['ST_CASE'][x]].reset_index()

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            primary_key = f"1989{st_case}{veh_no}"
            accident = Accident.objects.get(id=int(f"1989{st_case}"))
            data_to_save = {
                "id": primary_key,
                "accident": accident,
                'vehicle_number': int(veh_no)
            }
            for vehicle_model_field_name in vehicle_model_fields:
                data_source = get_data_source("vehicle." + vehicle_model_field_name, 1989)
                if data_source:
                    csv_field_name = data_source.split(".")[1]
                    data_converter_function = FARS_DATA_CONVERTERS["vehicle." + vehicle_model_field_name]
                    data_to_save[vehicle_model_field_name] = data_converter_function(csv[csv_field_name][x], 1989)

            for accident_model_field_name in accident_model_fields:
                data_source = get_data_source("vehicle." + accident_model_field_name, 1989)
                if data_source:
                    csv_field_name = data_source.split(".")[1]
                    data_converter_function = FARS_DATA_CONVERTERS["vehicle." + accident_model_field_name]
                    data_to_save[accident_model_field_name] = data_converter_function(accident_temp_df[csv_field_name][0], 1989)


            speeding_related = None
            speeding_related = speeding_related_converter(csv["VIOL_CHG"][x], "violation", 1989)
            if not speeding_related:
                for factor in ["DR_CF1", "DR_CF2", "DR_CF3"]:
                    speeding_related = speeding_related_converter(csv[factor][x], "drf", 1989)
                    # print(f"DRF output {speeding_related}")
                    if speeding_related:
                        break
            if not speeding_related:
                speeding_related = 0
            # if speeding_related:
                # print("YES YES YES YES YES YES YES YES YES YES YES YES YES YES YES YES YES YESYES YES YES YES YES YES YES YES YES")
            data_to_save['speeding_related'] = speeding_related
            print(data_to_save)
            Vehicle.objects.create(**data_to_save)
            # break