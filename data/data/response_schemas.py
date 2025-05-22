import decimal
from ninja import Schema, Field

from datetime import datetime

from typing import List, Optional

from pydantic import (
    BaseModel,
    NegativeInt,
    NonNegativeInt,
    NonPositiveInt,
    PositiveInt
)

class ChoiceSchema(Schema):
    id: int
    display: str

class StateSchema(Schema):
    id: int
    name: str

class CountySchema(Schema):
    id: int
    name: str

class CitySchema(Schema):
    id: int = Field(None, alias="id")
    name: str = Field(None, alias="name")

class DrugsSchema(Schema):
    id: decimal.Decimal = Field(..., alias="id")
    drug_test_type: int = Field(None, alias="drug_test_type")
    drug_test_type__display: str = Field(None, alias="get_drug_test_type_display")
    drug_test_result: int = Field(None, alias="drug_test_results")

class RaceSchema(Schema):
    id: decimal.Decimal = Field(..., alias="id")
    race: int = Field(None, alias="race")
    race__display: str = Field(None, alias="get_race_display")
    is_multiple_races: int = Field(None, alias="is_multiple_races")
    order: int = Field(None, alias="order")

class PersonRelatedFactorSchema(Schema):
    id: decimal.Decimal = Field(..., alias="id")
    person_related_factor: int = Field(None, alias="person_related_factor")
    person_related_factor__display: str = Field(None, alias="get_person_related_factor_display")
# 
class PedestrianTypeSchema(Schema):
    id: int
    person_type: int = Field(None, alias='person_type')
    person_type__display: str = Field(None, alias='get_person_type_display')
    marked_crosswalk_present: int = Field(None, alias='marked_crosswalk_present')
    marked_crosswalk_present__display: str = Field(None, alias='get_marked_crosswalk_present_display')
    sidewalk_present: int = Field(None, alias='sidewalk_present')
    sidewalk_present__display: str = Field(None, alias='get_sidewalk_present_display')
    in_school_zone: int = Field(None, alias='in_school_zone')
    in_school_zone__display: str = Field(None, alias='get_in_school_zone_display')
    pedestrian_crash_type: int = Field(None, alias='pedestrian_crash_type')
    pedestrian_crash_type__display: str = Field(None, alias='get_pedestrian_crash_type_display')
    bicycle_crash_type: int = Field(None, alias='bicycle_crash_type')
    bicycle_crash_type__display: str = Field(None, alias='get_bicycle_crash_type_display')
    pedestrian_location: int = Field(None, alias='pedestrian_location')
    pedestrian_location__display: str = Field(None, alias='get_pedestrian_location_display')
    bicycle_location: int = Field(None, alias='bicycle_location')
    bicycle_location__display: str = Field(None, alias='get_bicycle_location_display')
    pedestrian_position: int = Field(None, alias='pedestrian_position')
    pedestrian_position__display: str = Field(None, alias='get_pedestrian_position_display')
    bicycle_position: int = Field(None, alias='bicycle_position')
    bicycle_position__display: str = Field(None, alias='get_bicycle_position_display')
    pedestrian_direction: int = Field(None, alias='pedestrian_direction')
    pedestrian_direction__display: str = Field(None, alias='get_pedestrian_direction_display')
    bicycle_direction: int = Field(None, alias='bicycle_direction')
    bicycle_direction__display: str = Field(None, alias='get_bicycle_direction_display')
    motorist_direction: int = Field(None, alias='motorist_direction')
    motorist_direction__display: str = Field(None, alias='get_motorist_direction_display')
    motorist_maneuver: int = Field(None, alias='motorist_maneuver')
    motorist_maneuver__display: str = Field(None, alias='get_motorist_maneuver_display')
    intersection_leg: int = Field(None, alias='intersection_leg')
    intersection_leg__display: str = Field(None, alias='get_intersection_leg_display')
    pedestrian_scenario: str = Field(None, alias='pedestrian_scenario')
    pedestrian_scenario__display: str = Field(None, alias='get_pedestrian_scenario_display')
    pedestrian_crash_group: int = Field(None, alias='pedestrian_crash_group')
    pedestrian_crash_group__display: str = Field(None, alias='get_pedestrian_crash_group_display')
    bicycle_crash_group: int = Field(None, alias='bike_crash_group')
    bicycle_crash_group__display: str = Field(None, alias='get_bike_crash_group_display')


