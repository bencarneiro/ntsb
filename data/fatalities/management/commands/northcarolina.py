from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import NORTH_CAROLINA_PATH
from datetime import datetime


# Example usage:
class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryAccident.objects.filter(state_id=37).delete()
        crash_list = []
        crashes_path = f"{NORTH_CAROLINA_PATH}crashdata.csv"
        data = pd.read_csv(crashes_path)
        for x in data.index:
            latitude = data['Latitude'][x]
            longitude = data['Longitude'][x]
            if pd.isnull(latitude) or pd.isnull(longitude):
                latitude, longitude = None, None
            date = data['Date'][x]
            time = f"{data['Time'][x]}:00"
            month = date[:2]
            year = date[6:-1]
            day = date[3:5]
            timestring = f"{year}-{month}-{day}T{time}"
            timestamp = datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%S")
            print(timestring)
            severity = "Severe Crash"
            if data['Crash_Seve'][x] == "K":
                severity = "Fatal Crash"
            moto = False
            if data['Motorcycle'][x] == "Y":
                moto = True       
            new_accident = InjuryAccident(
                state_id = 37,
                state_accident_id = int(data['Crash_ID'][x]),
                latitude=latitude,
                longitude=longitude,
                county = data['County_Nam'][x],
                city = data['City'][x],
                crash_type = data['Crash_Type'][x],
                street_1 = data['On_Road'][x],
                street_2 = data['From_Road'][x],
                crash_severity = severity,
                motorcycle = moto,
                number_of_vehicles = data['Num_Vehicl'][x],
                number_of_nonmotorists = data['Num_Non_Mo'][x],
                dt=timestamp
            )
            crash_list += [new_accident]
            
        InjuryAccident.objects.bulk_create(crash_list)



# Index(['latitude', 'longitude', 'FID', 'Crash_ID', 'GIS_RteTxt', 'GIS_Milepo',
#        'Longitude', 'Latitude', 'Source_ID', 'MapMethod', 'LOC_ERROR', 'Date',
#        'Time', 'Day_of_Wee', 'County_Nam', 'City', 'MPO_RPO_Na', 'Crash_Seve',
#        'Crash_Type', 'Num_Vehicl', 'Num_Non_Mo', 'Weather', 'Road_Condi',
#        'Light_Cond', 'Alcohol_Re', 'Speed_Rela', 'Unbelted_D', 'Motorcycle',
#        'Heavy_Truc', 'On_Road', 'Distance', 'Direction', 'From_Road',
#        'Toward_Roa', 'Crash_Repo'],

# add to model : crash severity, num vehicles, num nonmotorists, motorcycle


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