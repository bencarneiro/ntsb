
from ninja import FilterSchema
from typing import Optional

from datetime import datetime

class PersonFilterSchema(FilterSchema):
    id: Optional[int] = None	
    id__gt: Optional[int] = None	
    id__lt: Optional[int] = None	
    accident_id: Optional[int] = None	
    accident_id__gt: Optional[int] = None	
    accident_id__lt: Optional[int] = None	
    vehicle_id: Optional[int] = None	
    vehicle_id__gt: Optional[int] = None	
    vehicle_id__lt: Optional[int] = None	
    parked_vehicle_id: Optional[int] = None	
    parked_vehicle_id__gt: Optional[int] = None	
    parked_vehicle_id__lt: Optional[int] = None	
    person_number: Optional[int] = None	
    person_number__gt: Optional[int] = None	
    person_number__lt: Optional[int] = None	
    age: Optional[int] = None	
    age__gt: Optional[int] = None	
    age__lt: Optional[int] = None	
    sex: Optional[int] = None			
    person_type: Optional[int] = None			
    injury_severity: Optional[int] = None			
    seating_position: Optional[int] = None			
    restraint_system_use: Optional[int] = None			
    restraint_system_misuse: Optional[int] = None			
    helmet_use: Optional[int] = None			
    helmet_misuse: Optional[int] = None			
    airbag_deployed: Optional[int] = None			
    ejection: Optional[int] = None			
    ejection_path: Optional[int] = None			
    extrication: Optional[int] = None			
    police_reported_alcohol_involvement: Optional[int] = None			
    alcohol_test_given: Optional[int] = None			
    alcohol_test_type: Optional[int] = None			
    alcohol_test_result: Optional[int] = None	
    alcohol_test_result__gt: Optional[int] = None	
    alcohol_test_result__lt: Optional[int] = None	
    police_reported_drug_involvement: Optional[int] = None			
    drug_tested: Optional[int] = None			
    transported_to_medical_facility_by: Optional[int] = None			
    died_en_route: Optional[int] = None			
    month_of_death: Optional[int] = None	
    month_of_death__gt: Optional[int] = None	
    month_of_death__lt: Optional[int] = None	
    day_of_death: Optional[int] = None	
    day_of_death__gt: Optional[int] = None	
    day_of_death__lt: Optional[int] = None	
    year_of_death: Optional[int] = None	
    year_of_death__gt: Optional[int] = None	
    year_of_death__lt: Optional[int] = None	
    hour_of_death: Optional[int] = None	
    hour_of_death__gt: Optional[int] = None	
    hour_of_death__lt: Optional[int] = None	
    minute_of_death: Optional[int] = None	
    minute_of_death__gt: Optional[int] = None	
    minute_of_death__lt: Optional[int] = None	
    lag_hours: Optional[int] = None	
    lag_hours__gt: Optional[int] = None	
    lag_hours__lt: Optional[int] = None	
    lag_minutes: Optional[int] = None	
    lag_minutes__gt: Optional[int] = None	
    lag_minutes__lt: Optional[int] = None	
    vehicle_which_struck_non_motorist_id: Optional[int] = None			
    non_motorist_device_type: Optional[int] = None			
    non_motorist_device_motorization: Optional[int] = None			
    non_motorist_location: Optional[int] = None			
    at_work: Optional[int] = None			
    hispanic: Optional[int] = None		
    safetyequipment__helmet: Optional[int] = None
    safetyequipment__pads: Optional[int] = None
    safetyequipment__other_protective_equipment: Optional[int] = None
    safetyequipment__reflective_equipment: Optional[int] = None
    safetyequipment__lights: Optional[int] = None
    safetyequipment__other_preventative_equipment: Optional[int] = None
    pedestriantype__sidewalk_present: Optional[int] = None
    pedestriantype__in_school_zone: Optional[int] = None
    pedestriantype__pedestrian_crash_type: Optional[int] = None
    pedestriantype__marked_crosswalk_present: Optional[int] = None
    pedestriantype__bicycle_crash_type: Optional[int] = None
    pedestriantype__pedestrian_location: Optional[int] = None
    pedestriantype__bicycle_location: Optional[int] = None
    pedestriantype__pedestrian_position: Optional[int] = None
    pedestriantype__bicycle_position: Optional[int] = None
    pedestriantype__pedestrian_direction: Optional[int] = None
    pedestriantype__bicycle_direction: Optional[int] = None
    pedestriantype__motorist_direction: Optional[int] = None
    pedestriantype__motorist_maneuver: Optional[int] = None
    pedestriantype__intersection_leg: Optional[int] = None
    pedestriantype__pedestrian_scenario: Optional[int] = None
    pedestriantype__pedestrian_crash_group: Optional[int] = None
    pedestriantype__bike_crash_group: Optional[int] = None
    
    accident__state_id: Optional[int] = None
    accident__county_id: Optional[int] = None
    accident__year: Optional[int] = None
    accident__year__lt: Optional[int] = None
    accident__year__gt: Optional[int] = None
    accident__datetime__lt: Optional[datetime] = None
    accident__datetime__gt: Optional[datetime] = None
    accident__number_of_persons_not_in_motor_vehicles: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles__lt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles__gt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport__gt: Optional[int] = None
    accident__number_of_vehicles: Optional[int] = None
    accident__number_of_vehicles__lt: Optional[int] = None
    accident__number_of_vehicles__gt: Optional[int] = None
    accident__number_of_vehicles_in_transport: Optional[int] = None
    accident__number_of_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_vehicles_in_transport__gt: Optional[int] = None
    accident__number_of_parked_vehicles: Optional[int] = None
    accident__number_of_parked_vehicles__lt: Optional[int] = None
    accident__number_of_parked_vehicles__gt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles__lt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles__gt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport__gt: Optional[int] = None
    accident__month: Optional[int] = None
    accident__day: Optional[int] = None
    accident__day_of_the_week: Optional[int] = None
    accident__route_signing: Optional[int] = None
    accident__rural_urban: Optional[int] = None
    accident__functional_system: Optional[int] = None
    accident__road_owner: Optional[int] = None
    accident__national_highway_system: Optional[int] = None
    accident__special_jurisdiction: Optional[int] = None
    accident__first_harmful_event: Optional[int] = None
    accident__manner_of_collision_of_first_harmful_event: Optional[int] = None
    accident__at_intersection: Optional[int] = None
    accident__relation_to_junction: Optional[int] = None
    accident__type_of_intersection: Optional[int] = None
    accident__relation_to_road: Optional[int] = None
    accident__work_zone: Optional[int] = None
    accident__light_condition: Optional[int] = None
    accident__atmospheric_condition: Optional[int] = None
    accident__school_bus_related: Optional[bool] = None
    accident__rail_grade_crossing_identifier: Optional[str] = None