class SafetyEquipmentSchema(Schema): 
    id: int
    helmet: int = Field(None, alias='helmet')
    helmet__display: str = Field(None, alias='get_helmet_display')
    pads: int = Field(None, alias='pads')
    pads__display: str = Field(None, alias='get_pads_display')
    other_protective_equipment: int = Field(None, alias='other_protective_equipment')
    other_protective_equipment__display: str = Field(None, alias='get_other_protective_equipment_display')
    reflective_equipment: int = Field(None, alias='reflective_equipment')
    reflective_equipment__display: str = Field(None, alias='get_reflective_equipment_display')
    lights: int = Field(None, alias='lights')
    lights__display: str = Field(None, alias='get_lights_display')
    other_preventative_equipment: int = Field(None, alias='other_preventative_equipment')
    other_preventative_equipment__display: str = Field(None, alias='get_other_preventative_equipment_display')

    # other_protective_equipment = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)
    # # NM16D NMREFCLO
    # reflective_equipment = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)
    # # NM16E NMLIGHT
    # lights = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)
    # # NM16F NMOTHPRE
    # other_preventative_equipment = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)



class NonmotoristContributingCircumstanceSchema(Schema):
    id: decimal.Decimal = Field(..., alias="id")
    nonmotorist_contributing_circumstance: int  = Field(None, alias="nonmotorist_contributing_circumstance")
    nonmotorist_contributing_circumstance__display: str = Field(None, alias="get_nonmotorist_contributing_circumstance_display")

class NonmotoristImpairedSchema(Schema):
    id: decimal.Decimal = Field(..., alias="id")
    nonmotorist_impaired: int = Field(None, alias="nonmotorist_impaired")
    nonmotorist_impaired__display: str = Field(None, alias="get_nonmotorist_impaired_display")


class NonmotoristDistractedSchema(Schema):
    id: decimal.Decimal = Field(..., alias="id")
    nonmotorist_distracted_by: int = Field(None, alias="nonmotorist_distracted_by")
    nonmotorist_distracted_by__display: str = Field(None, alias="get_nonmotorist_distracted_by_display")


class NonmotoristPriorActionSchema(Schema):
    id: decimal.Decimal = Field(..., alias="id")
    nonmotorist_prior_action: int = Field(None, alias="nonmotorist_prior_action")
    nonmotorist_prior_action__display: str = Field(None, alias="get_nonmotorist_prior_action_display")


class PersonSchema(Schema):
    id: int
    person_number: int = Field(..., alias='person_number')
    age: int	
    sex: int = Field(..., alias="sex")
    sex__display: str = Field(..., alias="get_sex_display")
    person_type: int = Field(..., alias='person_type')	
    person_type__display: str = Field(..., alias='get_person_type_display')
    injury_severity: int = Field(..., alias='injury_severity')	
    injury_severity__display: str = Field(..., alias='get_injury_severity_display')
    seating_position: int = Field(..., alias='seating_position')	
    seating_position__display: str = Field(..., alias='get_seating_position_display')
    restraint_system_use: int = Field(..., alias='restraint_system_use')	
    restraint_system_use__display: str = Field(..., alias='get_restraint_system_use_display')
    restraint_system_misuse: int = Field(..., alias='restraint_system_misuse')	
    restraint_system_misuse__display: str = Field(..., alias='get_restraint_system_misuse_display')
    helmet_use: int = Field(..., alias='helmet_use')	
    helmet_use__display: str = Field(..., alias='get_helmet_use_display')
    helmet_misuse: int = Field(..., alias='helmet_misuse')	
    helmet_misuse__display: str = Field(..., alias='get_helmet_misuse_display')
    airbag_deployed: int = Field(..., alias='airbag_deployed')	
    airbag_deployed__display: str = Field(..., alias='get_airbag_deployed_display')
    ejection: int = Field(..., alias='ejection')	
    ejection__display: str = Field(..., alias='get_ejection_display')
    ejection_path: int = Field(..., alias='ejection_path')	
    ejection_path__display: str = Field(..., alias='get_ejection_path_display')
    extrication: int = Field(..., alias='extrication')	
    extrication__display: str = Field(..., alias='get_extrication_display')
    police_reported_alcohol_involvement: int = Field(..., alias='police_reported_alcohol_involvement')	
    police_reported_alcohol_involvement__display: str = Field(..., alias='get_police_reported_alcohol_involvement_display')
    alcohol_test_given: int = Field(..., alias='alcohol_test_given')	
    alcohol_test_given__display: str = Field(..., alias='get_alcohol_test_given_display')
    alcohol_test_type: int = Field(..., alias='alcohol_test_type')	
    alcohol_test_type__display: str = Field(..., alias='get_alcohol_test_type_display')
    alcohol_test_result: int	
    police_reported_drug_involvement: int = Field(..., alias='police_reported_drug_involvement')	
    police_reported_drug_involvement__display: str = Field(..., alias='get_police_reported_drug_involvement_display')
    drug_tested: int = Field(..., alias='drug_tested')	
    drug_tested__display: str = Field(..., alias='get_drug_tested_display')
    transported_to_medical_facility_by: int = Field(..., alias='transported_to_medical_facility_by')	
    transported_to_medical_facility_by__display: str = Field(..., alias='get_transported_to_medical_facility_by_display')
    died_en_route: int = Field(..., alias='died_en_route')	
    died_en_route__display: str = Field(..., alias='get_died_en_route_display')
    month_of_death: int = Field(..., alias='month_of_death')	
    month_of_death__display: str = Field(..., alias='get_month_of_death_display')
    day_of_death: int	
    year_of_death: int	
    hour_of_death: int	
    minute_of_death: int	
    lag_hours: int	
    lag_minutes: int	
    at_work: int = Field(..., alias='at_work')	
    at_work__display: str = Field(..., alias='get_at_work_display')
    hispanic: int = Field(..., alias='hispanic')	
    hispanic__display: str = Field(..., alias='get_hispanic_display')
    drugs: list[DrugsSchema] = Field(None, alias="drugs_set")
    race: list[RaceSchema] = Field(None, alias="race_set")
    person_related_factors: list[PersonRelatedFactorSchema] = Field(None, alias="personrelatedfactor_set")


