from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import MICHIGAN_PATH
from datetime import datetime
import os

def injury_severity_converter(code):
    if "Fatal" in code:
        return 4
    if "Serious" in code:
        return 3
    if "Minor" in code:
        return 2
    if "Possible" in code:
        return 1
    if "No Injury" in code:
        return 0
    if "Uncoded" in code:
        return 9
    return 9

def month_converter(month_name):
    if month_name == "January":
        return "01"
    if month_name == "February":
        return "02"
    if month_name == "March":
        return "03"
    if month_name == "April":
        return "04"
    if month_name == "May":
        return "05"
    if month_name == "June":
        return "06"
    if month_name == "July":
        return "07"
    if month_name == "August":
        return "08"
    if month_name == "September":
        return "09"
    if month_name == "October":
        return "10"
    if month_name == "November":
        return "11"
    if month_name == "December":
        return "12"


# Example usage:
class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):   
        crashes = []
        vehicles = []
        persons = []     
        InjuryPerson.objects.filter(injury_accident__state_id=26, injury_accident__dt__year=2015).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=26, injury_accident__dt__year=2015).delete()
        InjuryAccident.objects.filter(state_id=26, dt__year=2015).delete()
        year = 2015
        start = 1
        end = 90
        total = int(os.listdir(f"../michigan/data/{year}")[0].split("of_")[1].split(".")[0])
        # saved_crash_ids = set()
        saved_crashes = set()
        saved_vehicle_ids = {}
        while start <= total:
            if end > total:
                end = total
            data = pd.read_csv(f"../michigan/data/{year}/crash_data_{year}__{start}_to_{end}_of_{total}.csv", skiprows=1)

            for x in data.index:
                
                if int(data['Crash Instance'][x]) not in saved_crashes:
                    hour = data['Time of Day'][x].split(":")[0].zfill(2)
                    if len(hour) > 2:
                        hour = "00"
                    month = month_converter(data['Crash Month'][x])
                    datestring = f"2015-{month}-{str(data['Crash Day'][x]).zfill(2)}T{hour}:00:00"
                    timestamp = datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S")
                    latitude = data['Crash Latitude'][x]
                    longitude = data['Crash Longitude'][x]
                    try:
                        county = data['County'][x].split(": ")[1]
                    except:
                        county = data['County'][x]
                    if not latitude or not longitude:
                        latitude, longitude = None, None
                    
                    crash = InjuryAccident(
                        state_id=26,
                        state_accident_id=int(data['Crash Instance'][x]),
                        dt=timestamp,
                        latitude = latitude,
                        longitude = longitude,
                        city = data['City or Township'][x],
                        county = county,
                        crash_type = data['Crash Type'][x]
                    )
                    print(f"saved crash {data['Crash Instance'][x]}")
                    crashes += [crash]
                    saved_crashes.add(int(data['Crash Instance'][x]))
                    saved_vehicles = 0
                if data['Vehicle Instance'][x] not in saved_vehicle_ids:
                    vehicle = InjuryVehicle(
                        injury_accident=crash,
                        vehicle_number = saved_vehicles + 1,
                        body_type = data['Traffic Unit Type'][x] + " " + data['Vehicle Type'][x]
                    )
                    if data['Traffic Unit Type'][x] not in ["Pedestrian", "Bicycle", "Train Engineer"]:
                        vehicles += [vehicle]
                        saved_vehicle_ids[data['Vehicle Instance'][x]] = saved_vehicles + 1
                        saved_vehicles += 1
                        print(f"saved vehicle {data['Vehicle Instance'][x]} as vehicle number {saved_vehicles}")
                try:
                    age = int(data['Person Age'][x])
                except:
                    age = None
                if data['Traffic Unit Type'][x] in ["Pedestrian", "Bicycle", "Train Engineer"]:
                    person = InjuryPerson(
                        injury_accident = crash,
                        person_type = data['Party Type'][x],
                        sex = data['Person Gender'][x],
                        age = age,
                        injury_severity = injury_severity_converter(data['Person Degree of Injury'][x])
                    )
                    print(f"saved pedestrian {data['Person Instance'][x]}")
                    persons += [person]
                else:                    
                    person = InjuryPerson(
                        injury_accident = crash,
                        injury_vehicle = vehicle,
                        person_type = data['Party Type'][x],
                        sex = data['Person Gender'][x],
                        age = age,
                        injury_severity = injury_severity_converter(data['Person Degree of Injury'][x])
                    )
                    print(f"saved motorist {data['Person Instance'][x]}")
                    persons += [person]
                    
            start += 90
            end += 90
        InjuryAccident.objects.bulk_create(crashes)
        InjuryVehicle.objects.bulk_create(vehicles)
        InjuryPerson.objects.bulk_create(persons)
        # calculate totals from values in the database
        new_crashes = InjuryAccident.objects.filter(state_id=26, dt__year=2015)
        
        print("running death count totals")
        for crash in new_crashes:
            crash.death_count = len(InjuryPerson.objects.filter(injury_accident=crash, injury_severity=4))
            crash.severe_injury_count = len(InjuryPerson.objects.filter(injury_accident=crash, injury_severity=3))
            crash.save()
    
