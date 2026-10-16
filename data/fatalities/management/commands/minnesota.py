from django.core.management.base import BaseCommand
from data.settings import MINNESOTA_PATH
import pandas as pd
from fatalities.models import InjuryAccident, InjuryVehicle
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        crash_list = []
        vehicle_list = []
        InjuryAccident.objects.filter(state_id=27).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=27).delete()
        crashes = pd.read_csv(f"{MINNESOTA_PATH}/crash.csv")
        for x in crashes.index:
            if x % 100 == 0:
                InjuryAccident.objects.bulk_create(crash_list)
                InjuryVehicle.objects.bulk_create(vehicle_list)
                crash_list = []
                vehicle_list = []
            dt = crashes['DateOfIncident'][x]
            state_accident_id = crashes['LocalCodeTxt'][x]
            lat = round(crashes['LatDec'][x],7)
            lon = round(crashes['LongDec'][x],7)
            street_1 = crashes['RdwyNameTxt'][x]
            city = crashes['CityTownship'][x]
            county = crashes['CountyNameTxt'][x]
            severe_injury_count = crashes['SuspectedSeriousInjury_calc'][x]
            death_count = crashes['Fatalities_calc'][x]
            crash_type = f"{crashes['CrashType'][x]} - {crashes['CrashDetail'][x]}"
            if "Yes" in crashes['HitAndRunInd_txtCARTO'][x]:
                crash_type += " - HIT AND RUN"
            print(x)
            new_injury_accident = InjuryAccident(
                state_id=27,
                state_accident_id=state_accident_id,
                latitude=lat,
                longitude=lon,
                street_1=street_1,
                city=city,
                county=county,
                death_count=death_count,
                severe_injury_count=severe_injury_count,
                crash_type=crash_type,
                dt=dt
            )
            crash_list += [new_injury_accident]
            vehicle_makemodel_list = crashes['VehicleMakeModelYearTxt_list'][x]
            body_type_list = crashes['VehicleTypeCde_txtCARTO_list'][x]
            if pd.isnull(body_type_list):
                continue
            body_types = body_type_list.split(", ")
            y = 0
            for body_type in body_types:
                try:
                    model = vehicle_makemodel_list.split(", ")[y]
                except:
                    model = None
                new_injury_vehicle = InjuryVehicle(
                    injury_accident=new_injury_accident,
                    body_type = body_type,
                    model = model,
                    vehicle_number = y + 1
                )
                vehicle_list += [new_injury_vehicle]
                y += 1

        InjuryAccident.objects.bulk_create(crash_list)
        InjuryVehicle.objects.bulk_create(vehicle_list)
            


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