class NonMotoristSchema(PersonSchema):
    vehicle_which_struck_non_motorist_id: int = Field(None, alias="vehicle_which_struck_non_motorist.id")	
    non_motorist_device_type: int = Field(..., alias='non_motorist_device_type')	
    non_motorist_device_type__display: str = Field(..., alias='get_non_motorist_device_type_display')
    non_motorist_device_motorization: int = Field(..., alias='non_motorist_device_motorization')	
    non_motorist_device_motorization__display: str = Field(..., alias='get_non_motorist_device_motorization_display')
    non_motorist_location: int = Field(..., alias='non_motorist_location')	
    non_motorist_location__display: str = Field(..., alias='get_non_motorist_location_display')
    pedestrian_type: PedestrianTypeSchema = Field(None, alias='pedestriantype')
    safety_equipment: SafetyEquipmentSchema = Field(None, alias='safetyequipment')
    contributing_circumstances: List[NonmotoristContributingCircumstanceSchema] = Field(None, alias="nonmotoristcontributingcircumstance_set")
    impairments: List[NonmotoristImpairedSchema] = Field(None, alias="nonmotoristimpaired_set")
    distractions: List[NonmotoristDistractedSchema] = Field(None, alias="nonmotoristdistracted_set")
    prior_actions: List[NonmotoristPriorActionSchema] = Field(None, alias="nonmotoristprioraction_set")

class VehiclePersonSchema(PersonSchema):
    id: int
    vehicle_id: int = Field(0, alias='vehicle.vehicle_number')

class ParkedVehiclePersonSchema(Schema):
    id: int
    parked_vehicle_id: int = Field(0, alias='parked_vehicle.parked_vehicle_number')

class VehicleRelatedFactorSchema(Schema):
    id: int
    vehicle_related_factor: int = Field(..., alias='vehicle_related_factor')
    vehicle_related_factor__display: str = Field(..., alias='get_vehicle_related_factor_display')

class DriverRelatedFactorSchema(Schema):
    id: int
    driver_related_factor: int = Field(..., alias='driver_related_factor')
    driver_related_factor__display: str = Field(..., alias='get_driver_related_factor_display')

class VisionSchema(Schema):
    id: int
    visibility: int = Field(..., alias='visibility')
    visibility__display: str = Field(..., alias='get_visibility_display')

class DamageSchema(Schema):
    id: int
    area_of_impact: int = Field(..., alias='area_of_impact')
    area_of_impact__display: str = Field(..., alias='get_area_of_impact_display')

class DriverDistractedSchema(Schema):
    id: int
    distracted_by: int = Field(..., alias='distracted_by')
    distracted_by__display: str = Field(..., alias='get_distracted_by_display')

class DriverImpairedSchema(Schema):
    id: int
    driver_impaired: int = Field(..., alias='driver_impaired')
    driver_impaired__display: str = Field(..., alias='get_driver_impaired_display')

class VehicleFactorSchema(Schema):
    id: int
    contributing_cause: int = Field(..., alias='contributing_cause')
    contributing_cause__display: str = Field(..., alias='get_contributing_cause_display')

class ManeuverSchema(Schema):
    id: int
    driver_maneuvered_to_avoid: int = Field(..., alias='driver_maneuvered_to_avoid')
    driver_maneuvered_to_avoid__display: str = Field(..., alias='get_driver_maneuvered_to_avoid_display')

class ViolationSchema(Schema):
    id: int
    moving_violation: int = Field(..., alias='moving_violation')
    moving_violation__display: str = Field(..., alias='get_moving_violation_display')

