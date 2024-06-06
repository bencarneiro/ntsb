from ninja import NinjaAPI
from typing import List
from ninja import Schema, Field, FilterSchema, Query, Redoc
from .response_schemas import *
from .filter_schemas import *
from fatalities.models import *
from ninja.pagination import paginate
from django.db.models import Q
from typing import Optional, Tuple
from datetime import datetime
List
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
# from ninja import 


api = NinjaAPI(docs = Redoc(),
   openapi_extra={
       "info": {
           "termsOfService": "https://github.com/bencarneiro/ntsb",
       }
   },
   title="Roadway Report",
   description="This is a free API which returns data on ALL traffic fatalities in the USA. The database currently contains a complete dataset for 2022, and I will be importing 1975-2021 in the coming months.    Check out the [github](https://github.com/bencarneiro/ntsb)")


@api.get("/accidents", response=List[AccidentSchema])
@paginate
def accident_list(request, filters: AccidentFilterSchema = Query(...)):
    queryset = Accident.objects.order_by("id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/accidents/{accident_id}", response=AccidentSchema)
def accident_by_id(request, accident_id: int):
    accident = get_object_or_404(Accident, id=accident_id)
    return accident


@api.get("/accidents_geojson", response=list[FeatureSchema])
@paginate
def accident_list(request, filters: AccidentFilterSchema = Query(...)):
    queryset = Accident.objects.order_by("id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/test/{accident_id}", response=FeatureSchema)
def accident_by_id(request, accident_id: int):
    accident = get_object_or_404(Accident, id=accident_id)
    return accident




@api.get("/accidents_by_location", response=List[AccidentSchema])
@paginate
def accidents_by_loction(request, filters: AccidentLocationFilterSchema = Query(...)):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        return "Required Parameters are lat, lon, radius"
    try:
        search_location = Point(x=float(request.GET['lon']), y=float(request.GET['lat']), srid=4326)
        radius_in_miles = float(request.GET['radius'])
    except:
        return list()

    queryset = Accident.objects.annotate(
        distance=Distance('location', search_location)
    ).order_by('distance').filter(location__distance_lte=(search_location, D(mi=radius_in_miles)))
    qe = filters.get_filter_expression()
    q = Q()
    for param in qe.deconstruct()[1]:
        if param[0] not in {'lat', 'lon', 'radius'}:
            q &= Q((param[0], param[1]))
    queryset = queryset.filter(q)
    return list(queryset)


@api.get("/accidents_by_vehicle", response=List[AccidentSchema])
@paginate
def accidents_by_vehicle(request, filters: VehicleFilterSchema = Query(...)):
    queryset = Vehicle.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_parked_vehicle", response=List[AccidentSchema])
@paginate
def accidents_by_parked_vehicle(request, filters: ParkedVehicleFilterSchema = Query(...)):
    queryset = ParkedVehicle.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_person", response=List[AccidentSchema])
@paginate
def accidents_by_person(request, filters: PersonFilterSchema = Query(...)):
    queryset = Person.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_crash_event", response=List[AccidentSchema])
@paginate
def accidents_by_crash_event(request, filters: CrashEventFilterSchema = Query(...)):
    queryset = CrashEvent.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_weather", response=List[AccidentSchema])
@paginate
def accidents_by_weather(request, filters: WeatherFilterSchema = Query(...)):
    queryset = Weather.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/accidents_by_crash_related_factor", response=List[AccidentSchema])
@paginate
def accidents_by_crash_related_factor(request, filters: CrashRelatedFactorFilterSchema = Query(...)):
    queryset = CrashRelatedFactors.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("accident_id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/accidents_by_damage", response=List[AccidentSchema])
@paginate
def accidents_by_crash_related_factor(request, filters: DamageFilterSchema = Query(...)):
    queryset = Damage.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/accidents_by_distraction", response=List[AccidentSchema])
@paginate
def accidents_by_distraction(request, filters: DriverDistractedFilterSchema = Query(...)):
    queryset = DriverDistracted.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)



@api.get("/accidents_by_driver_impairment", response=List[AccidentSchema])
@paginate
def accidents_by_driver_impairment(request, filters: DriverImpairedFilterSchema = Query(...)):
    queryset = DriverImpaired.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/accidents_by_vehicle_factor", response=List[AccidentSchema])
@paginate
def accidents_by_vehicle_factor(request, filters: VehicleFactorFilterSchema = Query(...)):
    queryset = VehicleFactor.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_maneuver", response=List[AccidentSchema])
@paginate
def accidents_by_maneuver(request, filters: ManeuverFilterSchema = Query(...)):
    queryset = Maneuver.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_moving_violation", response=List[AccidentSchema])
@paginate
def accidents_by_moving_violation(request, filters: ViolationFilterSchema = Query(...)):
    queryset = Violation.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/accidents_by_vision_obstruction", response=List[AccidentSchema])
@paginate
def accidents_by_vision_obstruction(request, filters: VisionFilterSchema = Query(...)):
    queryset = Vision.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/accidents_by_driver_related_factor", response=List[AccidentSchema])
