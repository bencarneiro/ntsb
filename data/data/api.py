from ninja import NinjaAPI
from typing import List
from ninja import Schema, Field
from fatalities.models import Accident, Person, Vehicle
from ninja.pagination import paginate
from django.db.models import Q



api = NinjaAPI()

class StateSchema(Schema):
    id: int
    name: str

class CountySchema(Schema):
    id: int
    name: str

class DrugsSchema(Schema):
    id: int = Field(None, alias="drug_test_type")
    drug_test_given: str = Field(None, alias="get_drug_test_type_display")
    drug_test_result: int = Field(None, alias="drug_test_results")

class RaceSchema(Schema):
    id: int = Field(None, alias="race")
    race: str = Field(None, alias="get_race_display")
    is_multiple_races: int = Field(None, alias="is_multiple_races")
    order: int = Field(None, alias="order")

class PersonRelatedFactorSchema(Schema):
    id: int = Field(None, alias="person_related_factor")
    factor: str = Field(None, alias="get_person_related_factor_display")
# 
class PedestrianTypeSchema(Schema):
    person_type_id: int = Field(None, alias='person_type')
    person_type: str = Field(None, alias='get_person_type_diplay')

class SafetyEquipmentSchema(Schema): 
    helmet: str = Field(None, alias='get_helmet_display')
    helmet_id: int = Field(None, alias='helmet')
    pads: str = Field(None, alias='get_pads_display')
    pads_id: int = Field(None, alias='pads')

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
    id: int = Field(..., alias='person_number')
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
    drugs: list[DrugsSchema] = Field(None, alias="drugs_set")
    race: list[RaceSchema] = Field(None, alias="race_set")
    person_related_factors: list[PersonRelatedFactorSchema] = Field(None, alias="personrelatedfactor_set")

class ParkedVehiclePersonSchema(Schema):
    id: int = Field(..., alias='person_number')
    drugs: list[DrugsSchema] = Field(None, alias="drugs_set")
    race: list[RaceSchema] = Field(None, alias="race_set")
    person_related_factors: list[PersonRelatedFactorSchema] = Field(None, alias="personrelatedfactor_set")

class VehicleRelatedFactorSchema(Schema):
    id: int = Field(..., alias='vehicle_related_factor')
    factor: str = Field(..., alias='get_vehicle_related_factor_display')

class DriverRelatedFactorSchema(Schema):
    id: int = Field(..., alias='driver_related_factor')
    factor: str = Field(..., alias='get_driver_related_factor_display')
    
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
    persons: List[VehiclePersonSchema] = Field(..., alias='person_set')
    vehicle_related_factors: List[VehicleRelatedFactorSchema] = Field(..., alias='vehiclerelatedfactor_set')
    driver_related_factors: List[DriverRelatedFactorSchema] = Field(..., alias='driverrelatedfactor_set')
    damages: List[DamageSchema] = Field(..., alias='damage_set')
    distractions: List[DriverDistractedSchema] = Field(..., alias='driverdistracted_set')
    driver_impaired: List[DriverImpairedSchema] = Field(..., alias='driverimpaired_set')
    vehicle_factors: List[VehicleFactorSchema] = Field(..., alias='vehiclefactor_set')
    maneuvers: List[ManeuverSchema] = Field(..., alias='maneuver_set')
    moving_violations: List[ViolationSchema] = Field(..., alias='violation_set')


class ParkedVehicleRelatedFactorSchema(Schema):
    id: int = Field(..., alias='parked_vehicle_related_factor')
    factor: str = Field(..., alias='get_parked_vehicle_related_factor_display')

class ParkedVehicleSchema(Schema):
    id: int = Field(None, alias='vehicle_number')
    persons: List[ParkedVehiclePersonSchema] = Field(..., alias='person_set')
    parked_vehicle_related_factors: List[ParkedVehicleRelatedFactorSchema] = Field(..., alias='parkedvehiclerelatedfactor_set')

class CrashEventSchema(Schema):
    crash_event_number: int
    vehicle_1: int = Field(None, alias='vehicle_1.vehicle_number')
    parked_vehicle_1: int = Field(None, alias='parked_vehicle_1.vehicle_number')
    vehicle_2: int = Field(None, alias='vehicle_2.vehicle_number')
    parked_vehicle_2: int = Field(None, alias='parked_vehicle_2.vehicle_number')
    area_of_impact_1: int
    area_of_impact_1_display: str = Field(..., alias='get_area_of_impact_1_display')
    sequence_of_events: int
    sequence_of_events_display: str =  Field(..., alias='get_sequence_of_events_display')
    area_of_impact_2: int
    area_of_impact_2_display: str = Field(..., alias='get_area_of_impact_1_display')
    

class CrashRelatedFactorSchema(Schema):

    id: int = Field(..., alias='crash_related_factor')
    factor: str = Field(..., alias='get_crash_related_factor_display')


