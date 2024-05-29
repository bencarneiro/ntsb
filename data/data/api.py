from ninja import NinjaAPI
from typing import List
from ninja import Schema, Field
from fatalities.models import Accident, Person, Vehicle
from ninja.pagination import paginate
from django.db.models import Q



api = NinjaAPI()

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

class VehiclePersonSchema(Schema):\
    id: int = Field(..., alias='person_number')

class ParkedVehiclePersonSchema(Schema):
    id: int = Field(..., alias='person_number')

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


class AccidentSchema(Schema):
    id: int
    st_case: int
    vehicles: List[VehicleSchema] = Field(..., alias='vehicle_set')
    parked_vehicles: List[ParkedVehicleSchema] = Field(..., alias='parkedvehicle_set')
    nonmotorists: List[NonMotoristSchema] = Field(..., alias='person_set')
    crash_events: list[CrashEventSchema] = Field(..., alias='crashevent_set')
    crash_related_factors: list[CrashRelatedFactorSchema] = Field(..., alias='crashrelatedfactors_set')
    weather: list[WeatherSchema] = Field(..., alias='weather_set')




@api.get("/accidents", response=List[AccidentSchema])
@paginate
def tasks(request):
    queryset = Accident.objects.order_by("st_case")
    return list(queryset)

@api.get("/hello")
def hello(request):
    return "Hello world"

