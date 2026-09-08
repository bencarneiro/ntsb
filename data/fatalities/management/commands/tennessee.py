from django.core.management.base import BaseCommand
from data.settings import TENNESSEE_PATH
import pandas as pd
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson
from datetime import datetime, timezone

from django.utils.timezone import make_aware, utc

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=47).delete()
        InjuryAccident.objects.filter(state_id=47).delete()
        new_crash_list = []
        crashes = pd.read_csv(f"{TENNESSEE_PATH}/tn_fatal_and_serious_injury_crashes.csv")
        for x in crashes.index:
            state_accident_id = crashes['MRN'][x]
            state_id = 47
            dt = crashes['Collision_Date'][x]
            latitude = crashes['Latitude'][x]
            longitude = crashes['Longitude'][x]
            crash_severity = crashes['Crash_Type'][x]
            city = crashes['City'][x]
            county = crashes['County'][x]
            crash_type = crashes['First_Harmfu_Event'][x]
            if crashes['Pedestrian'][x] !="-":
                crash_type += " - Pedestrian"
            if crashes['Pedalcyclist'][x] !="-":
                crash_type += " - Cyclist"
            if crashes['Other_Nonmotorist'][x] !="-":
                crash_type += " - Other Nonmotorist"
            if crashes['Motorcycle_Involved'][x] !="-":
                crash_type += " - Motorcycle"
            if crashes['ATV_Involved'][x] !="-":
                crash_type += " - ATV Involved"
            if crashes['LargeTruck_Involved'][x] !="-":
                crash_type += " - Large Truck"
            if crashes['SchoolBus'][x] !="-":
                crash_type += " - School Bus"
            new_injury_accident = InjuryAccident(
                state_id=state_id,
                state_accident_id=state_accident_id,
                latitude=latitude,
                longitude=longitude,
                city=city,
                county=county,
                crash_type=crash_type,
                crash_severity = crash_severity,
                dt=dt
            )
            new_crash_list += [new_injury_accident]
        InjuryAccident.objects.bulk_create(new_crash_list)


# 'OBJECTID', 'MRN', 'Fatality', 'Injury', 'Latitude', 'Longitude',
#        'THP_District', 'Collision_Date', 'Collision_Year', 'Collision_Month',
#        'Collision_Day', 'Collision_Hour', 'Collision_Min', 'Collision_DOW',
#        'Collision_Time', 'Crash_Type', 'Light_Condition', 'Weather',
#        'First_Harmfu_Event', 'Work_Zone_Type', 'Agency_Name', 'THP',
#        'Unbelted', 'Distracted_Driver', 'Driver_Drinking', 'Driver_Drugged',
#        'Drowsy_Driver', 'Speeding_Involved', 'Pedalcyclist', 'Pedestrian',
#        'Other_Nonmotorist', 'ATV_Involved', 'LargeTruck_Involved',
#        'Motorcycle_Involved', 'SchoolBus', 'County', 'City', 'DOW_Nmb'

# class InjuryAccident(models.Model):
#     id = models.AutoField(primary_key=True)
#     state = models.ForeignKey(State, on_delete= models.DO_NOTHING)
#     state_accident_id = models.CharField(max_length=128, null=True, blank=True)
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
#     crash_severity = models.CharField(max_length=64, null=True, blank=True)
#     # this field only employed for north carolina right now. 
#     motorcycle = models.BooleanField(default=False)
#     number_of_vehicles = models.PositiveSmallIntegerField(null=True, blank=True)
#     number_of_nonmotorists = models.PositiveSmallIntegerField(null=True, blank=True)
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