class ParkedVehicleFilterSchema(FilterSchema):
    vehicle_number: Optional[int] = None	
    vehicle_number__gt: Optional[int] = None	
    vehicle_number__lt: Optional[int] = None
    number_of_occupants: Optional[int] = None	
    number_of_occupants__gt: Optional[int] = None	
    number_of_occupants__lt: Optional[int] = None
    hit_and_run: Optional[int] = None		
    registration_state: Optional[int] = None		
    registered_vehicle_owner: Optional[int] = None	
    vehicle_identification_number: Optional[str] = None
    vehicle_model_year: Optional[int] = None	
    vehicle_model_year__gt: Optional[int] = None	
    vehicle_model_year__lt: Optional[int] = None
    vpic_make: Optional[int] = None		
    vpic_model: Optional[int] = None		
    vpic_body_class: Optional[int] = None		
    ncsa_make: Optional[int] = None		
    ncsa_model: Optional[int] = None		
    body_type: Optional[int] = None		
    final_stage_body_class: Optional[int] = None		
    gross_vehicle_weight_rating_lower: Optional[int] = None		
    gross_vehicle_weight_rating_upper: Optional[int] = None		
    vehicle_trailing: Optional[int] = None		
    trailer_vin_1: Optional[str] = None
    trailer_vin_2: Optional[str] = None
    trailer_vin_3: Optional[str] = None	
    trailer_weight_rating_1: Optional[int] = None
    trailer_weight_rating_2: Optional[int] = None
    trailer_weight_rating_3: Optional[int] = None
    motor_carrier_identification_number: Optional[int] = None
    vehicle_configuration: Optional[int] = None		
    cargo_body_type: Optional[int] = None		
    hazardous_material_involvement: Optional[bool] = None		
    hazardous_material_placard: Optional[int] = None		
    hazardous_material_id: Optional[int] = None		
    hazardous_material_class_number: Optional[int] = None		
    release_of_hazardous_material: Optional[int] = None		
    bus_use: Optional[int] = None		
    special_vehicle_use: Optional[int] = None		
    emergency_vehicle_use: Optional[int] = None	
    underride_override: Optional[int] = None		
    rollover: Optional[int] = None		
    rollover_location: Optional[int] = None		
    initial_contact_point: Optional[int] = None		
    extent_of_damage: Optional[int] = None		
    vehicle_towed: Optional[int] = None		
    most_harmful_event: Optional[int] = None		
    fire_occurence: Optional[bool] = None		
    combined_make_model_id: Optional[int] = None		
    fatalities: Optional[int] = None	
    fatalities__gt: Optional[int] = None	
    fatalities__lt: Optional[int] = None	
    
    accident__state_id: Optional[int] = None
    accident__county_id: Optional[int] = None
    accident__year: Optional[int] = None
    accident__year__lt: Optional[int] = None
    accident__year__gt: Optional[int] = None
    accident__datetime__lt: Optional[datetime] = None
    accident__datetime__gt: Optional[datetime] = None
    accident__number_of_persons_not_in_motor_vehicles: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles__lt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles__gt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport__gt: Optional[int] = None
    accident__number_of_vehicles: Optional[int] = None
    accident__number_of_vehicles__lt: Optional[int] = None
    accident__number_of_vehicles__gt: Optional[int] = None
    accident__number_of_vehicles_in_transport: Optional[int] = None
    accident__number_of_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_vehicles_in_transport__gt: Optional[int] = None
    accident__number_of_parked_vehicles: Optional[int] = None
    accident__number_of_parked_vehicles__lt: Optional[int] = None
    accident__number_of_parked_vehicles__gt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles__lt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles__gt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport__gt: Optional[int] = None
    accident__month: Optional[int] = None
    accident__day: Optional[int] = None
    accident__day_of_the_week: Optional[int] = None
    accident__route_signing: Optional[int] = None
    accident__rural_urban: Optional[int] = None
    accident__functional_system: Optional[int] = None
    accident__road_owner: Optional[int] = None
    accident__national_highway_system: Optional[int] = None
    accident__special_jurisdiction: Optional[int] = None
    accident__first_harmful_event: Optional[int] = None
    accident__manner_of_collision_of_first_harmful_event: Optional[int] = None
    accident__at_intersection: Optional[int] = None
    accident__relation_to_junction: Optional[int] = None
    accident__type_of_intersection: Optional[int] = None
    accident__relation_to_road: Optional[int] = None
    accident__work_zone: Optional[int] = None
    accident__light_condition: Optional[int] = None
    accident__atmospheric_condition: Optional[int] = None
    accident__school_bus_related: Optional[bool] = None
    accident__rail_grade_crossing_identifier: Optional[str] = None



