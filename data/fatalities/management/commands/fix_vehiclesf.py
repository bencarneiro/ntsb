from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import VehicleRelatedFactor, ParkedVehicleRelatedFactor, PersonRelatedFactor, Vehicle, ParkedVehicle

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):

        VehicleRelatedFactor.objects.filter(vehicle_related_factor=99).update(vehicle_related_factor=999)
        ParkedVehicleRelatedFactor.objects.filter(parked_vehicle_related_factor=99).update(parked_vehicle_related_factor=999)
        PersonRelatedFactor.objects.filter(person_related_factor=99).update(person_related_factor=999)
        Vehicle.objects.filter(body_type=32).update(body_type=34)
        ParkedVehicle.objects.filter(body_type=32).update(body_type=34)