class WeatherSchema(Schema):

    id: int = Field(..., alias='atmospheric_condition')
    weather: str = Field(..., alias='get_atmospheric_condition_display')

# class RouteSigningSchema(Schema):


class AccidentSchema(Schema):
    st_case: int
    fatalities: int
    state: StateSchema
    county: CountySchema
    number_of_vehicles: int = Field(0, alias="number_of_vehicles")
    number_of_vehicles_in_transport: int = Field(0, alias="number_of_vehicles_in_transit")
    number_of_parked_vehicles: int = Field(0, alias="number_of_parked_vehicles")
    number_of_persons_in_motor_vehicles: int = Field(0, alias="number_of_persons_in_motor_vehicles")
    number_of_persons_in_motor_vehicles_in_transport: int = Field(0, alias="number_of_persons_in_motor_vehicles_in_transport")
    number_of_nonmotorists: int = Field(0, alias="number_of_persons_not_in_motor_vehicles")
    number_of_nonmotorists_and_parkers: int = Field(0, alias="number_of_persons_not_in_motor_vehicles_in_transport")


    trafficway_identifier_1: str
    trafficway_identifier_2: str

    route_signing_id: int = Field(..., alias='route_signing')
    route_signing_name: str = Field(..., alias='get_route_signing_display')
    rural_urban_id: int = Field(..., alias='rural_urban')
    rural_urban_name: str = Field(..., alias='get_rural_urban_display')
    functional_system_id: int = Field(..., alias='functional_system')
    functional_system_name: str = Field(..., alias='get_functional_system_display')
    road_owner_id: int = Field(..., alias='road_owner')
    road_owner_name: str = Field(..., alias='get_road_owner_display')
    national_highway_system_id: int = Field(..., alias="national_highway_system")
    national_highway_system_name: str = Field(..., alias='get_national_highway_system_display')
    special_jurisdiction_id: int = Field(..., alias="special_jurisdiction")
    special_jurisdiction_name: str = Field(..., alias='get_special_jurisdiction_display')
    milepoint: int = Field(None, alias="milepoint")
    first_harmful_event_id: int = Field(..., alias="first_harmful_event")
    first_harmful_event_name: str = Field(..., alias='get_first_harmful_event_display')
    manner_of_collision_of_first_harmful_event_id: int = Field(..., alias="manner_of_collision_of_first_harmful_event")
    manner_of_collision_of_first_harmful_event_name: str = Field(..., alias="get_manner_of_collision_of_first_harmful_event_display")
    at_intersection_id: int = Field(..., alias="at_intersection")
    at_intersection_name: str = Field(..., alias="get_at_intersection_display")


    relation_to_junction_id: int = Field(..., alias="relation_to_junction")
    relation_to_junction_name: str = Field(..., alias="get_relation_to_junction_display")
    type_of_intersection_id: int = Field(..., alias="type_of_intersection")
    type_of_intersection_name: str = Field(..., alias="get_type_of_intersection_display")
    relation_to_road_id: int = Field(..., alias="relation_to_road")
    relation_to_road_name: str = Field(..., alias="get_relation_to_road_display")
    work_zone_id: int = Field(..., alias="work_zone")
    work_zone_name: str = Field(..., alias="get_work_zone_display")
    light_condition_id: int = Field(..., alias="light_condition")
    light_condition_name: str = Field(..., alias="get_light_condition_display")
    atmospheric_condition_id: int = Field(..., alias="atmospheric_condition")
    atmospheric_condition_name: str = Field(..., alias="get_atmospheric_condition_display")
    school_bus_related: bool
    rail_grade_crossing_identifier: int
    ems_notified_hour: int
    ems_notified_minute: int
    ems_arrived_hour: int
    ems_arrived_minute: int
    arrived_at_hospital_hour: int
    arrived_at_hospital_minute: int


    vehicles: List[VehicleSchema] = Field(..., alias='vehicle_set')
    parked_vehicles: List[ParkedVehicleSchema] = Field(..., alias='parkedvehicle_set')
    nonmotorists: List[NonMotoristSchema] = Field(..., alias='person_set')
    crash_events: list[CrashEventSchema] = Field(..., alias='crashevent_set')
    crash_related_factors: list[CrashRelatedFactorSchema] = Field(..., alias='crashrelatedfactors_set')
    weather: list[WeatherSchema] = Field(..., alias='weather_set')


# Extra accident fields which aren't in the schema yet
    
#  'city_id': None,
#  'month': 2,
#  'day': 4,
#  'day_of_the_week': 6,
#  'year': 2022,
#  'hour': 11,
#  'minute': None,
    
#  'latitude': Decimal('34.8465861'),
#  'longitude': Decimal('-86.5714361'),
#  'exact_location': None,
#  'exact_location_best_guess': None,
    




@api.get("/accidents", response=List[AccidentSchema])
@paginate
def tasks(request):
    queryset = Accident.objects.order_by("st_case")
    return list(queryset)

@api.get("/hello")
def hello(request):
    return "Hello world"

