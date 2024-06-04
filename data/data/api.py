from ninja import NinjaAPI
from typing import List
from ninja import Schema, Field, FilterSchema, Query
from .response_schemas import *
from .filter_schemas import *
from fatalities.models import Accident, CrashEvent, CrashRelatedFactors, ParkedVehicle, Person, Vehicle, Weather
from ninja.pagination import paginate
from django.db.models import Q
from typing import Optional
from datetime import datetime
List
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404


api = NinjaAPI()


@api.get("/accidents", response=List[AccidentSchema])
@paginate
def accidents_list(request, filters: AccidentFilterSchema = Query(...)):
    queryset = Accident.objects.order_by("st_case")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/accidents/{accident_id}", response=AccidentSchema)
def get_accident(request, accident_id: int):
    accident = get_object_or_404(Accident, id=accident_id)
    return accident



@api.get("/vehicles", response=List[VehicleSchema])
@paginate
def vehicle_list(request, filters: VehicleFilterSchema = Query(...)):
    queryset = Vehicle.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/vehicles/{vehicle_id}", response=VehicleSchema)
def get_vehicle(request, vehicle_id: int):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return vehicle

@api.get("/parked_vehicles", response=List[ParkedVehicleSchema])
@paginate
def parked_vehicle_list(request, filters: ParkedVehicleFilterSchema = Query(...)):
    queryset = ParkedVehicle.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/parked_vehicles/{vehicle_id}", response=ParkedVehicleSchema)
def get_parked_vehicle(request, vehicle_id: int):
    vehicle = get_object_or_404(ParkedVehicle, id=vehicle_id)
    return vehicle

@api.get("/persons", response=List[NonMotoristSchema])
@paginate
def person_list(request, filters: PersonFilterSchema = Query(...)):
    queryset = Person.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/persons/{person_id}", response=NonMotoristSchema)
def get_person(request, person_id: int):
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


@api.get("/accidents_by_vehicle", response=List[AccidentSchema])
@paginate
def accidents_by_vehicle(request, filters: VehicleFilterSchema = Query(...)):
    queryset = Vehicle.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_parked_vehicle", response=List[AccidentSchema])
@paginate
def accidents_by_parked_vehicle(request, filters: ParkedVehicleFilterSchema = Query(...)):
    queryset = ParkedVehicle.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_person", response=List[AccidentSchema])
@paginate
def accidents_by_person(request, filters: PersonFilterSchema = Query(...)):
    queryset = Person.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_crash_event", response=List[AccidentSchema])
@paginate
def accidents_by_crash_event(request, filters: CrashEventFilterSchema = Query(...)):
    queryset = CrashEvent.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_weather", response=List[AccidentSchema])
@paginate
def accidents_by_weather(request, filters: WeatherFilterSchema = Query(...)):
    queryset = Weather.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/accidents_by_crash_related_factor", response=List[AccidentSchema])
@paginate
def accidents_by_weather(request, filters: CrashRelatedFactorFilterSchema = Query(...)):
    queryset = CrashRelatedFactors.objects.order_by("accident__st_case")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)



@api.get("/hello")
def hello(request):
    print(Person.__dict__)
    return list(Person.died_en_route_choices)

