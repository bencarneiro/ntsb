from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import CALIFORNIA_PATH
from datetime import datetime
import os

def person_type_converter(code):
    if code == 1:
        return "Driver"
    elif code == 2:
        return "Passenger"
    elif code == 3:
        return "Pedestrian"
    elif code == 4:
        return "Bicyclist"
    elif code == 6:
        return "Non-Injured Party"
    else:
        return "Other"
    	

def crash_type_converter(code):
    if code == "A":
        return "Head-On"
    elif code == "B":
        return "Sideswipe"
    elif code == "C":
        return "Rear End"
    elif code == "D":
        return "Broadside"
    elif code == "E":
        return "Hit Object"
    elif code == "F":
        return "Overturned"
    elif code == "G":
        return "Vehicle/Pedestrian"
    elif code == "H":
        return "Other"
    return None

def injury_severity_converter(injury_severity):
    if injury_severity == 0: 
        return 0
    if injury_severity == 1:
        return 4
    if injury_severity in {2,5}:
        return 3
    if injury_severity in {3,6}:
        return 2
    if injury_severity in {4,7}:
        return 1
    
    
def body_type_converter(code):
    if code == "A":
        return "Passenger Car/Station Wagon"
    elif code == "B":
        return "Passenger Car With Trailer"
    elif code == "C":
        return "Motorcycle/Scooter"
    elif code == "D":
        return "Pickup or Panel Truck"
    elif code == "E":
        return "Pickup or Panel Truck with Trailer"
    elif code == "F":
        return "Truck or Truck Tractor"
    elif code == "G":
        return "Truck or Truck Tractor with Trailer"
    elif code == "H":
        return "Schoolbus"
    elif code == "I":
        return "Other Bus"
    elif code == "J":
        return "Emergency Vehicle"
    elif code == "K":
        return "Highway Construction Equipment"
    elif code == "L":
        return "Bicycle"
    elif code == "M":
        return "Other Vehicle"
    elif code == "N":
        return "Pedestrian"
    elif code == "O":
        return "Moped"
    else:
        return None

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=6, injury_accident__dt__year__gte=2014).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=6, injury_accident__dt__year__gte=2014).delete()
        InjuryAccident.objects.filter(state_id=6, dt__year__gte=2014).delete()
        files = os.listdir(CALIFORNIA_PATH)
        for file in files:
            if "." in file:
                continue
            crashes_path = f"{CALIFORNIA_PATH}{file}/Crashes.csv"
            parties_crash = f"{CALIFORNIA_PATH}{file}/Parties.csv"
            victims_path = f"{CALIFORNIA_PATH}{file}/Victims.csv"
            crashes = pd.read_csv(crashes_path)
            parties = pd.read_csv(parties_crash)
            victims = pd.read_csv(victims_path)
            accidents, vehicles, persons = [],[],[]
            for x in crashes.index:
                print(x)
                print(f"id: {crashes['CASE_ID'][x]}")
                party_numbers_saved_as_vehicles = []
                parties_to_crash = parties[parties['CASE_ID']==crashes['CASE_ID'][x]]
                victims_of_crash = victims[victims['CASE_ID']==crashes['CASE_ID'][x]]
                injury_totals = victims_of_crash['VICTIM_DEGREE_OF_INJURY'].value_counts()
                death_count = 0
                serious_injury_count = 0
                if 1 in injury_totals:
                    death_count += injury_totals[1]
                if 2 in injury_totals:
                    serious_injury_count += injury_totals[2]
                if 5 in injury_totals:
                    serious_injury_count += injury_totals[5]
                time = crashes['COLLISION_TIME'][x]
                if pd.isnull(time) or time > 2359:
                    time = 0
                minutes = str(time % 100).zfill(2)
                hours = str(math.floor(time/100)).zfill(2)
                timestamp = datetime.strptime(crashes['COLLISION_DATE'][x] + "T" + hours + ":" + minutes + ":00", "%Y-%m-%dT%H:%M:%S")
                
                try:
                    latitude = float(crashes['POINT_Y'][x])
                    longitude = float(crashes['POINT_X'][x])
                    if pd.isnull(latitude):
                        latitude, longitude = None, None
                except:
                    latitude, longitude = None, None
                new_injury_accident = InjuryAccident(
                    state_accident_id=crashes['CASE_ID'][x],
                    state_id=6,
                    dt = timestamp,
                    latitude = latitude,
                    longitude = longitude,
                    city = crashes['CITY'][x],
                    county = crashes['COUNTY'][x],
                    street_1 = crashes['PRIMARY_RD'][x],
                    street_2 = crashes['SECONDARY_RD'][x],
                    crash_type=crash_type_converter(crashes['TYPE_OF_COLLISION'][x]),
                    death_count = death_count,
                    severe_injury_count = serious_injury_count
                )
                accidents += [new_injury_accident]
                vehicles_for_this_crash = {}
                for y in parties_to_crash.index:
                    if parties_to_crash['PARTY_TYPE'][y] in {"1","3"}:
                        try:
                            veh_year = str(int(parties_to_crash['VEHICLE_YEAR'][y]))
                            if veh_year == "9999":
                                veh_year = ""
                        except:
                            veh_year = ""
                        make = veh_year + " " + str(parties_to_crash['VEHICLE_MAKE'][y])
                        print(make)
                        new_injury_vehicle = InjuryVehicle(
                            injury_accident=new_injury_accident,
                            vehicle_number = parties_to_crash['PARTY_NUMBER'][y],
                            make=make,
                            body_type = body_type_converter(parties_to_crash['STWD_VEHICLE_TYPE'][y]),
                        )
                        vehicles += [new_injury_vehicle]
                        
                        vehicles_for_this_crash[int(parties_to_crash['PARTY_NUMBER'][y])] = new_injury_vehicle
                        driver = victims_of_crash[(victims_of_crash['PARTY_NUMBER'] == parties_to_crash['PARTY_NUMBER'][y]) & (victims_of_crash['VICTIM_ROLE'] == 1)]
                        
                        if len(driver) == 0:
                            print("No driver found in victim table")
                            new_injury_person = InjuryPerson(
                                injury_accident = new_injury_accident,
                                injury_vehicle=new_injury_vehicle,
                                person_type = "Driver",
                                age = parties_to_crash['PARTY_AGE'][y],
                                sex = parties_to_crash['PARTY_SEX'][y],
                                injury_severity=0
                            )
                            print(f"party: {parties_to_crash['PARTY_NUMBER'][y]} ---person written but not a victim")
                            persons += [new_injury_person]
                for z in victims_of_crash.index:
                    if victims_of_crash['PARTY_NUMBER'][z] in vehicles_for_this_crash:
                        injury_vehicle = vehicles_for_this_crash[victims_of_crash['PARTY_NUMBER'][z]]
                    else:
                        injury_vehicle = None

                    new_injury_person = InjuryPerson(
                        injury_accident=new_injury_accident,
                        injury_vehicle=injury_vehicle,
                        age=victims_of_crash['VICTIM_AGE'][z],
                        sex=victims_of_crash['VICTIM_SEX'][z],
                        person_type=person_type_converter(int(victims_of_crash['VICTIM_ROLE'][z])),
                        injury_severity=injury_severity_converter(int(victims_of_crash['VICTIM_DEGREE_OF_INJURY'][z]))
                    )
                    print(f"victim written - {person_type_converter(int(victims_of_crash['VICTIM_ROLE'][z]))} - vehicle {injury_vehicle}")
                    persons += [new_injury_person]
                
                    
            InjuryAccident.objects.bulk_create(accidents)
            InjuryVehicle.objects.bulk_create(vehicles)
            InjuryPerson.objects.bulk_create(persons)
            # break


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