class VehicleSchema(Schema):
    id: int
    accident: int = Field(..., alias="accident.id")
    vehicle_number: int
    number_of_occupants: int
    fatalities: int
    hit_and_run: int = Field(..., alias='hit_and_run')	
    hit_and_run__display: str = Field(..., alias='get_hit_and_run_display')
    registration_state: int = Field(..., alias='registration_state')	
    registration_state__display: str = Field(..., alias='get_registration_state_display')
    registered_vehicle_owner: int = Field(..., alias='registered_vehicle_owner')	
    registered_vehicle_owner__display: str = Field(..., alias='get_registered_vehicle_owner_display')
    vehicle_identification_number: str
    vehicle_model_year: int
    vpic_make: Optional[int] = None
    vpic_model: Optional[int] = None
    vpic_body_class: int = Field(..., alias='vpic_body_class')	
    vpic_body_class__display: str = Field(..., alias='get_vpic_body_class_display')
    ncsa_make: int = Field(..., alias='ncsa_make')	
    ncsa_make__display: str = Field(..., alias='get_ncsa_make_display')
    ncsa_model: int = Field(..., alias='ncsa_model')
    body_type: int = Field(..., alias='body_type')	
    body_type__display: str = Field(..., alias='get_body_type_display')
    final_stage_body_class: int = Field(..., alias='final_stage_body_class')	
    final_stage_body_class__display: str = Field(..., alias='get_final_stage_body_class_display')
    gross_vehicle_weight_rating_lower: int = Field(..., alias='gross_vehicle_weight_rating_lower')	
    gross_vehicle_weight_rating_lower__display: str = Field(..., alias='get_gross_vehicle_weight_rating_lower_display')
    gross_vehicle_weight_rating_upper: int = Field(..., alias='gross_vehicle_weight_rating_upper')	
    gross_vehicle_weight_rating_upper__display: str = Field(..., alias='get_gross_vehicle_weight_rating_upper_display')
    vehicle_trailing: int = Field(..., alias='vehicle_trailing')	
    vehicle_trailing__display: str = Field(..., alias='get_vehicle_trailing_display')
    trailer_vin_1: Optional[str] = None
    trailer_vin_2: Optional[str] = None
    trailer_vin_3: Optional[str] = None
    trailer_weight_rating_1: int = Field(..., alias='trailer_weight_rating_1')	
    trailer_weight_rating_1__display: str = Field(..., alias='get_trailer_weight_rating_1_display')
    trailer_weight_rating_2: int = Field(..., alias='trailer_weight_rating_2')	
    trailer_weight_rating_2__display: str = Field(..., alias='get_trailer_weight_rating_2_display')
    trailer_weight_rating_3: int = Field(..., alias='trailer_weight_rating_3')	
    trailer_weight_rating_3__display: str = Field(..., alias='get_trailer_weight_rating_3_display')
    jackknife: int = Field(..., alias='jackknife')	
    jackknife__display: str = Field(..., alias='get_jackknife_display')
    motor_carrier_identification_number: str
    vehicle_configuration: int = Field(..., alias='vehicle_configuration')	
    vehicle_configuration__display: str = Field(..., alias='get_vehicle_configuration_display')
    cargo_body_type: int = Field(..., alias='cargo_body_type')	
    cargo_body_type__display: str = Field(..., alias='get_cargo_body_type_display')
    hazardous_material_involvement: bool
    hazardous_material_placard: int = Field(..., alias='hazardous_material_placard')	
    hazardous_material_placard__display: str = Field(..., alias='get_hazardous_material_placard_display')
    hazardous_material_id: Optional[int] = None
    hazardous_material_class_number: int = Field(..., alias='hazardous_material_class_number')	
    hazardous_material_class_number__display: str = Field(..., alias='get_hazardous_material_class_number_display')
    release_of_hazardous_material: int = Field(..., alias='release_of_hazardous_material')	
    release_of_hazardous_material__display: str = Field(..., alias='get_release_of_hazardous_material_display')
    bus_use: int = Field(..., alias='bus_use')	
    bus_use__display: str = Field(..., alias='get_bus_use_display')
    special_vehicle_use: int = Field(..., alias='special_vehicle_use')	
    special_vehicle_use__display: str = Field(..., alias='get_special_vehicle_use_display')
    emergency_vehicle_use: int = Field(..., alias='emergency_vehicle_use')	
    emergency_vehicle_use__display: str = Field(..., alias='get_emergency_vehicle_use_display')
    travel_speed: int
    underride_override: int = Field(..., alias='underride_override')	
    underride_override__display: str = Field(..., alias='get_underride_override_display')
    rollover: int = Field(..., alias='rollover')	
    rollover__display: str = Field(..., alias='get_rollover_display')
    rollover_location: int = Field(..., alias='rollover_location')	
    rollover_location__display: str = Field(..., alias='get_rollover_location_display')
    initial_contact_point: int = Field(..., alias='initial_contact_point')	
    initial_contact_point__display: str = Field(..., alias='get_initial_contact_point_display')
    extent_of_damage: int = Field(..., alias='extent_of_damage')	
    extent_of_damage__display: str = Field(..., alias='get_extent_of_damage_display')
    vehicle_towed: int = Field(..., alias='vehicle_towed')	
    vehicle_towed__display: str = Field(..., alias='get_vehicle_towed_display')
    most_harmful_event: int = Field(..., alias='most_harmful_event')	
    most_harmful_event__display: str = Field(..., alias='get_most_harmful_event_display')
    fire_occurence: bool     
    automated_driving_system_present: int = Field(..., alias='automated_driving_system_present')	
    automated_driving_system_present__display: str = Field(..., alias='get_automated_driving_system_present_display')
    automated_driving_system_level: int = Field(..., alias='automated_driving_system_level')	
    automated_driving_system_level__display: str = Field(..., alias='get_automated_driving_system_level_display')
    automated_driving_system_engaged: int = Field(..., alias='automated_driving_system_engaged')	
    automated_driving_system_engaged__display: str = Field(..., alias='get_automated_driving_system_engaged_display')
    combined_make_model: Optional[int] = Field(None, alias="combined_make_model")
        
    driver_drinking: int = Field(..., alias='driver_drinking')	
    driver_drinking__display: str = Field(..., alias='get_driver_drinking_display')
    driver_present: int = Field(..., alias='driver_present')	
    driver_present__display: str = Field(..., alias='get_driver_present_display')
    drivers_license_state: int = Field(..., alias='drivers_license_state')	
    drivers_license_state__display: str = Field(..., alias='get_drivers_license_state_display')
    driver_zip_code: int
    non_cdl_license_type: int = Field(..., alias='non_cdl_license_type')	
    non_cdl_license_type__display: str = Field(..., alias='get_non_cdl_license_type_display')
    non_cdl_license_status: int = Field(..., alias='non_cdl_license_status')	
    non_cdl_license_status__display: str = Field(..., alias='get_non_cdl_license_status_display')
    cdl_license_status: int = Field(..., alias='cdl_license_status')	
    cdl_license_status__display: str = Field(..., alias='get_cdl_license_status_display')
    cdl_endorsements: int = Field(..., alias='cdl_endorsements')	
    cdl_endorsements__display: str = Field(..., alias='get_cdl_endorsements_display')
    license_compliance_with_class_of_vehicle: int = Field(..., alias='license_compliance_with_class_of_vehicle')	
    license_compliance_with_class_of_vehicle__display: str = Field(..., alias='get_license_compliance_with_class_of_vehicle_display')
    compliance_with_license_restrictions: int = Field(..., alias='compliance_with_license_restrictions')	
    compliance_with_license_restrictions__display: str = Field(..., alias='get_compliance_with_license_restrictions_display')
    driver_height: int
    driver_weight: int
        
    previous_recorded_crashes: int
    previous_bac_suspensions_underage: Optional[int] = None
    previous_bac_suspensions: Optional[int] = None
    previous_dwi_convictions: int
    previous_speeding_convictions: int
    previous_other_moving_violations: int
    month_of_oldest_violation: int
    year_of_oldest_violation: int
    month_of_newest_violation: int
    year_of_newest_violation: int

    speeding_related: int = Field(..., alias='speeding_related')	
    speeding_related__display: str = Field(..., alias='get_speeding_related_display')
    trafficway_description: int = Field(..., alias='trafficway_description')	
    trafficway_description__display: str = Field(..., alias='get_trafficway_description_display')
    total_lanes_in_roadway: int = Field(..., alias='total_lanes_in_roadway')	
    total_lanes_in_roadway__display: str = Field(..., alias='get_total_lanes_in_roadway_display')
    speed_limit: int
    roadway_alignment: int = Field(..., alias='roadway_alignment')	
    roadway_alignment__display: str = Field(..., alias='get_roadway_alignment_display')
    roadway_grade: int = Field(..., alias='roadway_grade')	
    roadway_grade__display: str = Field(..., alias='get_roadway_grade_display')
    roadway_surface_type: int = Field(..., alias='roadway_surface_type')	
    roadway_surface_type__display: str = Field(..., alias='get_roadway_surface_type_display')
    roadway_surface_condition: int = Field(..., alias='roadway_surface_condition')	
    roadway_surface_condition__display: str = Field(..., alias='get_roadway_surface_condition_display')
    traffic_control_device: int = Field(..., alias='traffic_control_device')	
    traffic_control_device__display: str = Field(..., alias='get_traffic_control_device_display')
    traffic_control_device_functioning: int = Field(..., alias='traffic_control_device_functioning')	
    traffic_control_device_functioning__display: str = Field(..., alias='get_traffic_control_device_functioning_display')
    pre_event_movement: int = Field(..., alias='pre_event_movement')	
    pre_event_movement__display: str = Field(..., alias='get_pre_event_movement_display')
    critical_precrash_event: int = Field(..., alias='critical_precrash_event')	
    critical_precrash_event__display: str = Field(..., alias='get_critical_precrash_event_display')
    attempted_avoidance_maneuver: int = Field(..., alias='attempted_avoidance_maneuver')	
    attempted_avoidance_maneuver__display: str = Field(..., alias='get_attempted_avoidance_maneuver_display')
    precrash_stability: int = Field(..., alias='precrash_stability')	
    precrash_stability__display: str = Field(..., alias='get_precrash_stability_display')
    preimpact_location: int = Field(..., alias='preimpact_location')	
    preimpact_location__display: str = Field(..., alias='get_preimpact_location_display')
    crash_type: int = Field(..., alias='crash_type')	
    crash_type__display: str = Field(..., alias='get_crash_type_display')


    persons: List[VehiclePersonSchema] = Field(..., alias='person_set')
    vehicle_related_factors: List[VehicleRelatedFactorSchema] = Field(..., alias='vehiclerelatedfactor_set')
    driver_related_factors: List[DriverRelatedFactorSchema] = Field(..., alias='driverrelatedfactor_set')
    damages: List[DamageSchema] = Field(..., alias='damage_set')
    distractions: List[DriverDistractedSchema] = Field(..., alias='driverdistracted_set')
    driver_impairments: List[DriverImpairedSchema] = Field(..., alias='driverimpaired_set')
    vehicle_factors: List[VehicleFactorSchema] = Field(..., alias='vehiclefactor_set')
    maneuvers: List[ManeuverSchema] = Field(..., alias='maneuver_set')
    moving_violations: List[ViolationSchema] = Field(..., alias='violation_set')
    vision_obstructions: List[VisionSchema] = Field(..., alias='vision_set')

