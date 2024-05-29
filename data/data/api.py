from ninja import NinjaAPI
from typing import List
from ninja import Schema, Field
from fatalities.models import Accident, Person, Vehicle
from ninja.pagination import paginate
from django.db.models import Q



api = NinjaAPI()


class NonMotoristSchema(Schema):
    vehicle_id: int = Field(0, alias='vehicle.vehicle_number')
    id: int = Field(..., alias='person_number')

class VehiclePersonSchema(Schema):\
    id: int = Field(..., alias='person_number')

class ParkedVehiclePersonSchema(Schema):
    id: int = Field(..., alias='person_number')

class VehicleSchema(Schema):
    id: int = Field(None, alias='vehicle_number')
    persons: List[VehiclePersonSchema] = Field(..., alias='person_set')

class ParkedVehicleSchema(Schema):
    id: int = Field(None, alias='vehicle_number')
    persons: List[ParkedVehiclePersonSchema] = Field(..., alias='person_set')

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

