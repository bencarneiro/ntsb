from ninja import NinjaAPI
from typing import List
from ninja import Schema, Field
from fatalities.models import Accident, Person, Vehicle
from ninja.pagination import paginate
from django.db.models import Q



api = NinjaAPI()


class NonMotoristSchema(Schema):
    id: int
    vehicle_number: int = Field(0, alias='vehicle.vehicle_number')
    person_number: int

class VehiclePersonSchema(Schema):
    id: int
    vehicle_number: int = Field(0, alias='vehicle.vehicle_number')
    person_number: int

class ParkedVehiclePersonSchema(Schema):
    id: int
    vehicle_number: int = Field(0, alias='parked_vehicle.vehicle_number')
    person_number: int

class VehicleSchema(Schema):
    id: int
    vehicle_number: int
    persons: List[VehiclePersonSchema] = Field(..., alias='person_set')

class ParkedVehicleSchema(Schema):
    id: int
    vehicle_number: int
    persons: List[ParkedVehiclePersonSchema] = Field(..., alias='person_set')


class AccidentSchema(Schema):
    id: int
    st_case: int
    vehicles: List[VehicleSchema] = Field(..., alias='vehicle_set')
    parked_vehicles: List[ParkedVehicleSchema] = Field(..., alias='parkedvehicle_set')
    nonmotorists: List[NonMotoristSchema] = Field(..., alias='person_set')


@api.get("/accidents", response=List[AccidentSchema])
@paginate
def tasks(request):
    queryset = Accident.objects.order_by("st_case")
    return list(queryset)

@api.get("/hello")
def hello(request):
    return "Hello world"



# 'vehicle_set': <django.db.models.fields.related_descriptors.ReverseManyToOneDescriptor at 0x75aa965d32e0>,
#               'parkedvehicle_set': <django.db.models.fields.related_descriptors.ReverseManyToOneDescriptor at 0x75aa965dffa0>,
#               'person_set': <django.db.models.fields.related_descriptors.ReverseManyToOneDescriptor at 0x75aa965ef520>,
#               'crashevent_set': <django.db.models.fields.related_descriptors.ReverseManyToOneDescriptor at 0x75aa965fca30>,
#               'crashrelatedfactors_set': <django.db.models.fields.related_descriptors.ReverseManyToOneDescriptor at 0x75aa96589ee0>,
#               'weather_set': <django.db.models.fields.related_descriptors.ReverseManyToOneDescriptor at 0x75aa965fe880>})