class VehicleFilterSchema(FilterSchema):

    vehicle_number: Optional[int] = None	
    vehicle_number__gt: Optional[int] = None	
    vehicle_number__lt: Optional[int] = None
    number_of_occupants: Optional[int] = None	
    number_of_occupants__gt: Optional[int] = None	
    number_of_occupants__lt: Optional[int] = None
    hit_and_run: Optional[int] = None		
    registration_state: Optional[int] = None		
    registered_vehicle_owner: Optional[int] = None	
    vehicle_identification_number: Optional[str] = None
    vehicle_model_year: Optional[int] = None	
    vehicle_model_year__gt: Optional[int] = None	
    vehicle_model_year__lt: Optional[int] = None
    vpic_make: Optional[int] = None		
    vpic_model: Optional[int] = None		
    vpic_body_class: Optional[int] = None		
    ncsa_make: Optional[int] = None		
    ncsa_model: Optional[int] = None		
    body_type: Optional[int] = None		
    final_stage_body_class: Optional[int] = None		
    gross_vehicle_weight_rating_lower: Optional[int] = None		
    gross_vehicle_weight_rating_upper: Optional[int] = None		
    vehicle_trailing: Optional[int] = None		
    trailer_vin_1: Optional[str] = None
    trailer_vin_2: Optional[str] = None
    trailer_vin_3: Optional[str] = None	
    trailer_weight_rating_1: Optional[int] = None
    trailer_weight_rating_2: Optional[int] = None
    trailer_weight_rating_3: Optional[int] = None
    jackknife: Optional[int] = None
    motor_carrier_identification_number: Optional[int] = None
    vehicle_configuration: Optional[int] = None		
    cargo_body_type: Optional[int] = None		
    hazardous_material_involvement: Optional[bool] = None		
    hazardous_material_placard: Optional[int] = None		
    hazardous_material_id: Optional[int] = None		
    hazardous_material_class_number: Optional[int] = None		
    release_of_hazardous_material: Optional[int] = None		
    bus_use: Optional[int] = None		
    special_vehicle_use: Optional[int] = None		
    emergency_vehicle_use: Optional[int] = None		
    travel_speed: Optional[int] = None	
    travel_speed__gt: Optional[int] = None	
    travel_speed__lt: Optional[int] = None
    underride_override: Optional[int] = None		
    rollover: Optional[int] = None		
    rollover_location: Optional[int] = None		
    initial_contact_point: Optional[int] = None		
    extent_of_damage: Optional[int] = None		
    vehicle_towed: Optional[int] = None		
    most_harmful_event: Optional[int] = None		
    fire_occurence: Optional[bool] = None		
    automated_driving_system_present: Optional[int] = None		
    automated_driving_system_level: Optional[int] = None		
    automated_driving_system_engaged: Optional[int] = None		
    combined_make_model_id: Optional[int] = None		
    fatalities: Optional[int] = None	
    fatalities__gt: Optional[int] = None	
    fatalities__lt: Optional[int] = None
    driver_drinking: Optional[int] = None		
    driver_present: Optional[int] = None		
    drivers_license_state: Optional[int] = None		
    driver_zip_code: Optional[int] = None		
    non_cdl_license_type: Optional[int] = None		
    non_cdl_license_status: Optional[int] = None		
    cdl_license_status: Optional[int] = None		
    cdl_endorsements: Optional[int] = None		
    license_compliance_with_class_of_vehicle: Optional[int] = None		
    compliance_with_license_restrictions: Optional[int] = None		
    driver_height: Optional[int] = None	
    driver_height__gt: Optional[int] = None	
    driver_height__lt: Optional[int] = None
    driver_weight: Optional[int] = None	
    driver_weight__gt: Optional[int] = None	
    driver_weight__lt: Optional[int] = None
    previous_recorded_crashes: Optional[int] = None		
    previous_bac_suspensions_underage: Optional[int] = None		
    previous_bac_suspensions: Optional[int] = None		
    previous_other_suspensions: Optional[int] = None		
    previous_dwi_convictions: Optional[int] = None		
    previous_speeding_convictions: Optional[int] = None		
    previous_other_moving_violations: Optional[int] = None		
    month_of_oldest_violation: Optional[int] = None		
    year_of_oldest_violation: Optional[int] = None		
    month_of_newest_violation: Optional[int] = None		
    year_of_newest_violation: Optional[int] = None		
    speeding_related: Optional[int] = None		
    trafficway_description: Optional[int] = None		
    total_lanes_in_roadway: Optional[int] = None		
    speed_limit: Optional[int] = None	
    speed_limit__gt: Optional[int] = None	
    speed_limit__lt: Optional[int] = None
    roadway_alignment: Optional[int] = None		
    roadway_grade: Optional[int] = None		
    roadway_surface_type: Optional[int] = None		
    roadway_surface_condition: Optional[int] = None		
    traffic_control_device: Optional[int] = None		
    traffic_control_device_functioning: Optional[int] = None		
    pre_event_movement: Optional[int] = None		
    critical_precrash_event: Optional[int] = None		
    attempted_avoidance_maneuver: Optional[int] = None		
    precrash_stability: Optional[int] = None		
    preimpact_location: Optional[int] = None		
    crash_type: Optional[int] = None	
    
    accident__state_id: Optional[int] = None
    accident__county_id: Optional[int] = None
    accident__year: Optional[int] = None
    accident__year__lt: Optional[int] = None
    accident__year__gt: Optional[int] = None
    accident__datetime__lt: Optional[datetime] = None
    accident__datetime__gt: Optional[datetime] = None
    accident__number_of_persons_not_in_motor_vehicles: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles__lt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles__gt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_persons_not_in_motor_vehicles_in_transport__gt: Optional[int] = None
    accident__number_of_vehicles: Optional[int] = None
    accident__number_of_vehicles__lt: Optional[int] = None
    accident__number_of_vehicles__gt: Optional[int] = None
    accident__number_of_vehicles_in_transport: Optional[int] = None
    accident__number_of_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_vehicles_in_transport__gt: Optional[int] = None
    accident__number_of_parked_vehicles: Optional[int] = None
    accident__number_of_parked_vehicles__lt: Optional[int] = None
    accident__number_of_parked_vehicles__gt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles__lt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles__gt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport__lt: Optional[int] = None
    accident__number_of_persons_in_motor_vehicles_in_transport__gt: Optional[int] = None
    accident__month: Optional[int] = None
    accident__day: Optional[int] = None
    accident__day_of_the_week: Optional[int] = None
    accident__route_signing: Optional[int] = None
    accident__rural_urban: Optional[int] = None
    accident__functional_system: Optional[int] = None
    accident__road_owner: Optional[int] = None
    accident__national_highway_system: Optional[int] = None
    accident__special_jurisdiction: Optional[int] = None
    accident__first_harmful_event: Optional[int] = None
    accident__manner_of_collision_of_first_harmful_event: Optional[int] = None
    accident__at_intersection: Optional[int] = None
    accident__relation_to_junction: Optional[int] = None
    accident__type_of_intersection: Optional[int] = None
    accident__relation_to_road: Optional[int] = None
    accident__work_zone: Optional[int] = None
    accident__light_condition: Optional[int] = None
    accident__atmospheric_condition: Optional[int] = None
    accident__school_bus_related: Optional[bool] = None
    accident__rail_grade_crossing_identifier: Optional[str] = None	