class ParkedVehicleRelatedFactorSchema(Schema):
    id: int
    parked_vehicle_related_factor: int = Field(..., alias='parked_vehicle_related_factor')
    parked_vehicle_related_factor__display: str = Field(..., alias='get_parked_vehicle_related_factor_display')


class ParkedVehicleSchema(Schema):
    id: int
    accident: int = Field(..., alias="accident.id")
    vehicle_number: int
    fatalities: int
    unit_type: int = Field(..., alias="unit_type")
    unit_type__display: str = Field(..., alias="get_unit_type_display")
    first_harmful_event: int = Field(..., alias="first_harmful_event")
    first_harmful_event__display: str = Field(None, alias='get_first_harmful_event_display')
    manner_of_collision_of_first_harmful_event: int = Field(..., alias="manner_of_collision_of_first_harmful_event")
    manner_of_collision_of_first_harmful_event__display: str = Field(..., alias="get_manner_of_collision_of_first_harmful_event_display")
    hit_and_run: int = Field(..., alias='hit_and_run')	
    hit_and_run__display: str = Field(..., alias='get_hit_and_run_display')
    registration_state: int = Field(..., alias='registration_state')	
    registration_state__display: str = Field(..., alias='get_registration_state_display')
    registered_vehicle_owner: int = Field(..., alias='registered_vehicle_owner')	
    registered_vehicle_owner__display: str = Field(..., alias='get_registered_vehicle_owner_display')
    vehicle_identification_number: str
    vehicle_model_year: int
    vpic_make: Optional[int] = None
    vpic_model: Optional[int] = None

    vpic_body_class: int = Field(..., alias='vpic_body_class')	
    vpic_body_class__display: str = Field(..., alias='get_vpic_body_class_display')
    ncsa_make: int = Field(..., alias='ncsa_make')	
    ncsa_make__display: str = Field(..., alias='get_ncsa_make_display')
    ncsa_model: int = Field(..., alias='ncsa_model')
    body_type: int = Field(..., alias='body_type')	
    body_type__display: str = Field(..., alias='get_body_type_display')
    final_stage_body_class: int = Field(..., alias='final_stage_body_class')	
    final_stage_body_class__display: str = Field(..., alias='get_final_stage_body_class_display')
    gross_vehicle_weight_rating_lower: int = Field(..., alias='gross_vehicle_weight_rating_lower')	
    gross_vehicle_weight_rating_lower__display: str = Field(..., alias='get_gross_vehicle_weight_rating_lower_display')
    gross_vehicle_weight_rating_upper: int = Field(..., alias='gross_vehicle_weight_rating_upper')	
    gross_vehicle_weight_rating_upper__display: str = Field(..., alias='get_gross_vehicle_weight_rating_upper_display')
    vehicle_trailing: int = Field(..., alias='vehicle_trailing')	
    vehicle_trailing__display: str = Field(..., alias='get_vehicle_trailing_display')

    trailer_vin_1: Optional[str] = None
    trailer_vin_2: Optional[str] = None
    trailer_vin_3: Optional[str] = None
    trailer_weight_rating_1: int = Field(..., alias='trailer_weight_rating_1')	
    trailer_weight_rating_1__display: str = Field(..., alias='get_trailer_weight_rating_1_display')
    trailer_weight_rating_2: int = Field(..., alias='trailer_weight_rating_2')	
    trailer_weight_rating_2__display: str = Field(..., alias='get_trailer_weight_rating_2_display')
    trailer_weight_rating_3: int = Field(..., alias='trailer_weight_rating_3')	
    trailer_weight_rating_3__display: str = Field(..., alias='get_trailer_weight_rating_3_display')
    motor_carrier_identification_number: str
    vehicle_configuration: int = Field(..., alias='vehicle_configuration')	
    vehicle_configuration__display: str = Field(..., alias='get_vehicle_configuration_display')
    cargo_body_type: int = Field(..., alias='cargo_body_type')	
    cargo_body_type__display: str = Field(..., alias='get_cargo_body_type_display')
    hazardous_material_involvement: bool
    hazardous_material_placard: int = Field(..., alias='hazardous_material_placard')	
    hazardous_material_placard__display: str = Field(..., alias='get_hazardous_material_placard_display')
    hazardous_material_id: Optional[int] = None
    hazardous_material_class_number: int = Field(..., alias='hazardous_material_class_number')	
    hazardous_material_class_number__display: str = Field(..., alias='get_hazardous_material_class_number_display')
    release_of_hazardous_material: int = Field(..., alias='release_of_hazardous_material')	
    release_of_hazardous_material__display: str = Field(..., alias='get_release_of_hazardous_material_display')
    bus_use: int = Field(..., alias='bus_use')	
    bus_use__display: str = Field(..., alias='get_bus_use_display')
    special_vehicle_use: int = Field(..., alias='special_vehicle_use')	
    special_vehicle_use__display: str = Field(..., alias='get_special_vehicle_use_display')
    emergency_vehicle_use: int = Field(..., alias='emergency_vehicle_use')	
    emergency_vehicle_use__display: str = Field(..., alias='get_emergency_vehicle_use_display')
    
    underride_override: int = Field(..., alias='underride_override')	
    underride_override__display: str = Field(..., alias='get_underride_override_display')
    initial_contact_point: int = Field(..., alias='initial_contact_point')	
    initial_contact_point__display: str = Field(..., alias='get_initial_contact_point_display')
    extent_of_damage: int = Field(..., alias='extent_of_damage')	
    extent_of_damage__display: str = Field(..., alias='get_extent_of_damage_display')
    vehicle_towed: int = Field(..., alias='vehicle_towed')	
    vehicle_towed__display: str = Field(..., alias='get_vehicle_towed_display')
    most_harmful_event: int = Field(..., alias='most_harmful_event')	
    most_harmful_event__display: str = Field(..., alias='get_most_harmful_event_display')
    fire_occurence: bool
    combined_make_model: Optional[int] = Field(None, alias="combined_make_model")
    persons: List[ParkedVehiclePersonSchema] = Field(..., alias='person_set')
    parked_vehicle_related_factors: List[ParkedVehicleRelatedFactorSchema] = Field(..., alias='parkedvehiclerelatedfactor_set')
    number_of_occupants: int
    

