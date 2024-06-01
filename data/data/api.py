from ninja import NinjaAPI
from typing import List
from ninja import Schema, Field, FilterSchema, Query
from fatalities.models import Accident, CrashEvent, ParkedVehicle, Person, Vehicle
from ninja.pagination import paginate
from django.db.models import Q
from typing import Optional
from datetime import datetime

from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404


api = NinjaAPI()

class StateSchema(Schema):
    state: int
    state__display: str

class CountySchema(Schema):
    county: int
    county__display: str

class CitySchema(Schema):
    city: int = Field(None, alias="id")
    city__display: str = Field(None, alias="name")

class DrugsSchema(Schema):
    drug_test_given: int = Field(None, alias="drug_test_type")
    drug_test_given__display: str = Field(None, alias="get_drug_test_type_display")
    drug_test_result: int = Field(None, alias="drug_test_results")

class RaceSchema(Schema):
    race: int = Field(None, alias="race")
    race__display: str = Field(None, alias="get_race_display")
    is_multiple_races: int = Field(None, alias="is_multiple_races")
    order: int = Field(None, alias="order")

class PersonRelatedFactorSchema(Schema):
    person_related_factor: int = Field(None, alias="person_related_factor")
    person_related_factor__display: str = Field(None, alias="get_person_related_factor_display")
# 
class PedestrianTypeSchema(Schema):
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
    id: int = Field(None, alias="nonmotorist_contributing_circumstance")
    contributing_cause: str = Field(None, alias="get_nonmotorist_contributing_circumstance_display")

class NonmotoristImpairedSchema(Schema):
    id: int = Field(None, alias="nonmotorist_impaired")
    impairment: str = Field(None, alias="get_nonmotorist_impaired_display")


class NonmotoristDistractedSchema(Schema):
    id: int = Field(None, alias="nonmotorist_distracted_by")
    distraction: str = Field(None, alias="get_nonmotorist_distracted_by_display")


class NonmotoristPriorActionSchema(Schema):
    id: int = Field(None, alias="nonmotorist_prior_action")
    action: str = Field(None, alias="get_nonmotorist_prior_action_display")



class NonMotoristSchema(Schema):
    vehicle_id: int = Field(0, alias='vehicle.vehicle_number')
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
    vehicle_which_struck_non_motorist_id: int = Field(None, alias="vehicle_which_struck_non_motorist.id")	
    non_motorist_device_type: int = Field(..., alias='non_motorist_device_type')	
    non_motorist_device_type__display: str = Field(..., alias='get_non_motorist_device_type_display')
    non_motorist_device_motorization: int = Field(..., alias='non_motorist_device_motorization')	
    non_motorist_device_motorization__display: str = Field(..., alias='get_non_motorist_device_motorization_display')
    non_motorist_location: int = Field(..., alias='non_motorist_location')	
    non_motorist_location__display: str = Field(..., alias='get_non_motorist_location_display')
    at_work: int = Field(..., alias='at_work')	
    at_work__display: str = Field(..., alias='get_at_work_display')
    hispanic: int = Field(..., alias='hispanic')	
    hispanic__display: str = Field(..., alias='get_hispanic_display')


    pedestrian_type: PedestrianTypeSchema = Field(None, alias='pedestriantype')
    safety_equipment: SafetyEquipmentSchema = Field(None, alias='safetyequipment')
    contributing_circumstances: List[NonmotoristContributingCircumstanceSchema] = Field(None, alias="nonmotoristcontributingcircumstance_set")
    impairments: List[NonmotoristImpairedSchema] = Field(None, alias="nonmotoristimpaired_set")
    distractions: List[NonmotoristDistractedSchema] = Field(None, alias="nonmotoristdistracted_set")
    prior_actions: List[NonmotoristPriorActionSchema] = Field(None, alias="nonmotoristprioraction_set")
    drugs: list[DrugsSchema] = Field(None, alias="drugs_set")
    race: list[RaceSchema] = Field(None, alias="race_set")
    person_related_factors: list[PersonRelatedFactorSchema] = Field(None, alias="personrelatedfactor_set")

class VehiclePersonSchema(Schema):
    id: int = Field(..., alias='person_number')
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

class ParkedVehiclePersonSchema(Schema):
    id: int = Field(..., alias='person_number')
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
    non_motorist_device_type: int = Field(..., alias='non_motorist_device_type')	
    non_motorist_device_type__display: str = Field(..., alias='get_non_motorist_device_type_display')
    non_motorist_device_motorization: int = Field(..., alias='non_motorist_device_motorization')	
    non_motorist_device_motorization__display: str = Field(..., alias='get_non_motorist_device_motorization_display')
    non_motorist_location: int = Field(..., alias='non_motorist_location')	
    non_motorist_location__display: str = Field(..., alias='get_non_motorist_location_display')
    at_work: int = Field(..., alias='at_work')	
    at_work__display: str = Field(..., alias='get_at_work_display')
    hispanic: int = Field(..., alias='hispanic')	
    hispanic__display: str = Field(..., alias='get_hispanic_display')


    drugs: list[DrugsSchema] = Field(None, alias="drugs_set")
    race: list[RaceSchema] = Field(None, alias="race_set")
    person_related_factors: list[PersonRelatedFactorSchema] = Field(None, alias="personrelatedfactor_set")