class AccidentFilterSchema(FilterSchema):
    state_id: Optional[int] = None
    county_id: Optional[int] = None
    year: Optional[int] = None
    year__lt: Optional[int] = None
    year__gt: Optional[int] = None
    datetime__lt: Optional[datetime] = None
    datetime__gt: Optional[datetime] = None
    fatalities: Optional[int] = None
    fatalities__lt: Optional[int] = None
    fatalities__gt: Optional[int] = None
    number_of_persons_not_in_motor_vehicles: Optional[int] = None
    number_of_persons_not_in_motor_vehicles__lt: Optional[int] = None
    number_of_persons_not_in_motor_vehicles__gt: Optional[int] = None
    number_of_persons_not_in_motor_vehicles_in_transport: Optional[int] = None
    number_of_persons_not_in_motor_vehicles_in_transport__lt: Optional[int] = None
    number_of_persons_not_in_motor_vehicles_in_transport__gt: Optional[int] = None
    number_of_vehicles: Optional[int] = None
    number_of_vehicles__lt: Optional[int] = None
    number_of_vehicles__gt: Optional[int] = None
    number_of_vehicles_in_transport: Optional[int] = None
    number_of_vehicles_in_transport__lt: Optional[int] = None
    number_of_vehicles_in_transport__gt: Optional[int] = None
    number_of_parked_vehicles: Optional[int] = None
    number_of_parked_vehicles__lt: Optional[int] = None
    number_of_parked_vehicles__gt: Optional[int] = None
    number_of_persons_in_motor_vehicles: Optional[int] = None
    number_of_persons_in_motor_vehicles__lt: Optional[int] = None
    number_of_persons_in_motor_vehicles__gt: Optional[int] = None
    number_of_persons_in_motor_vehicles_in_transport: Optional[int] = None
    number_of_persons_in_motor_vehicles_in_transport__lt: Optional[int] = None
    number_of_persons_in_motor_vehicles_in_transport__gt: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    day_of_the_week: Optional[int] = None
    route_signing: Optional[int] = None
    rural_urban: Optional[int] = None
    functional_system: Optional[int] = None
    road_owner: Optional[int] = None
    national_highway_system: Optional[int] = None
    special_jurisdiction: Optional[int] = None
    first_harmful_event: Optional[int] = None
    manner_of_collision_of_first_harmful_event: Optional[int] = None
    at_intersection: Optional[int] = None
    relation_to_junction: Optional[int] = None
    type_of_intersection: Optional[int] = None
    relation_to_road: Optional[int] = None
    work_zone: Optional[int] = None
    light_condition: Optional[int] = None
    atmospheric_condition: Optional[int] = None
    school_bus_related: Optional[bool] = None
    rail_grade_crossing_identifier: Optional[str] = None

