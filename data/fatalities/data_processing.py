from fatalities.data_dictionary import FARS_DATA_DICTIONARY
from fatalities.models import City, County, State

def get_column_history(column):
    return FARS_DATA_DICTIONARY[column]

def get_data_source(column, year):
    for period in FARS_DATA_DICTIONARY[column]:
        if period['range']['start'] <= year and ((not period['range']['end']) or period['range']['end'] >= year):
            return period['key']
    return None,

def get_multiple_data_sources(column, year):
    locations = []
    for period in FARS_DATA_DICTIONARY[column]:
        if period['range']['start'] <= year and ((not period['range']['end']) or period['range']['end'] >= year):
            locations += [period['key']]
    return locations
    
def get_county(state_id, county_id):
    return County.objects.get(state_id=state_id, county_id=county_id)

def year_converter(year_field, year):
    if year < 1998:
        return 1900 + int(year_field)
    return int(year_field)

def route_signing_converter(route_signing, year):
    if year < 1981:
        if route_signing in [2,5]:
            return 8
        if route_signing == 3:
            return 2
        if route_signing == 4:
            return 3
        if route_signing == 6:
            return 4
        if route_signing == 7:
            return 6
    return route_signing 

def land_use_converter(land_use, year):
    if year < 1987:
        return land_use
    if year < 2015:
        if land_use in {1,2,3,4,5,6,9}:
            return 1
        if land_use in {11,12,13,14,15,16,19}:
            return 2
        return 9
    return land_use

def functional_system_converter(functional_system, year):
    if year < 1981:
        return None
    if year < 1987:
        if functional_system in {6}:
            return 5
        if functional_system in {7}:
            return 6
        if functional_system in {8}:
            return 7
        if functional_system in {9}:
            return 99
    if year < 2015:
        if functional_system in {1,11}:
            return 1
        if functional_system in {12}:
            return 2
        if functional_system in {2,13}:
            return 3
        if functional_system in {3,14}:
            return 4
        if functional_system in {4,15}:
            return 5
        if functional_system in {5}:
            return 6
        if functional_system in {6,16}:
            return 7
        if functional_system in {9,19,99}:
            return 99      
    return functional_system 
    
# 1975-1980
# This data element is included in the format, but is not initialized. Do not use it.
#  1981-1986
#  1 Principal Arterial – Interstate
#  2 Principal Arterial – Other Urban Freeways and Expressways
#  3 Principal Arterial – Other
#  4 Minor Arterial
#  5 Urban Collector
#  6 Major Rural Collector
#  7 Minor Rural Collector
#  8 Local Road or Street
#  9 Unknown
# 2015-Later
#  1 Interstate
#  2 Principal Arterial – Other Freeways and Expressways
#  3 Principal Arterial – Other
#  4 Minor Arterial
#  5 Major Collector
#  6 Minor Collector
#  7 Local
#  96 Trafficway Not in State Inventory
#  98 Not Reported
#  99 Unknown