class CrashEventSchema(Schema):
    id: int
    crash_event_number: int
    vehicle_1: int = Field(None, alias='vehicle_id_1')
    vehicle_2: int = Field(None, alias='vehicle_id_2')
    area_of_impact_1: int
    area_of_impact_1_display: str = Field(..., alias='get_area_of_impact_1_display')
    sequence_of_events: int
    sequence_of_events_display: str =  Field(..., alias='get_sequence_of_events_display')
    area_of_impact_2: int
    area_of_impact_2_display: str = Field(..., alias='get_area_of_impact_2_display')
    

class CrashRelatedFactorSchema(Schema):

    id: int = Field(..., alias='crash_related_factor')
    factor: str = Field(..., alias='get_crash_related_factor_display')


class WeatherSchema(Schema):

    id: int = Field(..., alias='atmospheric_condition')
    weather: str = Field(..., alias='get_atmospheric_condition_display')

# class RouteSigningSchema(Schema):


class AccidentSchema(Schema):
    id: int
    st_case: int
    fatalities: int
    state: StateSchema
    county: CountySchema
    city: CitySchema = Field(None, alias="city")
    month: int
    day: int
    hour: int
    minute: int
    datetime: datetime
    latitude: Optional[float] = Field(None, alias="latitude")
    longitude: Optional[float] = Field(None, alias="longitude")
    number_of_vehicles: int = Field(0, alias="number_of_vehicles")
    number_of_vehicles_in_transport: int = Field(0, alias="number_of_vehicles_in_transport")
    number_of_parked_vehicles: int = Field(0, alias="number_of_parked_vehicles")
    number_of_persons_in_motor_vehicles: int = Field(0, alias="number_of_persons_in_motor_vehicles")
    number_of_persons_in_motor_vehicles_in_transport: int = Field(0, alias="number_of_persons_in_motor_vehicles_in_transport")
    number_of_persons_in_parked_vehicles: int = Field(0, alias="number_of_persons_in_parked_vehicles")
    number_of_nonmotorists: int = Field(0, alias="number_of_persons_not_in_motor_vehicles")
    number_of_persons_not_in_motor_vehicles_in_transport: int = Field(0, alias="number_of_persons_not_in_motor_vehicles_in_transport")


    trafficway_identifier_1: str
    trafficway_identifier_2: Optional[str] = None

    route_signing: int = Field(..., alias='route_signing')
    route_signing__display: str = Field(..., alias='get_route_signing_display')
    rural_urban: int = Field(..., alias='rural_urban')
    rural_urban__display: str = Field(..., alias='get_rural_urban_display')
    functional_system: int = Field(..., alias='functional_system')
    functional_system__display: str = Field(..., alias='get_functional_system_display')
    road_owner: int = Field(..., alias='road_owner')
    road_owner__display: str = Field(..., alias='get_road_owner_display')
    national_highway_system: int = Field(..., alias="national_highway_system")
    national_highway_system__display: str = Field(..., alias='get_national_highway_system_display')
    special_jurisdiction: int = Field(..., alias="special_jurisdiction")
    special_jurisdiction__display: str = Field(..., alias='get_special_jurisdiction_display')
    milepoint: int = Field(None, alias="milepoint")
    first_harmful_event: int = Field(..., alias="first_harmful_event")
    first_harmful_event__display: str = Field(..., alias='get_first_harmful_event_display')
    manner_of_collision_of_first_harmful_event: int = Field(..., alias="manner_of_collision_of_first_harmful_event")
    manner_of_collision_of_first_harmful_event__display: str = Field(..., alias="get_manner_of_collision_of_first_harmful_event_display")
    within_interchange_area: int = Field(..., alias="within_interchange_area")
    within_interchange_area__display: str = Field(..., alias="get_within_interchange_area_display")


    relation_to_junction: int = Field(..., alias="relation_to_junction")
    relation_to_junction__display: str = Field(..., alias="get_relation_to_junction_display")
    type_of_intersection: int = Field(..., alias="type_of_intersection")
    type_of_intersection__display: str = Field(..., alias="get_type_of_intersection_display")
    relation_to_road: int = Field(..., alias="relation_to_road")
    relation_to_road__display: str = Field(..., alias="get_relation_to_road_display")
    work_zone: int = Field(..., alias="work_zone")
    work_zone__display: str = Field(..., alias="get_work_zone_display")
    light_condition: int = Field(..., alias="light_condition")
    light_condition__display: str = Field(..., alias="get_light_condition_display")
    atmospheric_condition: int = Field(..., alias="atmospheric_condition")
    atmospheric_condition__display: str = Field(..., alias="get_atmospheric_condition_display")
    school_bus_related: bool
    rail_grade_crossing_identifier: str
    ems_notified_hour: int
    ems_notified_minute: int
    ems_arrived_hour: int
    ems_arrived_minute: int
    arrived_at_hospital_hour: int
    arrived_at_hospital_minute: int


    vehicles: List[VehicleSchema] = Field(..., alias='vehicle_set')
    parked_vehicles: List[ParkedVehicleSchema] = Field(..., alias='parkedvehicle_set')
    nonmotorists: List[NonMotoristSchema] = Field(..., alias='nonmotorist_set')
    crash_events: list[CrashEventSchema] = Field(..., alias='crashevent_set')
    crash_related_factors: list[CrashRelatedFactorSchema] = Field(..., alias='crashrelatedfactors_set')
    weather: list[WeatherSchema] = Field(..., alias='weather_set')
    link: str

