from django.core.management.base import BaseCommand
from data.settings import MASSACHUSETTS_PATH
import pandas as pd
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson
from datetime import datetime, timezone


def convert_to_iso(date_str: str, time_str: str) -> str:
    """Converts a date string (MM/DD/YYYY) and time string (HH:MM AM/PM)

    into a fully formatted ISO 8601 timestamp string.
    """
    if pd.isnull(time_str):
        time_str = "12:00 AM"
    datetime_str = f"{date_str} {time_str}"
    parsed_dt = datetime.strptime(datetime_str, "%m/%d/%Y %I:%M %p")
    return parsed_dt.isoformat()

def get_inj_sev_code(severity):
    if severity == "Fatal injury (K)":
        return 4
    if severity == "Non-fatal injury - Incapacitating":
        return 3
    if severity == "Non-fatal injury - Non-incapacitating":
        return 2
    if severity == "Non-fatal injury - Possible":
        return 1
    if severity == "No injury":
        return 0
    if severity == "Deceased not caused by crash":
        return 6
    return 9

# Example usage:
# convert_to_iso("01/02/2016", "12:39 PM") -> '2016-01-02T12:39:00'

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=25).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=25).delete()
        InjuryAccident.objects.filter(state_id=25).delete()
        new_crash_list = []
        new_vehicle_list = []
        new_person_list = []
        crashes = pd.read_csv(f"{MASSACHUSETTS_PATH}/mass.csv").sort_values(by="Crash Number")
        last_crash_number = None
        last_crash_object = None
        for crash_id in crashes['Crash Number'].unique():
            total_fatalities = 0
            total_severe_injuries = 0
            crash_people = crashes[crashes['Crash Number']==crash_id].reset_index()
            latitude = crash_people['Latitude'][0]
            longitude = crash_people['Longitude'][0]
            street_2 = crash_people['Near Intersection Roadway'][0]
            street_1 = crash_people['Roadway'][0]
            date = crash_people['Crash Date'][0]
            time = crash_people['Crash Time'][0]
            dt = convert_to_iso(date,time)
            city = crash_people["City Town Name"][0]
            county = crash_people["County Name"][0]
            crash_type = crash_people['Vehicle Sequence of Events (All Vehicles)'][0]
            num_veh = crash_people['Number of Vehicles'][0]
            if pd.isnull(num_veh):
                num_veh = None
            if pd.isnull(latitude) or pd.isnull(longitude):
                latitude, longitude = None, None
            #todo add fatality and injury count
            new_injury_accident = InjuryAccident(
                state_id=25,
                state_accident_id=crash_id,
                dt=dt,
                latitude=latitude,
                longitude=longitude,
                city=city,
                county=county,
                street_1=street_1,
                street_2=street_2,
                crash_type=crash_type,
                number_of_vehicles=num_veh,
            )
            veh_ids = crash_people['Vehicle Unit Number'].unique()

            for veh_id in veh_ids:

                if pd.notnull(veh_id):
                    veh_persons = crash_people[crash_people['Vehicle Unit Number'] == veh_id].reset_index()
                    model = ""
                    if pd.notnull(veh_persons['Vehicle Model Year'][0]):
                        model += str(int(veh_persons['Vehicle Model Year'][0]))
                    if pd.notnull(veh_persons['Vehicle Model'][0]):
                        model += veh_persons['Vehicle Model'][0]
                    make = None
                    if pd.notnull(veh_persons['Vehicle Make'][0]):
                        make = veh_persons['Vehicle Make'][0]

                    new_injury_vehicle = InjuryVehicle(
                        vehicle_number = veh_id,
                        injury_accident=new_injury_accident,
                        make = make,
                        model = model,
                        violation = veh_persons['Driver Violation Code'][0]
                    )
                    new_vehicle_list += [new_injury_vehicle]
                    for x in veh_persons.index:
                        inj_sev = get_inj_sev_code(veh_persons['Injury Type'][x])
                        if inj_sev == 3:
                            total_severe_injuries += 1
                        if inj_sev == 4:
                            total_fatalities += 1
                        age = veh_persons['Age'][x]
                        if pd.isnull(age):
                            age = None
                        new_injury_person = InjuryPerson(
                            injury_accident=new_injury_accident,
                            injury_vehicle = new_injury_vehicle,
                            age = age,
                            sex = veh_persons['Sex'][x],
                            person_type=veh_persons['Person Type'][x],
                            injury_severity=inj_sev
                        )
                        new_person_list += [new_injury_person]
                else:
                    veh_persons = crash_people[pd.isnull(crash_people['Vehicle Unit Number'])].reset_index()
                    for x in veh_persons.index:
                        inj_sev = get_inj_sev_code(veh_persons['Injury Type'][x])
                        if inj_sev == 3:
                            total_severe_injuries += 1
                        if inj_sev == 4:
                            total_fatalities += 1
                        age = veh_persons['Age'][x]
                        if pd.isnull(age):
                            age = None
                        new_injury_person = InjuryPerson(
                            injury_accident=new_injury_accident,
                            age = age,
                            sex = veh_persons['Sex'][x],
                            person_type=veh_persons['Person Type'][x],
                            injury_severity=inj_sev
                        )
                        new_person_list += [new_injury_person]
                for x in veh_persons.index:
                    print(veh_id)
                    print(veh_persons['Person Type'][x])
                    print(veh_persons['Injury Type'][x])
            new_injury_accident.death_count = total_fatalities
            new_injury_accident.severe_injury_count = total_severe_injuries
            new_crash_list += [new_injury_accident]
            # break
            

        InjuryAccident.objects.bulk_create(new_crash_list)
        InjuryVehicle.objects.bulk_create(new_vehicle_list)
        InjuryPerson.objects.bulk_create(new_person_list)

# 'Crash Number', 'City Town Name', 'Crash Date', 'Crash Status',
#        'Crash Time', 'Number of Vehicles', 'Total Fatalities', 'County Name',
#        'Hit and Run', 'Vehicle Sequence of Events (All Vehicles)', 'Latitude',
#        'Longitude', 'Street Number', 'Roadway', 'Near Intersection Roadway',
#        'Vehicle Unit Number', 'Vehicle Make', 'Vehicle Model',
#        'Vehicle Model Year', 'Driver Violation Code', 'Person Number', 'Age',
#        'Ejected Description', 'Injury Type', 'Person Type', 'Sex'],

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