class VehicleRelatedFactorSchema(Schema):
    id: int = Field(..., alias='vehicle_related_factor')
    factor: str = Field(..., alias='get_vehicle_related_factor_display')

class DriverRelatedFactorSchema(Schema):
    id: int = Field(..., alias='driver_related_factor')
    factor: str = Field(..., alias='get_driver_related_factor_display')

class VisionSchema(Schema):
    id: int = Field(..., alias='visibility')
    vision: str = Field(..., alias='get_visibility_display')

class DamageSchema(Schema):
    id: int = Field(..., alias='area_of_impact')
    area_of_impact: str = Field(..., alias='get_area_of_impact_display')

class DriverDistractedSchema(Schema):
    id: int = Field(..., alias='distracted_by')
    distracted_by: str = Field(..., alias='get_distracted_by_display')

class DriverImpairedSchema(Schema):
    id: int = Field(..., alias='driver_impaired')
    driver_impaired: str = Field(..., alias='get_driver_impaired_display')

class VehicleFactorSchema(Schema):
    id: int = Field(..., alias='contributing_cause')
    contributing_cause: str = Field(..., alias='get_contributing_cause_display')

class ManeuverSchema(Schema):
    id: int = Field(..., alias='driver_maneuvered_to_avoid')
    name: str = Field(..., alias='get_driver_maneuvered_to_avoid_display')

class ViolationSchema(Schema):
    id: int = Field(..., alias='moving_violation')
    moving_violation: str = Field(..., alias='get_moving_violation_display')

class VehicleSchema(Schema):
    id: int = Field(None, alias='vehicle_number')
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
    vpic_make: int
    vpic_model: int
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
    trailer_vin_1: str
    trailer_vin_2: str
    trailer_vin_3: str
    trailer_weight_rating_1: int = Field(..., alias='trailer_weight_rating_1')	
    trailer_weight_rating_1__display: str = Field(..., alias='get_trailer_weight_rating_1_display')
    trailer_weight_rating_2: int = Field(..., alias='trailer_weight_rating_2')	
    trailer_weight_rating_2__display: str = Field(..., alias='get_trailer_weight_rating_2_display')
    trailer_weight_rating_3: int = Field(..., alias='trailer_weight_rating_3')	
    trailer_weight_rating_3__display: str = Field(..., alias='get_trailer_weight_rating_3_display')
    jackknife: int = Field(..., alias='jackknife')	
    jackknife__display: str = Field(..., alias='get_jackknife_display')
    motor_carrierentification_number: str
    vehicle_configuration: int = Field(..., alias='vehicle_configuration')	
    vehicle_configuration__display: str = Field(..., alias='get_vehicle_configuration_display')
    cargo_body_type: int = Field(..., alias='cargo_body_type')	
    cargo_body_type__display: str = Field(..., alias='get_cargo_body_type_display')
    hazardous_material_involvement: bool
    hazardous_material_placard: int = Field(..., alias='hazardous_material_placard')	
    hazardous_material_placard__display: str = Field(..., alias='get_hazardous_material_placard_display')
    hazardous_material: int
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
    combined_make_model: int = Field(None, alias="combined_make_model")
        
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
    previous_bac_suspensions_underage: int
    previous_bac_suspensions: int
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
    driver_impaired: List[DriverImpairedSchema] = Field(..., alias='driverimpaired_set')
    vehicle_factors: List[VehicleFactorSchema] = Field(..., alias='vehiclefactor_set')
    maneuvers: List[ManeuverSchema] = Field(..., alias='maneuver_set')
    moving_violations: List[ViolationSchema] = Field(..., alias='violation_set')
    vision: List[VisionSchema] = Field(..., alias='vision_set')

class ParkedVehicleRelatedFactorSchema(Schema):
    id: int = Field(..., alias='parked_vehicle_related_factor')
    factor: str = Field(..., alias='get_parked_vehicle_related_factor_display')


class ParkedVehicleSchema(Schema):
    id: int = Field(None, alias='vehicle_number')
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
    vpic_make: int
    vpic_model: int

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

    trailer_vin_1: str
    trailer_vin_2: str
    trailer_vin_3: str
    trailer_weight_rating_1: int = Field(..., alias='trailer_weight_rating_1')	
    trailer_weight_rating_1__display: str = Field(..., alias='get_trailer_weight_rating_1_display')
    trailer_weight_rating_2: int = Field(..., alias='trailer_weight_rating_2')	
    trailer_weight_rating_2__display: str = Field(..., alias='get_trailer_weight_rating_2_display')
    trailer_weight_rating_3: int = Field(..., alias='trailer_weight_rating_3')	
    trailer_weight_rating_3__display: str = Field(..., alias='get_trailer_weight_rating_3_display')
    motor_carrierentification_number: str
    vehicle_configuration: int = Field(..., alias='vehicle_configuration')	
    vehicle_configuration__display: str = Field(..., alias='get_vehicle_configuration_display')
    cargo_body_type: int = Field(..., alias='cargo_body_type')	
    cargo_body_type__display: str = Field(..., alias='get_cargo_body_type_display')
    hazardous_material_involvement: bool
    hazardous_material_placard: int = Field(..., alias='hazardous_material_placard')	
    hazardous_material_placard__display: str = Field(..., alias='get_hazardous_material_placard_display')
    hazardous_material: int
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
    combined_make_model: int = Field(None, alias="combined_make_model_id")
    persons: List[ParkedVehiclePersonSchema] = Field(..., alias='person_set')
    parked_vehicle_related_factors: List[ParkedVehicleRelatedFactorSchema] = Field(..., alias='parkedvehiclerelatedfactor_set')
    number_of_occupants: int
    

