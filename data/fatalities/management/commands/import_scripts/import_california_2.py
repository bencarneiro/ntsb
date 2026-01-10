from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import CALIFORNIA_PATH
from datetime import datetime
# array(['severe injury', 'no injury', 'killed', 'other visible injury',
#        'complaint of pain'], dtype=object)


def injury_severity_converter(severity):
    if severity == "no injury":
        return 0
    if severity == "complaint of pain":
        return 1
    if severity == "other visible injury":
        return 2
    if severity == "severe injury":
        return 3
    if severity == "killed":
        return 4
    return 9



class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=6, injury_accident__dt__year__lt=2014).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=6, injury_accident__dt__year__lt=2014).delete()
        InjuryAccident.objects.filter(state_id=6, dt__year__lt=2014).delete()

        crashes_path = f"{CALIFORNIA_PATH}early_data/collisions.csv"
        parties_crash = f"{CALIFORNIA_PATH}early_data/parties.csv"
        victims_path = f"{CALIFORNIA_PATH}early_data/victims.csv"
        crashes = pd.read_csv(crashes_path)
        parties = pd.read_csv(parties_crash)
        victims = pd.read_csv(victims_path)
        accidents, vehicles, persons = [],[],[]
        for x in crashes.index:

            print(x)
            print(f"id: {crashes['case_id'][x]}")
            parties_to_crash = parties[parties['case_id']==crashes['case_id'][x]]
            victims_of_crash = victims[victims['case_id']==crashes['case_id'][x]]
            injury_totals = victims_of_crash['victim_degree_of_injury'].value_counts()
            death_count = 0
            serious_injury_count = 0
            death_count += len(victims_of_crash[victims_of_crash['victim_degree_of_injury'] == "killed"])
            serious_injury_count += len(victims_of_crash[victims_of_crash['victim_degree_of_injury'] == "severe injury"])
            time = crashes['collision_time'][x]
            if pd.isnull(time):
                time = "00:00:00"
            print(crashes['collision_date'][x])
            print(time)
            timestamp = datetime.strptime(crashes['collision_date'][x] + "T" + str(time), "%Y-%m-%dT%H:%M:%S")
            
            try:
                latitude = float(crashes['latitude'][x])
                longitude = float(crashes['longitude'][x])
                if pd.isnull(latitude):
                    latitude, longitude = None, None
            except:
                latitude, longitude = None, None
            new_injury_accident = InjuryAccident(
                state_accident_id=int(crashes['case_id'][x]),
                state_id=6,
                dt = timestamp,
                latitude = latitude,
                longitude = longitude,
                county = crashes['county_location'][x],
                street_1 = crashes['primary_road'][x],
                street_2 = crashes['secondary_road'][x],
                crash_type=crashes['type_of_collision'][x],
                death_count = death_count,
                severe_injury_count = serious_injury_count
            )
            accidents += [new_injury_accident]
            vehicles_for_this_crash = {}
            for y in parties_to_crash.index:
                if parties_to_crash['party_type'][y] in {"driver","parked vehicle"}:
                    try:
                        veh_year = str(int(parties_to_crash['vehicle_year'][y]))
                        if veh_year == "9999":
                            veh_year = ""
                    except:
                        veh_year = ""
                    make = veh_year + " " + str(parties_to_crash['vehicle_make'][y])
                    print(make)
                    new_injury_vehicle = InjuryVehicle(
                        injury_accident=new_injury_accident,
                        vehicle_number = parties_to_crash['party_number'][y],
                        make=make,
                        body_type = parties_to_crash['statewide_vehicle_type'][y],
                    )
                    vehicles += [new_injury_vehicle]
                    
                    vehicles_for_this_crash[int(parties_to_crash['party_number'][y])] = new_injury_vehicle
                    driver = victims_of_crash[(victims_of_crash['party_number'] == parties_to_crash['party_number'][y]) & (victims_of_crash['victim_role'] == 1)]
                    age = parties_to_crash['party_age'][y]
                    if pd.isnull(age):
                        age = None
                        
                    if len(driver) == 0:
                        print("No driver found in victim table")
                        new_injury_person = InjuryPerson(
                            injury_accident = new_injury_accident,
                            injury_vehicle=new_injury_vehicle,
                            person_type = "Driver",
                            age = age,
                            sex = parties_to_crash['party_sex'][y],
                            injury_severity=0
                        )
                        print(f"party: {parties_to_crash['party_number'][y]} ---person written but not a victim")
                        persons += [new_injury_person]
            for z in victims_of_crash.index:
                if victims_of_crash['party_number'][z] in vehicles_for_this_crash:
                    injury_vehicle = vehicles_for_this_crash[victims_of_crash['party_number'][z]]
                else:
                    injury_vehicle = None
                age = victims_of_crash['victim_age'][z]
                if pd.isnull(age):
                    age = None
                new_injury_person = InjuryPerson(
                    injury_accident=new_injury_accident,
                    injury_vehicle=injury_vehicle,
                    age=age,
                    sex=victims_of_crash['victim_sex'][z],
                    person_type=victims_of_crash['victim_role'][z],
                    injury_severity=injury_severity_converter(victims_of_crash['victim_degree_of_injury'][z])
                )
                print(f"victim written - {victims_of_crash['victim_role'][z]} - vehicle {injury_vehicle}")
                persons += [new_injury_person]
            
            if x % 1000 == 999:
                InjuryAccident.objects.bulk_create(accidents)
                InjuryVehicle.objects.bulk_create(vehicles)
                InjuryPerson.objects.bulk_create(persons)
                accidents, vehicles, persons = [],[],[]
            
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