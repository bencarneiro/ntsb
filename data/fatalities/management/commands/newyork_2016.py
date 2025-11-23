from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import NEW_YORK_PATH
from datetime import datetime

def injury_severity_converter(severity):
    if severity == 'K - FATAL':
        return 4
    if severity == 'A - SERIOUS INJURY':
        return 3
    if severity == 'B - INJURY':
        return 2
    if severity == 'C - POSSIBLE INJURY':
        return 1
    return 9

# Example usage:
class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=36, injury_accident__dt__year=2016).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=36, injury_accident__dt__year=2016).delete()
        InjuryAccident.objects.filter(state_id=36, dt__year=2016).delete()

        crashes_path = f"{NEW_YORK_PATH}crash_2016.csv"
        vehicle_path = f"{NEW_YORK_PATH}vehicle_2016.csv"
        person_path = f"{NEW_YORK_PATH}person_2016.csv"
        crashes = pd.read_csv(crashes_path)
        vehicles = pd.read_csv(vehicle_path)
        persons = pd.read_csv(person_path)
        crash_list = []
        vehicle_list = []
        person_list = []
        print(crashes.columns)
        for x in crashes.index:
            print(x)
            
            crash_vehicles = vehicles[vehicles['state_accident_id'] == crashes['state_accident_id'][x]]
            crash_persons = persons[persons['state_accident_id'] == crashes['state_accident_id'][x]]
            latitude = crashes['latitude'][x]
            longitude = crashes['longitude'][x]
            if pd.isnull(crashes['latitude'][x]) or pd.isnull(crashes['longitude'][x]):
                latitude, longitude = None, None
            timestamp = datetime.strptime(crashes['dt'][x], "%Y-%m-%dT%H:%M:%S")
            new_crash = InjuryAccident(
                state_id=36,
                state_accident_id = int(crashes['state_accident_id'][x]),
                dt = timestamp,
                latitude = latitude,
                longitude = longitude,
                county = crashes['county'][x],
                street_1 = crashes['street_1'][x],
                street_2 = crashes['street_2'][x],
                crash_type = crashes['crash_type'][x],
                death_count = crashes['death_count'][x],
                severe_injury_count = crashes['severe_injury_count'][x]
            )
            
            crash_list += [new_crash]
            veh_dict = {}
            for y in crash_vehicles.index:
                veh_num = int(crash_vehicles['vehicle_number'][y])
                new_vehicle = InjuryVehicle(
                    injury_accident=new_crash,
                    vehicle_number=veh_num,
                    body_type=crash_vehicles['body_type'][y],
                )
                vehicle_list += [new_vehicle]
                print(veh_num)
                veh_dict[veh_num] = new_vehicle
            for z in crash_persons.index:
                age = crash_persons['age'][z]
                if pd.isnull(age):
                    age = None
                veh_num = int(crash_persons['vehicle_number'][z])
                if not veh_num or pd.isnull(veh_num):
                    person_vehicle = None
                else:
                    person_vehicle = veh_dict[veh_num]
                new_person = InjuryPerson(
                    injury_accident=new_crash,
                    injury_vehicle=person_vehicle,
                    age = age,
                    sex = crash_persons['sex'][z],
                    injury_severity = injury_severity_converter(crash_persons['injury_severity'][z]),
                    person_type = crash_persons['person_type'][z]
                )
                person_list += [new_person]
        InjuryAccident.objects.bulk_create(crash_list)
        InjuryVehicle.objects.bulk_create(vehicle_list)
        InjuryPerson.objects.bulk_create(person_list)



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