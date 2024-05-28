from ninja import NinjaAPI
from typing import List
from ninja import Schema, Field
from fatalities.models import Accident
from ninja.pagination import paginate



api = NinjaAPI()


class VehicleSchema(Schema):
    id: int
    vehicle_number: int

class AccidentSchema(Schema):
    id: int
    st_case: int
    vehicles: List[VehicleSchema] = Field(..., alias='vehicle_set') # ! None - to mark it as optional


@api.get("/accidents", response=List[AccidentSchema])
@paginate
def tasks(request):
    queryset = Accident.objects.order_by("st_case")
    return list(queryset)

@api.get("/hello")
def hello(request):
    return "Hello world"