class CrashEventFilterSchema(FilterSchema):
    accident_id: Optional[int] = None
    accident_id__lt: Optional[int] = None
    accident_id__gt: Optional[int] = None
    crash_event_number: Optional[int] = None
    crash_event_number__lt: Optional[int] = None
    crash_event_number__gt: Optional[int] = None
    sequence_of_events: Optional[int] = None

class WeatherFilterSchema(FilterSchema):
    atmospheric_condition: Optional[int] = None

class CrashRelatedFactorFilterSchema(FilterSchema):
    crash_related_factor: Optional[int] = None

class DamageFilterSchema(FilterSchema):
    area_of_impact: Optional[int] = None
    
class DriverRelatedFactorFilterSchema(FilterSchema):
    driver_related_factor: Optional[int] = None
    
class DriverDistractedFilterSchema(FilterSchema):
    distracted_by: Optional[int] = None
    
class DriverImpairedFilterSchema(FilterSchema):
    driver_impaired: Optional[int] = None
    
class VehicleFactorFilterSchema(FilterSchema):
    contributing_cause: Optional[int] = None
    
class ManeuverFilterSchema(FilterSchema):
    driver_maneuvered_to_avoid: Optional[int] = None
    
class VehicleRelatedFactorFilterSchema(FilterSchema):
    vehicle_related_factor: Optional[int] = None