@paginate
def accidents_by_driver_related_factor(request, filters: DriverRelatedFactorFilterSchema = Query(...)):
    queryset = DriverRelatedFactor.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_vehicle_related_factor", response=List[AccidentSchema])
@paginate
def accidents_by_driver_related_factor(request, filters: VehicleRelatedFactorFilterSchema = Query(...)):
    queryset = VehicleRelatedFactor.objects.order_by("vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)


@api.get("/accidents_by_parked_vehicle_related_factor", response=List[AccidentSchema])
@paginate
def accidents_by_parked_vehicle_related_factor(request, filters: ParkedVehicleRelatedFactorFilterSchema = Query(...)):
    queryset = ParkedVehicleRelatedFactor.objects.order_by("parked_vehicle__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("parked_vehicle__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_drug", response=List[AccidentSchema])
@paginate
def accidents_by_drug(request, filters: DrugsFilterSchema = Query(...)):
    queryset = Drugs.objects.order_by("person__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("person__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_race", response=List[AccidentSchema])
@paginate
def accidents_by_race(request, filters: RaceFilterSchema = Query(...)):
    queryset = Race.objects.order_by("person__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("person__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_person_related_factor", response=List[AccidentSchema])
@paginate
def accidents_by_person_related_factor(request, filters: PersonRelatedFactorFilterSchema = Query(...)):
    queryset = PersonRelatedFactor.objects.order_by("person__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("person__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_nonmotorist_contributing_circumstance", response=List[AccidentSchema])
@paginate
def accidents_by_nonmotorist_contributing_circumstance(request, filters: NonmotoristContributingCircumstanceFilterSchema = Query(...)):
    queryset = NonmotoristContributingCircumstance.objects.order_by("person__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("person__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_nonmotorist_impairment", response=List[AccidentSchema])
@paginate
def accidents_by_nonmotorist_impairment(request, filters: NonmotoristImpairedFilterSchema = Query(...)):
    queryset = NonmotoristImpaired.objects.order_by("person__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("person__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_nonmotorist_distraction", response=List[AccidentSchema])
@paginate
def accidents_by_nonmotorist_distraction(request, filters: NonmotoristDistractedFilterSchema = Query(...)):
    queryset = NonmotoristDistracted.objects.order_by("person__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("person__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)

@api.get("/accidents_by_nonmotorist_prior_action", response=List[AccidentSchema])
@paginate
def accidents_by_nonmotorist_prior_action(request, filters: NonmotoristPriorActionFilterSchema = Query(...)):
    queryset = NonmotoristPriorAction.objects.order_by("person__accident__id")
    queryset = filters.filter(queryset)
    listo = list(queryset.values_list("person__accident__id", flat=True))
    new_qs = Accident.objects.filter(id__in=listo)
    return list(new_qs)




@api.get("/vehicles", response=List[VehicleSchema])
@paginate
def vehicle_list(request, filters: VehicleFilterSchema = Query(...)):
    queryset = Vehicle.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/vehicles/{vehicle_id}", response=VehicleSchema)
def vehicle_by_id(request, vehicle_id: int):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return vehicle

@api.get("/parked_vehicles", response=List[ParkedVehicleSchema])
@paginate
def parked_vehicle_list(request, filters: ParkedVehicleFilterSchema = Query(...)):
    queryset = ParkedVehicle.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/parked_vehicles/{vehicle_id}", response=ParkedVehicleSchema)
def parked_vehicle_by_id(request, vehicle_id: int):
    parked_vehicle = get_object_or_404(ParkedVehicle, id=vehicle_id)
    return parked_vehicle

@api.get("/persons", response=List[NonMotoristSchema])
@paginate
def person_list(request, filters: PersonFilterSchema = Query(...)):
    queryset = Person.objects.order_by("accident__id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/persons/{person_id}", response=NonMotoristSchema)
def person_by_id(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    return person

@api.get("/crash_events", response=List[CrashEventSchema])
@paginate
def crash_event_list(request, filters: CrashEventFilterSchema = Query(...)):

    queryset = CrashEvent.objects.order_by("accident__id")
    if "vehicle" in request.GET and request.GET['vehicle']:
        queryset = queryset.filter(Q(vehicle_1_id=request.GET['vehicle']) | Q(vehicle_2_id=request.GET['vehicle']) | Q(parked_vehicle_1_id=request.GET['vehicle']) | Q(parked_vehicle_2_id=request.GET['vehicle']))
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/crash_events/{crash_event_id}", response=CrashEventSchema)
def crash_event_by_id(request, crash_event_id: int):
    crashevent = get_object_or_404(CrashEvent, id=crash_event_id)
    return crashevent


@api.get("/damages", response=List[DamageSchema])
@paginate
def damage_list(request, filters: DamageFilterSchema = Query(...)):
    queryset = Damage.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/damages/{damage_id}", response=DamageSchema)
def damage_by_id(request, damage_id: int):
    damage = get_object_or_404(Damage, id=damage_id)
    return damage


@api.get("/distractions", response=List[DriverDistractedSchema])
@paginate
def distraction_list(request, filters: DamageFilterSchema = Query(...)):
    queryset = DriverDistracted.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/distractions/{distraction_id}", response=DriverDistractedSchema)
def distraction_by_id(request, distraction_id: int):
    distraction = get_object_or_404(DriverDistracted, id=distraction_id)
    return distraction


@api.get("/driver_impairments", response=List[DriverImpairedSchema])
@paginate
def driver_impairment_list(request, filters: DriverImpairedFilterSchema = Query(...)):
    queryset = DriverImpaired.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/driver_impairments/{driver_impairment_id}", response=DriverImpairedSchema)
def driver_impairment_by_id(request, driver_impairment_id: int):
    impairment = get_object_or_404(DriverImpaired, id=driver_impairment_id)
    return impairment


@api.get("/vehicle_factors", response=List[VehicleFactorSchema])
@paginate
def vehicle_factor_list(request, filters: VehicleFactorFilterSchema = Query(...)):
    queryset = VehicleFactor.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/vehicle_factors/{vehicle_factor_id}", response=VehicleFactorSchema)
def vehicle_factor_by_id(request, vehicle_factor_id: int):
    factor = get_object_or_404(VehicleFactor, id=vehicle_factor_id)
    return factor



@api.get("/maneuvers", response=List[ManeuverSchema])
@paginate
def maneuver_list(request, filters: ManeuverFilterSchema = Query(...)):
    queryset = Maneuver.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/maneuvers/{maneuver_id}", response=ManeuverSchema)
def maneuver_by_id(request, maneuver_id: int):
    maneuver = get_object_or_404(Maneuver, id=maneuver_id)
    return maneuver



@api.get("/moving_violations", response=List[ViolationSchema])
@paginate
def moving_violation_list(request, filters: ViolationFilterSchema = Query(...)):
    queryset = Violation.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/moving_violations/{moving_violation_id}", response=ViolationSchema)
def moving_violation_by_id(request, moving_violation_id: int):
    violation = get_object_or_404(Violation, id=moving_violation_id)
    return violation


@api.get("/vision_obstructions", response=List[VisionSchema])
@paginate
def vision_obstruction_list(request, filters: VisionFilterSchema = Query(...)):
    queryset = Vision.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/vision_obstructions/{vision_obstruction_id}", response=VisionSchema)
def vision_obstruction_by_id(request, vision_obstruction_id: int):
    vision = get_object_or_404(Vision, id=vision_obstruction_id)
    return vision



@api.get("/vehicle_related_factors", response=List[VehicleRelatedFactorSchema])
@paginate
def vehicle_related_factor_list(request, filters: VehicleRelatedFactorFilterSchema = Query(...)):
    queryset = VehicleRelatedFactor.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/vehicle_related_factors/{vehicle_related_factor_id}", response=VehicleRelatedFactorSchema)
def vehicle_related_factor_by_id(request, vehicle_related_factor_id: int):
    vrf = get_object_or_404(VehicleRelatedFactor, id=vehicle_related_factor_id)
    return vrf




@api.get("/driver_related_factors", response=List[DriverRelatedFactorSchema])
@paginate
def driver_related_factor_list(request, filters: DriverRelatedFactorFilterSchema = Query(...)):
    queryset = DriverRelatedFactor.objects.order_by("vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/driver_related_factors/{driver_related_factor_id}", response=DriverRelatedFactorSchema)
def driver_related_factor_by_id(request, driver_related_factor_id: int):
    drf = get_object_or_404(DriverRelatedFactor, id=driver_related_factor_id)
    return drf


@api.get("/parked_vehicle_related_factors", response=List[ParkedVehicleRelatedFactorSchema])
@paginate
def parked_vehicle_related_factor_list(request, filters: ParkedVehicleRelatedFactorFilterSchema = Query(...)):
    queryset = ParkedVehicleRelatedFactor.objects.order_by("parked_vehicle__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/parked_vehicle_related_factors/{parked_vehicle_related_factor_id}", response=ParkedVehicleRelatedFactorSchema)
def parked_vehicle_related_factor_by_id(request, parked_vehicle_related_factor_id: int):
    vrf = get_object_or_404(ParkedVehicleRelatedFactor, id=parked_vehicle_related_factor_id)
    return vrf



@api.get("/drugs", response=List[DrugsSchema])
@paginate
def drugs_list(request, filters: DrugsFilterSchema = Query(...)):
    queryset = Drugs.objects.order_by("person__accident__id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/drugs/{drugs_id}", response=DrugsSchema)
def drugs_by_id(request, drugs_id: int):
    drugs = get_object_or_404(Drugs, id=drugs_id)
    return drugs

@api.get("/race", response=List[RaceSchema])
@paginate
def race_list(request, filters: RaceFilterSchema = Query(...)):
    queryset = Race.objects.order_by("person__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/race/{race_id}", response=RaceSchema)
def race_by_id(request, race_id: int):
    race = get_object_or_404(Race, id=race_id)
    return race


@api.get("/person_related_factors", response=List[PersonRelatedFactorSchema])
@paginate
def person_related_factor_list(request, filters: PersonRelatedFactorFilterSchema = Query(...)):
    queryset = PersonRelatedFactor.objects.order_by("person__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/person_related_factors/{person_related_factor_id}", response=PersonRelatedFactorSchema)
def person_related_factor_by_id(request, person_related_factor_id: int):
    prf = get_object_or_404(PersonRelatedFactor, id=person_related_factor_id)
    return prf



@api.get("/nonmotorist_impairments", response=List[NonmotoristImpairedSchema])
@paginate
def nonmotorist_impairment_list(request, filters: NonmotoristImpairedFilterSchema = Query(...)):
    queryset = NonmotoristImpaired.objects.order_by("person__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/nonmotorist_impairments/{nonmotorist_impairment_id}", response=NonmotoristImpairedSchema)
def nonmotorist_impairment_by_id(request, nonmotorist_impairment_id: int):
    nmimpair = get_object_or_404(NonmotoristImpaired, id=nonmotorist_impairment_id)
    return nmimpair



@api.get("/nonmotorist_prior_actions", response=List[NonmotoristPriorActionSchema])
@paginate
def nonmotorist_prior_action_list(request, filters: NonmotoristPriorActionFilterSchema = Query(...)):
    queryset = NonmotoristPriorAction.objects.order_by("person__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/nonmotorist_prior_actions/{nonmotorist_prior_action_id}", response=NonmotoristPriorActionSchema)
def nonmotorist_prior_action_by_id(request, nonmotorist_prior_action_id: int):
    nmprior = get_object_or_404(NonmotoristPriorAction, id=nonmotorist_prior_action_id)
    return nmprior



@api.get("/nonmotorist_contributing_circumstances", response=List[NonmotoristContributingCircumstanceSchema])
@paginate
def nonmotorist_contributing_circumstance_list(request, filters: NonmotoristContributingCircumstanceFilterSchema = Query(...)):
    queryset = NonmotoristContributingCircumstance.objects.order_by("person__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/nonmotorist_contributing_circumstances/{nonmotorist_contributing_circumstance_id}", response=NonmotoristContributingCircumstanceSchema)
def nonmotorist_contributing_circumstance_by_id(request, nonmotorist_contributing_circumstance_id: int):
    nmcc = get_object_or_404(NonmotoristContributingCircumstance, id=nonmotorist_contributing_circumstance_id)
    return nmcc


@api.get("/nonmotorist_distractions", response=List[NonmotoristDistractedSchema])
@paginate
def nonmotorist_distraction_list(request, filters: NonmotoristDistractedFilterSchema = Query(...)):
    queryset = NonmotoristDistracted.objects.order_by("person__accident_id")
    queryset = filters.filter(queryset)
    return list(queryset)

@api.get("/nonmotorist_distractions/{nonmotorist_distraction_id}", response=NonmotoristDistractedSchema)
def nonmotorist_distraction_by_id(request, nonmotorist_distraction_id: int):
    nmdistract = get_object_or_404(NonmotoristDistracted, id=nonmotorist_distraction_id)
    return nmdistract




### CHOICES ENDPOINTS BELOW



## ACCIDENT ACCIDENT ACCIDENT

@api.get("/month_choices", response=List[Tuple])
def month_choices(request):
    return list(Accident.month_choices)
    

@api.get("/day_of_the_week_choices", response=List[Tuple])
def day_of_the_week_choices(request):
    return list(Accident.day_of_the_week_choices)
    

@api.get("/route_signing_choices", response=List[Tuple])
def route_signing_choices(request):
    return list(Accident.route_signing_choices)
    

@api.get("/rural_urban_choices", response=List[Tuple])
def rural_urban_choices(request):
    return list(Accident.rural_urban_choices)
    

@api.get("/functional_system_choices", response=List[Tuple])
def functional_system_choices(request):
    return list(Accident.functional_system_choices)
    

@api.get("/road_owner_choices", response=List[Tuple])
def road_owner_choices(request):
    return list(Accident.road_owner_choices)
    

@api.get("/national_highway_system_choices", response=List[Tuple])
def national_highway_system_choices(request):
    return list(Accident.national_highway_system_choices)
    

@api.get("/special_jurisdiction_choices", response=List[Tuple])
def special_jurisdiction_choices(request):
    return list(Accident.special_jurisdiction_choices)
    

@api.get("/first_harmful_event_choices", response=List[Tuple])
def first_harmful_event_choices(request):
    return list(Accident.first_harmful_event_choices)
    

@api.get("/manner_of_collision_of_first_harmful_event_choices", response=List[Tuple])
def manner_of_collision_of_first_harmful_event_choices(request):
    return list(Accident.manner_of_collision_of_first_harmful_event_choices)
    

@api.get("/at_intersection_choices", response=List[Tuple])
def at_intersection_choices(request):
    return list(Accident.at_intersection_choices)
    

@api.get("/relation_to_junction_choices", response=List[Tuple])
def relation_to_junction_choices(request):
    return list(Accident.relation_to_junction_choices)
    

@api.get("/type_of_intersection_choices", response=List[Tuple])
def type_of_intersection_choices(request):
    return list(Accident.type_of_intersection_choices)
    

@api.get("/relation_to_road_choices", response=List[Tuple])
def relation_to_road_choices(request):
    return list(Accident.relation_to_road_choices)
    

@api.get("/work_zone_choices", response=List[Tuple])
def work_zone_choices(request):
    return list(Accident.work_zone_choices)
    

@api.get("/light_condition_choices", response=List[Tuple])
def light_condition_choices(request):
    return list(Accident.light_condition_choices)
    

@api.get("/atmospheric_condition_choices", response=List[Tuple])
def atmospheric_condition_choices(request):
    return list(Accident.atmospheric_condition_choices)
    


    
### VEHICLE VEHICLE VEHICLE

@api.get("/hit_and_run_choices", response=List[Tuple])
def hit_and_run_choices(request):
    return list(Vehicle.hit_and_run_choices)
    

@api.get("/registration_state_choices", response=List[Tuple])
def registration_state_choices(request):
    return list(Vehicle.registration_state_choices)
    

@api.get("/registered_vehicle_owner_choices", response=List[Tuple])
def registered_vehicle_owner_choices(request):
    return list(Vehicle.registered_vehicle_owner_choices)
    

@api.get("/vpic_body_class_choices", response=List[Tuple])
def vpic_body_class_choices(request):
    return list(Vehicle.vpic_body_class_choices)
    

@api.get("/ncsa_make_choices", response=List[Tuple])
def ncsa_make_choices(request):
    return list(Vehicle.ncsa_make_choices)
    

@api.get("/body_type_choices", response=List[Tuple])
def body_type_choices(request):
    return list(Vehicle.body_type_choices)
    

@api.get("/final_stage_body_class_choices", response=List[Tuple])
def final_stage_body_class_choices(request):
    return list(Vehicle.final_stage_body_class_choices)
    

@api.get("/weight_rating_choices", response=List[Tuple])
def weight_rating_choices(request):
    return list(Vehicle.weight_rating_choices)
    

@api.get("/vehicle_trailing_choices", response=List[Tuple])
def vehicle_trailing_choices(request):
    return list(Vehicle.vehicle_trailing_choices)
    

@api.get("/trailer_weight_rating_choices", response=List[Tuple])
def trailer_weight_rating_choices(request):
    return list(Vehicle.trailer_weight_rating_choices)
    

@api.get("/jackknife_choices", response=List[Tuple])
def jackknife_choices(request):
    return list(Vehicle.jackknife_choices)
    

@api.get("/vehicle_configuration_choices", response=List[Tuple])
def vehicle_configuration_choices(request):
    return list(Vehicle.vehicle_configuration_choices)
    

@api.get("/cargo_body_type_choices", response=List[Tuple])
def cargo_body_type_choices(request):
    return list(Vehicle.cargo_body_type_choices)
    

@api.get("/placard_choices", response=List[Tuple])
def placard_choices(request):
    return list(Vehicle.placard_choices)
    

@api.get("/hazardous_material_class_number_choices", response=List[Tuple])
def hazardous_material_class_number_choices(request):
    return list(Vehicle.hazardous_material_class_number_choices)
    

@api.get("/release_of_hazardous_material_choices", response=List[Tuple])
def release_of_hazardous_material_choices(request):
    return list(Vehicle.release_of_hazardous_material_choices)
    

@api.get("/bus_use_choices", response=List[Tuple])
def bus_use_choices(request):
    return list(Vehicle.bus_use_choices)
    

@api.get("/special_vehicle_use_choices", response=List[Tuple])
def special_vehicle_use_choices(request):
    return list(Vehicle.special_vehicle_use_choices)
    

@api.get("/emergency_vehicle_use_choices", response=List[Tuple])
def emergency_vehicle_use_choices(request):
    return list(Vehicle.emergency_vehicle_use_choices)
    

@api.get("/underride_override_choices", response=List[Tuple])
def underride_override_choices(request):
    return list(Vehicle.underride_override_choices)
    

@api.get("/rollover_choices", response=List[Tuple])
def rollover_choices(request):
    return list(Vehicle.rollover_choices)
    

@api.get("/rollover_location_choices", response=List[Tuple])
def rollover_location_choices(request):
    return list(Vehicle.rollover_location_choices)
    

@api.get("/initial_contact_point_choices", response=List[Tuple])
def initial_contact_point_choices(request):
    return list(Vehicle.initial_contact_point_choices)
    

@api.get("/extent_of_damage_choices", response=List[Tuple])
def extent_of_damage_choices(request):
    return list(Vehicle.extent_of_damage_choices)
    

@api.get("/vehicle_towed_choices", response=List[Tuple])
def vehicle_towed_choices(request):
    return list(Vehicle.vehicle_towed_choices)
    

@api.get("/most_harmful_event_choices", response=List[Tuple])
def most_harmful_event_choices(request):
    return list(Vehicle.most_harmful_event_choices)
    

@api.get("/automated_driving_system_present_choices", response=List[Tuple])
def automated_driving_system_present_choices(request):
    return list(Vehicle.automated_driving_system_present_choices)
    

@api.get("/automated_driving_system_level_choices", response=List[Tuple])
def automated_driving_system_level_choices(request):
    return list(Vehicle.automated_driving_system_level_choices)
    

@api.get("/automated_driving_system_engaged_choices", response=List[Tuple])
def automated_driving_system_engaged_choices(request):
    return list(Vehicle.automated_driving_system_engaged_choices)
    

@api.get("/driver_drinking_choices", response=List[Tuple])
def driver_drinking_choices(request):
    return list(Vehicle.driver_drinking_choices)
    

@api.get("/driver_present_choices", response=List[Tuple])
def driver_present_choices(request):
    return list(Vehicle.driver_present_choices)
    

@api.get("/drivers_license_state_choices", response=List[Tuple])
def drivers_license_state_choices(request):
    return list(Vehicle.drivers_license_state_choices)
    

@api.get("/non_cdl_license_type_choices", response=List[Tuple])
def non_cdl_license_type_choices(request):
    return list(Vehicle.non_cdl_license_type_choices)
    

@api.get("/non_cdl_license_status_choices", response=List[Tuple])
def non_cdl_license_status_choices(request):
    return list(Vehicle.non_cdl_license_status_choices)
    

@api.get("/cdl_license_status_choices", response=List[Tuple])
def cdl_license_status_choices(request):
    return list(Vehicle.cdl_license_status_choices)
    

@api.get("/cdl_endorsements_choices", response=List[Tuple])
def cdl_endorsements_choices(request):
    return list(Vehicle.cdl_endorsements_choices)
    

@api.get("/license_compliance_with_class_of_vehicle_choices", response=List[Tuple])
def license_compliance_with_class_of_vehicle_choices(request):
    return list(Vehicle.license_compliance_with_class_of_vehicle_choices)
    

@api.get("/compliance_with_license_restrictions_choices", response=List[Tuple])
def compliance_with_license_restrictions_choices(request):
    return list(Vehicle.compliance_with_license_restrictions_choices)
    

@api.get("/month_of_oldest_violation_choices", response=List[Tuple])
def month_of_oldest_violation_choices(request):
    return list(Vehicle.month_of_oldest_violation_choices)
    

@api.get("/speeding_related_choices", response=List[Tuple])
def speeding_related_choices(request):
    return list(Vehicle.speeding_related_choices)
    

@api.get("/trafficway_description_choices", response=List[Tuple])
def trafficway_description_choices(request):
    return list(Vehicle.trafficway_description_choices)
    

@api.get("/total_lanes_in_roadway_choices", response=List[Tuple])
def total_lanes_in_roadway_choices(request):
    return list(Vehicle.total_lanes_in_roadway_choices)
    

@api.get("/roadway_alignment_choices", response=List[Tuple])
def roadway_alignment_choices(request):
    return list(Vehicle.roadway_alignment_choices)
    

@api.get("/roadway_grade_choices", response=List[Tuple])
def roadway_grade_choices(request):
    return list(Vehicle.roadway_grade_choices)
    

@api.get("/roadway_surface_type_choices", response=List[Tuple])
def roadway_surface_type_choices(request):
    return list(Vehicle.roadway_surface_type_choices)
    

@api.get("/roadway_surface_condition_choices", response=List[Tuple])
def roadway_surface_condition_choices(request):
    return list(Vehicle.roadway_surface_condition_choices)
    

@api.get("/traffic_control_device_choices", response=List[Tuple])
def traffic_control_device_choices(request):
    return list(Vehicle.traffic_control_device_choices)
    

@api.get("/traffic_control_device_functioning_choices", response=List[Tuple])
def traffic_control_device_functioning_choices(request):
    return list(Vehicle.traffic_control_device_functioning_choices)
    

@api.get("/pre_event_movement_choices", response=List[Tuple])
def pre_event_movement_choices(request):
    return list(Vehicle.pre_event_movement_choices)
    

@api.get("/critical_precrash_event_choices", response=List[Tuple])
def critical_precrash_event_choices(request):
    return list(Vehicle.critical_precrash_event_choices)
    

@api.get("/attempted_avoidance_maneuver_choices", response=List[Tuple])
def attempted_avoidance_maneuver_choices(request):
    return list(Vehicle.attempted_avoidance_maneuver_choices)
    

@api.get("/precrash_stability_choices", response=List[Tuple])
def precrash_stability_choices(request):
    return list(Vehicle.precrash_stability_choices)
    

@api.get("/preimpact_location_choices", response=List[Tuple])
def preimpact_location_choices(request):
    return list(Vehicle.preimpact_location_choices)
    

@api.get("/crash_type_choices", response=List[Tuple])
def crash_type_choices(request):
    return list(Vehicle.crash_type_choices)
    



### PERSON PERSON PERSON

@api.get("/sex_choices", response=List[Tuple])
def sex_choices(request):
    return list(Person.sex_choices)
    

@api.get("/person_type_choices", response=List[Tuple])
def person_type_choices(request):
    return list(Person.person_type_choices)
    

@api.get("/injury_severity_choices", response=List[Tuple])
def injury_severity_choices(request):
    return list(Person.injury_severity_choices)
    

@api.get("/seating_position_choices", response=List[Tuple])
def seating_position_choices(request):
    return list(Person.seating_position_choices)
    

@api.get("/restraint_system_use_choices", response=List[Tuple])
def restraint_system_use_choices(request):
    return list(Person.restraint_system_use_choices)
    

@api.get("/restraint_system_misuse_choices", response=List[Tuple])
def restraint_system_misuse_choices(request):
    return list(Person.restraint_system_misuse_choices)
    

@api.get("/helmet_use_choices", response=List[Tuple])
def helmet_use_choices(request):
    return list(Person.helmet_use_choices)
    

@api.get("/airbag_deployed_choices", response=List[Tuple])
def airbag_deployed_choices(request):
    return list(Person.airbag_deployed_choices)
    

@api.get("/ejection_choices", response=List[Tuple])
def ejection_choices(request):
    return list(Person.ejection_choices)
    

@api.get("/ejection_path_choices", response=List[Tuple])
def ejection_path_choices(request):
    return list(Person.ejection_path_choices)
    

@api.get("/extrication_choices", response=List[Tuple])
def extrication_choices(request):
    return list(Person.extrication_choices)
    

@api.get("/police_reported_alcohol_involvement_choices", response=List[Tuple])
def police_reported_alcohol_involvement_choices(request):
    return list(Person.police_reported_alcohol_involvement_choices)
    

@api.get("/alcohol_test_given_choices", response=List[Tuple])
def alcohol_test_given_choices(request):
    return list(Person.alcohol_test_given_choices)
    

@api.get("/alcohol_test_type_choices", response=List[Tuple])
def alcohol_test_type_choices(request):
    return list(Person.alcohol_test_type_choices)
    

@api.get("/police_reported_drug_involvement_choices", response=List[Tuple])
def police_reported_drug_involvement_choices(request):
    return list(Person.police_reported_drug_involvement_choices)
    

@api.get("/drug_tested_choices", response=List[Tuple])
def drug_tested_choices(request):
    return list(Person.drug_tested_choices)
    

@api.get("/transported_to_medical_facility_by_choices", response=List[Tuple])
def transported_to_medical_facility_by_choices(request):
    return list(Person.transported_to_medical_facility_by_choices)
    

@api.get("/died_en_route_choices", response=List[Tuple])
def died_en_route_choices(request):
    return list(Person.died_en_route_choices)
    

@api.get("/month_of_death_choices", response=List[Tuple])
def month_of_death_choices(request):
    return list(Person.month_of_death_choices)
    

@api.get("/non_motorist_device_type_choices", response=List[Tuple])
def non_motorist_device_type_choices(request):
    return list(Person.non_motorist_device_type_choices)
    

@api.get("/non_motorist_device_motorization_choices", response=List[Tuple])
def non_motorist_device_motorization_choices(request):
    return list(Person.non_motorist_device_motorization_choices)
    

@api.get("/non_motorist_location_choices", response=List[Tuple])
def non_motorist_location_choices(request):
    return list(Person.non_motorist_location_choices)
    

@api.get("/at_work_choices", response=List[Tuple])
def at_work_choices(request):
    return list(Person.at_work_choices)
    

@api.get("/hispanic_choices", response=List[Tuple])
def hispanic_choices(request):
    return list(Person.hispanic_choices)


#### OTHER OTHER OTHER



@api.get("/sequence_of_events_choices", response=List[Tuple])
def sequence_of_events_choices(request):
    return list(CrashEvent.sequence_of_events_choices)
    

@api.get("/area_of_impact_choices", response=List[Tuple])
def area_of_impact_choices(request):
    return list(CrashEvent.area_of_impact_choices)
    

@api.get("/crash_related_factor_choices", response=List[Tuple])
def crash_related_factor_choices(request):
    return list(CrashRelatedFactors.crash_related_factor_choices)
    


@api.get("/parked_vehicle_related_factor_choices", response=List[Tuple])
def parked_vehicle_related_factor_choices(request):
    return list(ParkedVehicleRelatedFactor.parked_vehicle_related_factor_choices)
    

@api.get("/vehicle_related_factor_choices", response=List[Tuple])
def vehicle_related_factor_choices(request):
    return list(VehicleRelatedFactor.vehicle_related_factor_choices)
    
@api.get("/driver_related_factor_choices", response=List[Tuple])
def driver_related_factor_choices(request):
    return list(DriverRelatedFactor.driver_related_factor_choices)
    

@api.get("/distracted_by_choices", response=List[Tuple])
def distracted_by_choices(request):
    return list(DriverDistracted.distracted_by_choices)
    

@api.get("/driver_impaired_choices", response=List[Tuple])
def driver_impaired_choices(request):
    return list(DriverImpaired.driver_impaired_choices)
    

@api.get("/driver_maneuvered_to_avoid_choices", response=List[Tuple])
def driver_maneuvered_to_avoid_choices(request):
    return list(Maneuver.driver_maneuvered_to_avoid_choices)
    

@api.get("/contributing_cause_choices", response=List[Tuple])
def contributing_cause_choices(request):
    return list(VehicleFactor.contributing_cause_choices)
    

@api.get("/moving_violation_choices", response=List[Tuple])
def moving_violation_choices(request):
    return list(Violation.moving_violation_choices)
    

@api.get("/visibility_choices", response=List[Tuple])
def visibility_choices(request):
    return list(Vision.visibility_choices)


@api.get("/person_related_factor_choices", response=List[Tuple])
def person_related_factor_choices(request):
    return list(PersonRelatedFactor.person_related_factor_choices)
    

@api.get("/race_choices", response=List[Tuple])
def race_choices(request):
    return list(Race.race_choices)
    

@api.get("/drug_test_type_choices", response=List[Tuple])
def drug_test_type_choices(request):
    return list(Drugs.drug_test_type_choices)
    

@api.get("/nonmotorist_contributing_circumstance_choices", response=List[Tuple])
def nonmotorist_contributing_circumstance_choices(request):
    return list(NonmotoristContributingCircumstance.nonmotorist_contributing_circumstance_choices)
    

@api.get("/nonmotorist_distracted_by_choices", response=List[Tuple])
def nonmotorist_distracted_by_choices(request):
    return list(NonmotoristDistracted.nonmotorist_distracted_by_choices)
    

@api.get("/nonmotorist_impaired_choices", response=List[Tuple])
def nonmotorist_impaired_choices(request):
    return list(NonmotoristImpaired.nonmotorist_impaired_choices)
    

@api.get("/nonmotorist_prior_action_choices", response=List[Tuple])
def nonmotorist_prior_action_choices(request):
    return list(NonmotoristPriorAction.nonmotorist_prior_action_choices)
    

@api.get("/helmet_choices", response=List[Tuple])
def helmet_choices(request):
    return list(SafetyEquipment.safety_equipment_choices)


@api.get("/pads_choices", response=List[Tuple])
def pads_choices(request):
    return list(SafetyEquipment.safety_equipment_choices)


@api.get("/other_protective_equipment_choices", response=List[Tuple])
def other_protective_equipment_choices(request):
    return list(SafetyEquipment.safety_equipment_choices)


@api.get("/other_preventative_equipment_choices", response=List[Tuple])
def other_preventative_equipment_choices(request):
    return list(SafetyEquipment.safety_equipment_choices)


@api.get("/lights_choices", response=List[Tuple])
def lights_choices(request):
    return list(SafetyEquipment.safety_equipment_choices)



@api.get("/reflective_equipment_choices", response=List[Tuple])
def reflective_equipment_choices(request):
    return list(SafetyEquipment.safety_equipment_choices)

@api.get("/safety_equipment_choices", response=List[Tuple])
def safety_equipment_choices(request):
    return list(SafetyEquipment.safety_equipment_choices)
    
@api.get("/marked_crosswalk_present_choices", response=List[Tuple])
def marked_crosswalk_present_choices(request):
    return list(PedestrianType.marked_crosswalk_present_choices)
    

@api.get("/sidewalk_present_choices", response=List[Tuple])
def sidewalk_present_choices(request):
    return list(PedestrianType.sidewalk_present_choices)
    

@api.get("/in_school_zone_choices", response=List[Tuple])
def in_school_zone_choices(request):
    return list(PedestrianType.in_school_zone_choices)
    

@api.get("/pedestrian_crash_type_choices", response=List[Tuple])
def pedestrian_crash_type_choices(request):
    return list(PedestrianType.pedestrian_crash_type_choices)
    

@api.get("/bicycle_crash_type_choices", response=List[Tuple])
def bicycle_crash_type_choices(request):
    return list(PedestrianType.bicycle_crash_type_choices)
    

@api.get("/pedestrian_location_choices", response=List[Tuple])
def pedestrian_location_choices(request):
    return list(PedestrianType.pedestrian_location_choices)
    

@api.get("/bicycle_location_choices", response=List[Tuple])
def bicycle_location_choices(request):
    return list(PedestrianType.bicycle_location_choices)
    

@api.get("/pedestrian_position_choices", response=List[Tuple])
def pedestrian_position_choices(request):
    return list(PedestrianType.pedestrian_position_choices)
    

@api.get("/bicycle_position_choices", response=List[Tuple])
def bicycle_position_choices(request):
    return list(PedestrianType.bicycle_position_choices)
    

@api.get("/pedestrian_direction_choices", response=List[Tuple])
def pedestrian_direction_choices(request):
    return list(PedestrianType.pedestrian_direction_choices)
    

@api.get("/bicycle_direction_choices", response=List[Tuple])
def bicycle_direction_choices(request):
    return list(PedestrianType.bicycle_direction_choices)
    

@api.get("/motorist_direction_choices", response=List[Tuple])
def motorist_direction_choices(request):
    return list(PedestrianType.motorist_direction_choices)
    

@api.get("/motorist_maneuver_choices", response=List[Tuple])
def motorist_maneuver_choices(request):
    return list(PedestrianType.motorist_maneuver_choices)
    

@api.get("/intersection_leg_choices", response=List[Tuple])
def intersection_leg_choices(request):
    return list(PedestrianType.intersection_leg_choices)
    

@api.get("/pedestrian_scenario_choices", response=List[Tuple])
def pedestrian_scenario_choices(request):
    return list(PedestrianType.pedestrian_scenario_choices)
    

@api.get("/pedestrian_crash_group_choices", response=List[Tuple])
def pedestrian_crash_group_choices(request):
    return list(PedestrianType.pedestrian_crash_group_choices)
    

@api.get("/bike_crash_group_choices", response=List[Tuple])
def bike_crash_group_choices(request):
    return list(PedestrianType.bike_crash_group_choices)