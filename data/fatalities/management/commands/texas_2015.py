from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import TEXAS_PATH
from datetime import datetime


def injury_severity_converter(injury_severity):
    if injury_severity == "K - FATAL INJURY":
        return 4
    if injury_severity == "A - SUSPECTED SERIOUS INJURY":
        return 3
    if injury_severity == "B - SUSPECTED MINOR INJURY":
        return 2
    if injury_severity == "C - POSSIBLE INJURY":
        return 1
    if injury_severity == "N - NOT INJURED":
        return 0
    return 9
    

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=48, injury_accident__dt__year=2015).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=48, injury_accident__dt__year=2015).delete()
        InjuryAccident.objects.filter(state_id=48, dt__year=2015).delete()
        data = pd.read_csv(f"{TEXAS_PATH}2015_texas.csv")
        crash_id = None
        for x in data.index:
            print(x)
            crash_id = data['Crash ID'][x]
            try:
                age = int(data['Person Age'][x])
            except:
                age = None
            try:
                latitude = float(data['Latitude'][x])
                longitude = float(data['Longitude'][x])
            except:
                latitude, longitude = None, None
            try:
                accident = InjuryAccident.objects.get(state_accident_id=crash_id)
                print("crash found")
            except:
                time = data['Crash Time'][x]
                if pd.isnull(time):
                    time = 0
                minutes = str(time % 100).zfill(2)
                hours = str(math.floor(time/100)).zfill(2)
                timestamp = datetime.strptime(data['Crash Date'][x] + "T" + hours + ":" + minutes + ":00", "%Y-%m-%dT%H:%M:%S")
                accident = InjuryAccident(
                    state_accident_id=crash_id,
                    state_id=48,
                    dt=timestamp,
                    latitude=latitude,
                    longitude=longitude,
                    city=data['City'][x],
                    county=data['County'][x],
                    street_1=data['Street Name'][x],
                    street_2=data['Intersecting Street Name'][x],
                    death_count = 0,
                    severe_injury_count = 0
                )
                accident.save()
                print("crash written")
            if data['Unit Description'][x] == "1 - MOTOR VEHICLE":
                print("This is a car")
                try: 
                    vehicle = InjuryVehicle.objects.get(
                        injury_accident__state_accident_id=crash_id, 
                        vehicle_number = data['Unit Number'][x]
                    )
                    print("car found")
                except:
                    hit_and_run = False
                    if data['Vehicle Hit and Run Flag'][x] == "Yes":
                        hit_and_run = True
                    vehicle = InjuryVehicle(
                        injury_accident=accident,
                        make = data['Vehicle Make'][x],
                        model = data['Vehicle Model Year'][x] + " " + data['Vehicle Model Name'][x],
                        body_type = data['Vehicle Body Style'][x],
                        hit_and_run = hit_and_run,
                        violation = data['Charge'][x],
                        vehicle_number = data['Unit Number'][x]
                    )
                    vehicle.save()
                    print("Car created")
                injury_severity = injury_severity_converter(data['Person Injury Severity'][x])
                person = InjuryPerson(
                    injury_accident = accident,
                    injury_vehicle = vehicle,
                    person_type = data['Person Type'][x],
                    age = age,
                    sex = data['Person Gender'][x],
                    injury_severity = injury_severity
                )
                person.save()
            else:
                injury_severity = injury_severity_converter(data['Person Injury Severity'][x])
                person = InjuryPerson(
                    injury_accident = accident,
                    person_type = data['Person Type'][x],
                    age = age,
                    sex = data['Person Gender'][x],
                    injury_severity = injury_severity
                )
                person.save()
            if injury_severity == 4:
                accident.death_count += 1
                accident.save()
                print("added a death to the count")
            if injury_severity == 3:
                accident.severe_injury_count += 1
                accident.save()
                print("added a disabling event to the count")
        

                
                




# class InjuryAccident(models.Model):
#     id = models.AutoField(primary_key=True)
#     state = models.ForeignKey(State, on_delete= models.DO_NOTHING)
#     state_accident_id = models.PositiveBigIntegerField(null=False, blank=False)
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