from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import FLORIDA_PATH
from datetime import datetime

def injury_severity_converter(severity):
    if severity == 'Fatal (within 30 days)':
        return 4
    if severity == 'Non-Traffic Fatality':
        return 4
    if severity == 'Incapacitating':
        return 3
    if severity == 'Non-Incapacitating':
        return 2
    if severity == 'Possible':
        return 1
    if severity == "None":
        return 0
    return 9

# Example usage:
class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=12).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=12).delete()
        InjuryAccident.objects.filter(state_id=12).delete()
        crashes_path = f"{FLORIDA_PATH}crash.csv"
        vehicle_path = f"{FLORIDA_PATH}vehicle.csv"
        person_path = f"{FLORIDA_PATH}person.csv"
        print(crashes_path)
        crashes = pd.read_csv(crashes_path)
        vehicles = pd.read_csv(vehicle_path)
        persons = pd.read_csv(person_path)
        state_id = 12
        crash_list = []
        vehicle_list = []
        person_list = []
        for x in crashes.index:
            print(f"crash #{crashes['crash_id'][x]} is a {crashes['crash_type'][x]}")
            crash_vehicles = vehicles[vehicles['crash_id']==crashes['crash_id'][x]]
            crash_persons = persons[persons['crash_id']==crashes['crash_id'][x]]
            latitude = crashes['lat'][x]
            if pd.isnull(crashes['lat'][x]):
                latitude = None
            longitude = crashes['lon'][x]
            if pd.isnull(crashes['lon'][x]):
                longitude = None
            new_injury_accident = InjuryAccident(
                state_accident_id = int(crashes['crash_id'][x]),
                dt = crashes['dt'][x],
                city = crashes['city'][x],
                county = crashes['county'][x],
                street_1 = crashes['street_1'][x],
                street_2 = crashes['street_2'][x],
                crash_type = crashes['crash_type'][x],
                death_count = crashes['death_count'][x],
                severe_injury_count = crashes['severe_injury_count'][x],
                latitude = latitude,
                longitude = longitude,
                state_id = 12
            )
            crash_list += [new_injury_accident]
            crash_vehicle_dict = {}
            for y in crash_vehicles.index:
                hit_and_run = False
                if crash_vehicles['hit_run'][y] == "Y":
                    hit_and_run = True
                new_injury_vehicle = InjuryVehicle(
                    injury_accident = new_injury_accident,
                    vehicle_number = crash_vehicles['veh_num'][y],
                    make = crash_vehicles['make'][y],
                    model = crash_vehicles['model'][y],
                    body_type = crash_vehicles['body_type'][y],
                    hit_and_run = hit_and_run
                )
                vehicle_list += [new_injury_vehicle]
                crash_vehicle_dict[crash_vehicles['veh_num'][y]] = new_injury_vehicle
            for z in crash_persons.index:
                age = crash_persons['age'][z]
                if age == "None" or pd.isnull(age):
                    age = None
                if crash_persons['veh_num'][z] == 0:
                    injury_vehicle = None
                else:
                    injury_vehicle = crash_vehicle_dict[crash_persons['veh_num'][z]]
                new_injury_person = InjuryPerson(
                    injury_accident = new_injury_accident,
                    injury_vehicle = injury_vehicle,
                    age = age,
                    sex = crash_persons['sex'][z],
                    person_type = crash_persons['person_type'][z],
                    injury_severity = injury_severity_converter(crash_persons['injury_severity'][z])
                )
                person_list += [new_injury_person]
            if x % 1000 == 0:
                InjuryAccident.objects.bulk_create(crash_list)
                InjuryVehicle.objects.bulk_create(vehicle_list)
                InjuryPerson.objects.bulk_create(person_list)
                print(f"hitting DB on crash row #{x}")
                crash_list = []
                vehicle_list = []
                person_list = []


        InjuryAccident.objects.bulk_create(crash_list)
        InjuryVehicle.objects.bulk_create(vehicle_list)
        InjuryPerson.objects.bulk_create(person_list)
        print("hitting db one last time")
            



# class InjuryAccident(models.Model):
#     id = models.AutoField(primary_key=True)
#     state = models.ForeignKey(State, on_delete= models.DO_NOTHING)
#     state_accident_id = models.DecimalField(max_digits=20, decimal_places=0)
#     dt = models.DateTimeField(null=False, blank=False)
#     latitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
#     longitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
#     city = models.TextField(null=True, blank=True)
#     county = models.TextField(null=True, blank=True)
#     street_1 = models.TextField(null=True)
#     street_2 = models.TextField(null=True)
#     crash_type = models.TextField(null=True, blank=True)
#     death_count = models.PositiveSmallIntegerField(null=True, blank=True)
#     severe_injury_count = models.PositiveSmallIntegerField(null=True, blank=True)
#     def map_link(self):
#         return f"<a href='https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}'>({self.latitude}, {self.longitude})</a>"

# class InjuryVehicle(models.Model):
#     injury_accident = models.ForeignKey(InjuryAccident, on_delete=models.CASCADE)
#     vehicle_number = models.PositiveSmallIntegerField(null=False, blank=False)
#     make = models.TextField(null=True, blank=True)
#     model = models.TextField(null=True, blank=True)
#     body_type = models.TextField(null=True, blank=True)
#     violation = models.TextField(null=True, blank=True)
#     hit_and_run = models.BooleanField(default=False)

# class InjuryPerson(models.Model):
#     injury_accident = models.ForeignKey(InjuryAccident, on_delete=models.CASCADE)
#     injury_vehicle = models.ForeignKey(InjuryVehicle, null=True, blank=True, on_delete = models.CASCADE)
#     age = models.PositiveSmallIntegerField(null = True, blank = True)
#     #p6 
#     sex = models.CharField(max_length=64, null=True, blank=True)
#     person_type = models.CharField(max_length=256,null=True, blank=True)
#     #p8 injury_severity
#     injury_severity_choices = [
#         (0, 'No Apparent Injury (O)'),
#         (1, 'Possible Injury (C)'),
#         (2, 'Suspected Minor Injury (B)'),
#         (3, 'Suspected Serious Injury (A)'),
#         (4, 'Fatal Injury (K)'),
#         (5, 'Injured, Severity Unknown (U) (Since 1978)'),
#         (6, 'Died Prior to Crash'),
#         (9, 'Unknown/Not Reported')
#     ]			
#     injury_severity = models.PositiveSmallIntegerField(choices=injury_severity_choices, default=9)