class ShortAccidentSchema(Schema):
    id: int
    datetime: datetime
    st_case: int
    fatalities: int
    link: str

class GeometrySchema(Schema):
    type: str = Field("Point", alias="not_applicable")
    coordinates: list[float] = Field([], alias="coordinates")

class FeatureSchema(Schema): 
    id: int
    type: str = Field("Feature", alias="not_applicable")
    properties: AccidentSchema
    geometry: GeometrySchema

    @staticmethod
    def resolve_geometry(self):
        return self
    @staticmethod
    def resolve_properties(self):
        return self

class FeatureCollectionSchema(Schema):
    type: str = Field("FeatureCollection", alias="not_applicable")
    features: list[FeatureSchema]


class ShortFeatureSchema(Schema): 
    id: int
    type: str = Field("Feature", alias="not_applicable")
    properties: ShortAccidentSchema
    geometry: GeometrySchema

    @staticmethod
    def resolve_geometry(self):
        return self
    @staticmethod
    def resolve_properties(self):
        return self
    

class MissedConnectionSchema(Schema):
    id: int
    crash_dt: datetime
    info: str

class ShortFeatureCollectionSchema(Schema):
    type: str = Field("FeatureCollection", alias="not_applicable")
    features: list[ShortFeatureSchema]

class MissedConnectionFeatureSchema(Schema): 
    id: int
    type: str = Field("Feature", alias="not_applicable")
    properties: MissedConnectionSchema
    geometry: GeometrySchema

    @staticmethod
    def resolve_geometry(self):
        return self
    @staticmethod
    def resolve_properties(self):
        return self
    
class MissedConnectionFeatureCollectionSchema(Schema):
    type: str = Field("FeatureCollection", alias="not_applicable")
    features: list[MissedConnectionFeatureSchema]