class CrashEventSchema(Schema):
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
    latitude: float
    longitude: float
    number_of_vehicles: int = Field(0, alias="number_of_vehicles")
    number_of_vehicles_in_transport: int = Field(0, alias="number_of_vehicles_in_transport")
    number_of_parked_vehicles: int = Field(0, alias="number_of_parked_vehicles")
    number_of_persons_in_motor_vehicles: int = Field(0, alias="number_of_persons_in_motor_vehicles")
    number_of_persons_in_motor_vehicles_in_transport: int = Field(0, alias="number_of_persons_in_motor_vehicles_in_transport")
    number_of_persons_in_parked_vehicles: int = Field(0, alias="number_of_persons_in_parked_vehicles")
    number_of_nonmotorists: int = Field(0, alias="number_of_persons_not_in_motor_vehicles")
    number_of_persons_not_in_motor_vehicles_in_transport: int = Field(0, alias="number_of_persons_not_in_motor_vehicles_in_transport")


    trafficway_identifier_1: str
    trafficway_identifier_2: str

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
    at_intersection: int = Field(..., alias="at_intersection")
    at_intersection__display: str = Field(..., alias="get_at_intersection_display")


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

class ShortAccidentSchema(Schema):
    id: int
    st_case: int
    fatalities: int
    latitude: float
    longitude: float
    data: str



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
    combined_make_model_id: Optional[int] = None		
    fatalities: Optional[int] = None	
    fatalities__gt: Optional[int] = None	
    fatalities__lt: Optional[int] = None	



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
    weather: Optional[int] = None

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



@api.get("/accidents", response=List[AccidentSchema])
@paginate
def accidents_list(request, filters: AccidentFilterSchema = Query(...)):
    queryset = Accident.objects.order_by("st_case")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/accidents/{accident_id}", response=AccidentSchema)
def get_employee(request, accident_id: int):
    accident = get_object_or_404(Accident, id=accident_id)
    return accident



@api.get("/vehicles", response=List[VehicleSchema])
@paginate
def vehicle_list(request, filters: VehicleFilterSchema = Query(...)):
    queryset = Vehicle.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/vehicles/{vehicle_id}", response=VehicleSchema)
def get_employee(request, vehicle_id: int):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return vehicle

@api.get("/parked_vehicles", response=List[ParkedVehicleSchema])
@paginate
def parked_vehicle_list(request, filters: ParkedVehicleFilterSchema = Query(...)):
    queryset = ParkedVehicle.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/parked_vehicles/{vehicle_id}", response=ParkedVehicleSchema)
def get_employee(request, vehicle_id: int):
    vehicle = get_object_or_404(ParkedVehicle, id=vehicle_id)
    return vehicle

@api.get("/persons", response=List[NonMotoristSchema])
@paginate
def person_list(request, filters: PersonFilterSchema = Query(...)):
    queryset = Person.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/persons/{person_id}", response=NonMotoristSchema)
def get_employee(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    return person

@api.get("/crash_events", response=List[CrashEventSchema])
@paginate
def crash_event_list(request, filters: CrashEventFilterSchema = Query(...)):

    queryset = CrashEvent.objects.order_by("accident__st_case")
    if "vehicle" in request.GET and request.GET['vehicle']:
        queryset = queryset.filter(Q(vehicle_1_id=request.GET['vehicle']) | Q(vehicle_2_id=request.GET['vehicle']) | Q(parked_vehicle_1_id=request.GET['vehicle']) | Q(parked_vehicle_2_id=request.GET['vehicle']))
    queryset = filters.filter(queryset)
    return list(queryset)



@api.get("/accidents_by_location", response=List[AccidentSchema])
@paginate
def accidents_by_loction(request, filters: AccidentFilterSchema = Query(...)):
    try:
        search_location = Point(x=float(request.GET['lon']), y=float(request.GET['lat']), srid=4326)
        radius_in_miles = float(request.GET['radius'])
    except:
        return list()

    queryset = Accident.objects.annotate(
        distance=Distance('location', search_location)
    ).order_by('distance').filter(location__distance_lte=(search_location, D(mi=radius_in_miles)))

    queryset = filters.filter(queryset)
    return list(queryset)


@api.get("/accidents_by_vehicle", response=List[ShortAccidentSchema])
@paginate
def accidents_by_vehicle(request, filters: VehicleFilterSchema = Query(...)):
    queryset = Vehicle.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/hello")
def hello(request):
    return "Hello world"