class ParkedVehicleRelatedFactorFilterSchema(FilterSchema):
    parked_vehicle_related_factor: Optional[int] = None
    
class ViolationFilterSchema(FilterSchema):
    moving_violation: Optional[int] = None

class VisionFilterSchema(FilterSchema):
    vision: Optional[int] = None
    

class DrugsFilterSchema(FilterSchema):
    drug_test_type: Optional[int] = None
    drug_test_result: Optional[int] = None
    drug_test_result__lt: Optional[int] = None
    drug_test_result__gt: Optional[int] = None

class RaceFilterSchema(FilterSchema):
    race: Optional[int] = None
    is_multiple_races: Optional[int] = None
    order: Optional[int] = None

class PersonRelatedFactorFilterSchema(FilterSchema):
    person_related_factor: Optional[int] = None
    
class NonmotoristContributingCircumstanceFilterSchema(FilterSchema):
    nonmotorist_contributing_circumstance: Optional[int] = None

class NonmotoristImpairedFilterSchema(FilterSchema):
    nonmotorist_impaired: Optional[int] = None


class NonmotoristDistractedFilterSchema(FilterSchema):
    nonmotorist_distracted_by: Optional[int] = None


class NonmotoristPriorActionFilterSchema(FilterSchema):
    nonmotorist_prior_action: Optional[int] = None