FARS_DATA_CONVERTERS = {
    'accident.st_case': lambda value, year: value,
    'accident.number_of_persons_not_in_motor_vehicles': lambda value, year: value,
    'accident.number_of_persons_not_in_motor_vehicles_in_transport': lambda value, year: value,
    'accident.number_of_vehicles': lambda value, year: value,
    'accident.number_of_vehicles_in_transport': lambda value, year: value,
    'accident.number_of_parked_vehicles': lambda value, year: value,
    'accident.number_of_persons_in_motor_vehicles': lambda value, year: value,
    'accident.number_of_persons_in_motor_vehicles_in_transport': lambda value, year: value,
    'accident.month': lambda value, year: value,
    'accident.day': lambda value, year: value,
    'accident.day_of_the_week': lambda value, year: value,
    'accident.year': year_converter,
    'accident.hour': lambda value, year: value,
    'accident.minute': lambda value, year: value,
    'accident.trafficway_identifier_1': lambda value, year: value,
    'accident.trafficway_identifier_2': lambda value, year: value,
    'accident.route_signing': route_signing_converter,
    'accident.rural_urban': land_use_converter,
    'accident.functional_system': functional_system_converter,
    'accident.road_owner': lambda value, year: value,
    'accident.national_highway_system': lambda value, year: value,
    'accident.special_jurisdiction': None,
    'accident.milepoint': None,
    'accident.latitude': None,
    'accident.longitude': None,
    'accident.first_harmful_event': None,
    'accident.manner_of_collision_of_first_harmful_event': None,
    'accident.at_intersection': None,
    'accident.relation_to_junction': None,
    'accident.type_of_intersection': None,
    'accident.relation_to_road': None,
    'accident.work_zone': None,
    'accident.light_condition': None,
    'accident.atmospheric_condition': None,
    'accident.school_bus_related': None,
    'accident.rail_grade_crossing_identifier': None,
    'accident.ems_notified_hour': None,
    'accident.ems_notified_minute': None,
    'accident.ems_arrived_hour': None,
    'accident.ems_arrived_minute': None,
    'accident.arrived_at_hospital_hour': None,
    'accident.arrived_at_hospital_minute': None,
    'accident.fatalities': None,
    'vehicle.vehicle_number': None,
    'vehicle.number_of_occupants': None,
    'vehicle.hit_and_run': None,
    'vehicle.registration_state': None,
    'vehicle.registered_vehicle_owner': None,
    'vehicle.vehicle_identification_number': None,
    'vehicle.vehicle_model_year': None,
    'vehicle.vpic_make': None,
    'vehicle.vpic_model': None,
    'vehicle.vpic_body_class': None,
    'vehicle.ncsa_make': None,
    'vehicle.ncsa_model': None,
    'vehicle.body_type': None,
    'vehicle.final_stage_body_class': None,
    'vehicle.gross_vehicle_weight_rating_lower': None,
    'vehicle.gross_vehicle_weight_rating_upper': None,
    'vehicle.vehicle_trailing': None,
    'vehicle.trailer_vin_1': None,
    'vehicle.trailer_vin_2': None,
    'vehicle.trailer_vin_3': None,
    'vehicle.trailer_weight_rating_1': None,
    'vehicle.trailer_weight_rating_2': None,
    'vehicle.trailer_weight_rating_3': None,
    'vehicle.jackknife': None,
    'vehicle.motor_carrier_identification_number': None,
    'vehicle.vehicle_configuration': None,
    'vehicle.cargo_body_type': None,
    'vehicle.hazardous_material_involvement': None,
    'vehicle.hazardous_material_placard': None,
    'vehicle.hazardous_material_id': None,
    'vehicle.hazardous_material_class_number': None,
    'vehicle.release_of_hazardous_material': None,
    'vehicle.bus_use': None,
    'vehicle.special_vehicle_use': None,
    'vehicle.emergency_vehicle_use': None,
    'vehicle.travel_speed': None,
    'vehicle.underride_override': None,
    'vehicle.rollover': None,
    'vehicle.rollover_location': None,
    'vehicle.initial_contact_point': None,
    'vehicle.extent_of_damage': None,
    'vehicle.vehicle_towed': None,
    'vehicle.most_harmful_event': None,
    'vehicle.fire_occurence': None,
    'vehicle.automated_driving_system_present': None,
    'vehicle.automated_driving_system_level': None,
    'vehicle.automated_driving_system_engaged': None,
    'vehicle.combined_make_model_id': None,
    'vehicle.fatalities': None,
    'vehicle.driver_drinking': None,
    'vehicle.driver_present': None,
    'vehicle.drivers_license_state': None,
    'vehicle.driver_zip_code': None,
    'vehicle.non_cdl_license_type': None,
    'vehicle.non_cdl_license_status': None,
    'vehicle.cdl_license_status': None,
    'vehicle.cdl_endorsements': None,
    'vehicle.license_compliance_with_class_of_vehicle': None,
    'vehicle.compliance_with_license_restrictions': None,
    'vehicle.driver_height': None,
    'vehicle.driver_weight': None,
    'vehicle.previous_recorded_crashes': None,
    'vehicle.previous_bac_suspensions_underage': None,
    'vehicle.previous_bac_suspensions': None,
    'vehicle.previous_other_suspensions': None,
    'vehicle.previous_dwi_convictions': None,
    'vehicle.previous_speeding_convictions': None,
    'vehicle.previous_other_moving_violations': None,
    'vehicle.month_of_oldest_violation': None,
    'vehicle.year_of_oldest_violation': None,
    'vehicle.month_of_newest_violation': None,
    'vehicle.year_of_newest_violation': None,
    'vehicle.speeding_related': None,
    'vehicle.trafficway_description': None,
    'vehicle.total_lanes_in_roadway': None,
    'vehicle.speed_limit': None,
    'vehicle.roadway_alignment': None,
    'vehicle.roadway_grade': None,
    'vehicle.roadway_surface_type': None,
    'vehicle.roadway_surface_condition': None,
    'vehicle.traffic_control_device': None,
    'vehicle.traffic_control_device_functioning': None,
    'vehicle.pre_event_movement': None,
    'vehicle.critical_precrash_event': None,
    'vehicle.attempted_avoidance_maneuver': None,
    'vehicle.precrash_stability': None,
    'vehicle.preimpact_location': None,
    'vehicle.crash_type': None,
    'person.person_number': None,
    'person.age': None,
    'person.sex': None,
    'person.person_type': None,
    'person.injury_severity': None,
    'person.seating_position': None,
    'person.restraint_system_use': None,
    'person.restraint_system_misuse': None,
    'person.helmet_use': None,
    'person.helmet_misuse': None,
    'person.airbag_deployed': None,
    'person.ejection': None,
    'person.ejection_path': None,
    'person.extrication': None,
    'person.police_reported_alcohol_involvement': None,
    'person.alcohol_test_given': None,
    'person.alcohol_test_type': None,
    'person.alcohol_test_result': None,
    'person.police_reported_drug_involvement': None,
    'person.drug_tested': None,
    'person.transported_to_medical_facility_by': None,
    'person.died_en_route': None,
    'person.month_of_death': None,
    'person.day_of_death': None,
    'person.year_of_death': None,
    'person.hour_of_death': None,
    'person.minute_of_death': None,
    'person.lag_hours': None,
    'person.lag_minutes': None,
    'person.vehicle_which_struck_non_motorist': None,
    'person.non_motorist_device_type': None,
    'person.non_motorist_device_motorization': None,
    'person.non_motorist_location': None,
    'person.at_work': None,
    'person.hispanic': None,
    'parked_vehicle.vehicle_number': None,
    'parked_vehicle.first_harmful_event': None,
    'parked_vehicle.manner_of_collision_of_first_harmful_event': None,
    'parked_vehicle.number_of_occupants': None,
    'parked_vehicle.unit_type': None,
    'parked_vehicle.hit_and_run': None,
    'parked_vehicle.registration_state': None,
    'parked_vehicle.registered_vehicle_owner': None,
    'parked_vehicle.vehicle_identification_number': None,
    'parked_vehicle.vehicle_model_year': None,
    'parked_vehicle.vpic_make': None,
    'parked_vehicle.vpic_model': None,
    'parked_vehicle.vpic_body_class': None,
    'parked_vehicle.ncsa_make': None,
    'parked_vehicle.ncsa_model': None,
    'parked_vehicle.body_type': None,
    'parked_vehicle.final_stage_body_class': None,
    'parked_vehicle.gross_vehicle_weight_rating_lower': None,
    'parked_vehicle.gross_vehicle_weight_rating_upper': None,
    'parked_vehicle.vehicle_trailing': None,
    'parked_vehicle.trailer_vin_1': None,
    'parked_vehicle.trailer_vin_2': None,
    'parked_vehicle.trailer_vin_3': None,
    'parked_vehicle.trailer_weight_rating_1': None,
    'parked_vehicle.trailer_weight_rating_2': None,
    'parked_vehicle.trailer_weight_rating_3': None,
    'parked_vehicle.motor_carrier_identification_number': None,
    'parked_vehicle.vehicle_configuration': None,
    'parked_vehicle.cargo_body_type': None,
    'parked_vehicle.hazardous_material_involvement': None,
    'parked_vehicle.hazardous_material_placard': None,
    'parked_vehicle.hazardous_material_id': None,
    'parked_vehicle.hazardous_material_class_number': None,
    'parked_vehicle.release_of_hazardous_material': None,
    'parked_vehicle.bus_use': None,
    'parked_vehicle.special_vehicle_use': None,
    'parked_vehicle.emergency_vehicle_use': None,
    'parked_vehicle.underride_override': None,
    'parked_vehicle.initial_contact_point': None,
    'parked_vehicle.extent_of_damage': None,
    'parked_vehicle.vehicle_towed': None,
    'parked_vehicle.most_harmful_event': None,
    'parked_vehicle.fire_occurence': None,
    'parked_vehicle.fatalities': None,
    'parked_vehicle.combined_make_model_id': None,
    'pedestrian_type.age': None,
    'pedestrian_type.sex': None,
    'pedestrian_type.person_type': None,
    'pedestrian_type.marked_crosswalk_present': None,
    'pedestrian_type.sidewalk_present': None,
    'pedestrian_type.in_school_zone': None,
    'pedestrian_type.pedestrian_crash_type': None,
    'pedestrian_type.bicycle_crash_type': None,
    'pedestrian_type.pedestrian_location': None,
    'pedestrian_type.bicycle_location': None,
    'pedestrian_type.pedestrian_position': None,
    'pedestrian_type.bicycle_position': None,
    'pedestrian_type.pedestrian_direction': None,
    'pedestrian_type.bicycle_direction': None,
    'pedestrian_type.motorist_direction': None,
    'pedestrian_type.motorist_maneuver': None,
    'pedestrian_type.intersection_leg': None,
    'pedestrian_type.pedestrian_scenario': None,
    'pedestrian_type.pedestrian_crash_group': None,
    'pedestrian_type.bike_crash_group': None,
    'crash_event.crash_event_number': None,
    'crash_event.vehicle_1': None,
    'crash_event.area_of_impact_1': None,
    'crash_event.sequence_of_events': None,
    'crash_event.vehicle_2': None,
    'crash_event.area_of_impact_2': None,
    'vehicle_event.event_number': None,
    'vehicle_event.vehicle_event_number': None,
    'vehicle_event.vehicle': None,
    'vehicle_event.vehicle_1': None,
    'vehicle_event.area_of_impact_1': None,
    'vehicle_event.sequence_of_events': None,
    'vehicle_event.vehicle_2': None,
    'vehicle_event.area_of_impact_2': None,
    'vehicle_sequence_of_events.vehicle': None,
    'vehicle_sequence_of_events.vehicle_event_number': None,
    'vehicle_sequence_of_events.sequence_of_events': None,
    'vehicle_sequence_of_events.area_of_impact': None,
    'crash_related_factors.crash_related_factor': None,
    'weather.weather': None,
    'vehicle_related_factor.vehicle_related_factor': None,
    'parked_vehicle_related_factor.vehicle_related_factor': None,
    'driver_related_factor.driver_related_factor': None,
    'damage.area_of_impact': None,
    'driver_distracted.distracted_by': None,
    'driver_impaired.driver_impaired': None,
    'vehicle_factor.contributing_cause': None,
    'maneuver.driver_maneuvered_to_avoid': None,
    'violation.moving_violation': None,
    'vision.visibility': None,
    'person_related_factor.person_related_factor': None,
    'drugs.drug_test_type': None,
    'drugs.drug_test_results': None,
    'race.race': None,
    'nonmotorist_contributing_circumstance.nonmotorist_contributing_circumstance': None,
    'nonmotorist_distracted.nonmotorist_distracted_by': None,
    'nonmotorist_impaired.nonmotorist_impaired': None,
    'nonmotorist_prior_action.nonmotorist_prior_action': None,
    'safety_equipment.helmet': None,
    'safety_equipment.pads': None,
    'safety_equipment.other_protective_equipment': None,
    'safety_equipment.reflective_equipment': None,
    'safety_equipment.lights': None,
    'safety_equipment.other_preventative_equipment': None,
}