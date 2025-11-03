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
        InjuryPerson.objects.filter(injury_accident__state_id=48, injury_accident__dt__year=2019).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=48, injury_accident__dt__year=2019).delete()
        InjuryAccident.objects.filter(state_id=48, dt__year=2019).delete()
        data = pd.read_csv(f"{TEXAS_PATH}2019_texas.csv")
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
    