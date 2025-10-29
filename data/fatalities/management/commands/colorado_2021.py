from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
from datetime import datetime
from data.settings import COLORADO_PATH


class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__dt__year=2021).delete()
        InjuryVehicle.objects.filter(injury_accident__dt__year=2021).delete()
        InjuryAccident.objects.filter(dt__year=2021).delete()
        data = pd.read_excel(f"{COLORADO_PATH}CDOTRM_CD_Crash_Listing_-_2021.xlsx")
        data = data[(data['Injury 04']>0) | (data['Injury 03']>0)]

        for x in data.index:
            state_accident_id = data['CUID'][x]
            print(f"state_accident_id: {state_accident_id}")
            time = data['Crash Time'][x]
            if pd.isnull(time):
                time = "00:00:00"
            timestamp = datetime.strptime(str(data['Crash Date'][x].date()) + "T" + time, "%Y-%m-%dT%H:%M:%S")
            print(f"timestamp {timestamp}")
            latitude = data['Latitude'][x]
            longitude = data['Longitude'][x]
            if pd.isnull(latitude):
                latitude = None
            if pd.isnull(longitude):
                longitude = None
            print(f"({latitude},{longitude})")
            city = data["City"][x]
            if pd.isnull(city):
                city = None
            county = data["County"][x]
            print(f"{city}, {county} county")
            location_1 = data['Location 1'][x]
            location_2 = data['Location 2'][x]
            if pd.isnull(location_1):
                location_1 = None
            if pd.isnull(location_2):
                location_2 = None
            print(f"{location_1} and {location_2}")
            crash_type = data['Crash Type'][x]
            print(f"crash type: {crash_type}")
            death_count = data['Injury 04'][x]
            serious_injury_count = data['Injury 03'][x]
            print(f"{death_count} deaths and {serious_injury_count} serious injuries")
            new_injury_accident = InjuryAccident(
                state_accident_id=state_accident_id,
                state_id=8,
                dt=timestamp,
                latitude=latitude,
                longitude=longitude,
                street_1=location_1,
                street_2=location_2,
                city=city,
                county=county,
                crash_type=crash_type,
                death_count=death_count,
                severe_injury_count=serious_injury_count,
            )
            new_injury_accident.save()
            tu_1_is_car = False
            if not pd.isnull(data['TU-1 Type'][x]):
                print("TU 1 is a vehicle")
                tu_1_is_car = True
                body_type = data['TU-1 Type'][x]
                print(f"body type: {body_type}")
                violation = data['TU-1 Driver Action'][x]
                print(f"violation: {violation}")
                hit_run = data['TU-1 Hit And Run'][x]
                age = data['TU-1 Age'][x]
                sex = data['TU-1 Sex '][x]
                if pd.isnull(age):
                    age = None
                if pd.isnull(sex):
                    Sex = None
                print(f"age: {age}, sex: {sex}")
                injury_severity = 9
                new_injury_vehicle = InjuryVehicle(
                    injury_accident = new_injury_accident,
                    body_type=body_type,
                    vehicle_number = 1,
                    hit_and_run=hit_run,
                    violation=violation
                )
                new_injury_vehicle.save()
                new_injury_person = InjuryPerson(
                    injury_accident = new_injury_accident,
                    injury_vehicle=new_injury_vehicle,
                    person_type="Driver",
                    age=age,
                    sex=sex,
                    injury_severity=injury_severity
                )
                new_injury_person.save()
                
            if not pd.isnull(data['TU-2 Type'][x]):
                print("TU 2 is a vehicle")
                body_type = data['TU-2 Type'][x]
                print(f"body type: {body_type}")
                violation = data['TU-2 Driver Action'][x]
                print(f"violation: {violation}")
                hit_run = data['TU-2 Hit And Run'][x]
                age = data['TU-2 Age'][x]
                sex = data['TU-2 Sex'][x]
                if pd.isnull(age):
                    age = None
                if pd.isnull(sex):
                    Sex = None
                print(f"age: {age}, sex: {sex}")
                injury_severity = 9
                vehicle_number = 1
                if tu_1_is_car:
                    vehicle_number = 2
                new_injury_vehicle = InjuryVehicle(
                    injury_accident = new_injury_accident,
                    body_type=body_type,
                    vehicle_number = vehicle_number,
                    hit_and_run=hit_run,
                    violation=violation
                )
                new_injury_vehicle.save()
                new_injury_person = InjuryPerson(
                    injury_accident = new_injury_accident,
                    injury_vehicle=new_injury_vehicle,
                    person_type="Driver",
                    age=age,
                    sex=sex,
                    injury_severity=injury_severity
                )
                new_injury_person.save()
                
                
                
            if not pd.isnull(data['TU-1 NM Type'][x]):
                print("TU 1 is a Pedestrian")
                person_type = data['TU-1 NM Type'][x]
                print(data['TU-1 NM Type'][x])
                age = data['TU-1 NM Age '][x]
                sex = data['TU-1 NM Sex '][x]
                if pd.isnull(age):
                    age = None
                if pd.isnull(sex):
                    Sex = None
                print(f"age {age}, sex: {sex}")
                injury_severity = 9
                new_injury_person = InjuryPerson(
                    injury_accident=new_injury_accident,
                    age=age,
                    sex=sex,
                    person_type=person_type,
                    injury_severity=injury_severity
                )
                new_injury_person.save()

                
                
            if not pd.isnull(data['TU-2 NM Type'][x]):
                print("TU 2 is a Pedestrian")
                person_type = data['TU-1 NM Type'][x]
                print(data['TU-2 NM Type'][x])
                age = data['TU-2 NM Age '][x]
                sex = data['TU-2 NM Sex '][x]
                if pd.isnull(age):
                    age = None
                if pd.isnull(sex):
                    Sex = None
                print(f"age {age}, sex: {sex}")
                injury_severity = 9
                new_injury_person = InjuryPerson(
                    injury_accident=new_injury_accident,
                    age=age,
                    sex=sex,
                    person_type=person_type,
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
#     age = models.PositiveSmallIntegerField(null = True)
#     #p6 
#     sex_choices = [
#         (1, "Male"),
#         (2, "Female"),
#         (3, "Other"),
#         (8, "Not Reported"),
#         (9, "Reported as Unknown")
#     ]
#     sex = models.PositiveSmallIntegerField(choices=sex_choices, default=8)
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