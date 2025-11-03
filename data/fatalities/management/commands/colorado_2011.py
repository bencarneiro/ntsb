from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import COLORADO_PATH
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=8, injury_accident__dt__year=2011).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=8, injury_accident__dt__year=2011).delete()
        InjuryAccident.objects.filter(state_id=8, dt__year=2011).delete()
        data = pd.read_excel(f"{COLORADO_PATH}CDOTRM_CD_Crash_Listing_-_2011.xlsx")
        data = data[(data['INJURY 04']>0) | (data['INJURY 03']>0)]

        for x in data.index:
            state_accident_id = "2011" + str(x).zfill(8)
            print(f"state_accident_id: {state_accident_id}")
            time = data['TIME'][x]
            if pd.isnull(time):
                time = "00:00:00"
            else:
                hours = str(math.floor(time/100)).zfill(2)
                minutes = str(round(time%100))
                print(time)
                print(hours)
                print(minutes)
                time = hours + ":" + minutes + ":" + "00"
            timestamp = datetime.strptime(str(data['DATE'][x].date()) + "T" + time, "%Y-%m-%dT%H:%M:%S")
            print(f"timestamp {timestamp}")
            latitude = data['LATITUDE'][x]
            longitude = data['LONGITUDE'][x]
            if pd.isnull(latitude):
                latitude = None
            if pd.isnull(longitude):
                longitude = None
            print(f"({latitude},{longitude})")
            city = data["CITY"][x]
            if pd.isnull(city):
                city = None
            county = data["COUNTY"][x]
            print(f"{city}, {county} county")
            location_1 = data['LOC_01'][x]
            location_2 = data['LOC_02'][x]
            if pd.isnull(location_1):
                location_1 = None
            if pd.isnull(location_2):
                location_2 = None
            print(f"{location_1} and {location_2}")
            crash_type = data['ACCTYPE'][x]
            print(f"crash type: {crash_type}")
            death_count = data['INJURY 04'][x]
            serious_injury_count = data['INJURY 03'][x]
            print(f"{death_count} deaths and {serious_injury_count} serious injuries")

            new_injury_accident = InjuryAccident(
                state_id=8,
                state_accident_id=state_accident_id,
                dt=timestamp,
                latitude=latitude,
                longitude=longitude,
                city=city,
                county=county,
                street_1=location_1,
                street_2=location_2,
                death_count=death_count,
                severe_injury_count=serious_injury_count,
                crash_type = crash_type
            )
            new_injury_accident.save()

            vehicle_count = 0

            age = data['AGE_1'][x]
            sex = data['SEX_1'][x]

            injury_severity = 9
            if data['DRVINJ_1'][x] == "FATAL":
                injury_severity = 4
            if data['DRVINJ_1'][x] == "INCAPACITATING INJURY":
                injury_severity = 3
            if data['DRVINJ_1'][x] == "NON-INCAPACITATING INJURY":
                injury_severity = 2
            if data['DRVINJ_1'][x] == "POSSIBLE/COMPLAINT OF INJURY":
                injury_severity = 1
            if data['DRVINJ_1'][x] == "NO INJURY":
                injury_severity = 0

            print(f"age: {age}, sex: {sex}, inj severity: {injury_severity}")
            if data['VEHICLE_1'][x] == "OTHER - SEE REPORT":

                print("person 1 is a pedestrian")
                print(data['ACCTYPE'][x])
                new_injury_person = InjuryPerson(
                    injury_accident=new_injury_accident,
                    age=age,
                    sex=sex,
                    person_type="Nonmotorist",
                    injury_severity=injury_severity
                )
                new_injury_person.save()
            else:
                vehicle_count += 1
                print("person 1 is a driver")
                body_type = data['VEHICLE_1'][x]
                violation = data['VIOLCODE_1'][x]
                vehicle_number = vehicle_count
                new_injury_vehicle = InjuryVehicle(
                    injury_accident=new_injury_accident,
                    body_type=body_type,
                    violation=violation,
                    vehicle_number=vehicle_number
                )
                new_injury_vehicle.save()
                new_injury_person = InjuryPerson(
                    injury_accident=new_injury_accident,
                    injury_vehicle=new_injury_vehicle,
                    age=age,
                    sex=sex,
                    person_type="Driver",
                    injury_severity=injury_severity
                )
                new_injury_person.save()
            if not pd.isnull(data['VEHICLE_2'][x]):

                age = data['AGE_2'][x]
                sex = data['SEX_2'][x]

                injury_severity = 9
                if data['DRVINJ_2'][x] == "FATAL":
                    injury_severity = 4
                if data['DRVINJ_2'][x] == "INCAPACITATING INJURY":
                    injury_severity = 3
                if data['DRVINJ_2'][x] == "NON-INCAPACITATING INJURY":
                    injury_severity = 2
                if data['DRVINJ_2'][x] == "POSSIBLE/COMPLAINT OF INJURY":
                    injury_severity = 1
                if data['DRVINJ_2'][x] == "NO INJURY":
                    injury_severity = 0

                print(f"age: {age}, sex: {sex}, inj severity: {injury_severity}")
                if data['VEHICLE_2'][x] == "OTHER - SEE REPORT":
                    print(data['ACCTYPE'][x])
                    new_injury_person = InjuryPerson(
                        injury_accident=new_injury_accident,
                        age=age,
                        sex=sex,
                        person_type="Nonmotorist",
                        injury_severity=injury_severity
                    )
                    new_injury_person.save()
                    print("person 2 is a pedestrian")
                else:
                    vehicle_count += 1
                    print("person 2 is a driver")
                    body_type = data['VEHICLE_2'][x]
                    violation = data['VIOLCODE_2'][x]
                    vehicle_number = vehicle_count
                    new_injury_vehicle = InjuryVehicle(
                        injury_accident=new_injury_accident,
                        body_type=body_type,
                        violation=violation,
                        vehicle_number=vehicle_number
                    )
                    new_injury_vehicle.save()
                    new_injury_person = InjuryPerson(
                        injury_accident=new_injury_accident,
                        injury_vehicle=new_injury_vehicle,
                        age=age,
                        sex=sex,
                        person_type="Driver",
                        injury_severity=injury_severity
                    )
                    new_injury_person.save()
            if not pd.isnull(data['VEHICLE_3'][x]):

                age = data['AGE_3'][x]
                sex = data['SEX_3'][x]

                injury_severity = 9
                if data['DRVINJ_3'][x] == "FATAL":
                    injury_severity = 4
                if data['DRVINJ_3'][x] == "INCAPACITATING INJURY":
                    injury_severity = 3
                if data['DRVINJ_3'][x] == "NON-INCAPACITATING INJURY":
                    injury_severity = 2
                if data['DRVINJ_3'][x] == "POSSIBLE/COMPLAINT OF INJURY":
                    injury_severity = 1
                if data['DRVINJ_3'][x] == "NO INJURY":
                    injury_severity = 0
                print(f"age: {age}, sex: {sex}, inj severity: {injury_severity}")
                if data['VEHICLE_3'][x] == "OTHER - SEE REPORT":
                    print(data['ACCTYPE'][x])
                    new_injury_person = InjuryPerson(
                        injury_accident=new_injury_accident,
                        age=age,
                        sex=sex,
                        person_type="Nonmotorist",
                        injury_severity=injury_severity
                    )
                    new_injury_person.save()
                    print("person 3 is a pedestrian")
                else:
                    vehicle_count += 1
                    print("person 3 is a driver")
                    body_type = data['VEHICLE_3'][x]
                    violation = data['VIOLCODE_3'][x]
                    vehicle_number = vehicle_count
                    new_injury_vehicle = InjuryVehicle(
                        injury_accident=new_injury_accident,
                        body_type=body_type,
                        violation=violation,
                        vehicle_number=vehicle_number
                    )
                    new_injury_vehicle.save()
                    new_injury_person = InjuryPerson(
                        injury_accident=new_injury_accident,
                        injury_vehicle=new_injury_vehicle,
                        age=age,
                        sex=sex,
                        person_type="Driver",
                        injury_severity=injury_severity
                    )
                    new_injury_person.save()



# class InjuryAccident(models.Model):
#     id = models.AutoField(primary_key=True)
#     state = models.ForeignKey(State, on_delete= models.DO_NOTHING)
#     state_accident_id = models.IntegerField(null=False, blank=False)
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
#     person_type = models.CharField(max_length=256, null=True, blank=True)
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