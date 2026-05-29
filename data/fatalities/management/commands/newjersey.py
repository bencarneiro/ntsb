from django.core.management.base import BaseCommand
from data.settings import NEW_JERSEY_PATH
import pandas as pd
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson

def injury_severity_processor(code):
    # print(f"FUNCTION WAS FED {code}")
    code = code.strip()
    if not code:
        return 9
    if int(code) == 1:
        return 4
    if int(code) == 2:
        return 3
    if int(code) == 3:
        return 2
    if int(code) == 4:
        return 1
    return 0
    

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=34).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=34).delete()
        InjuryAccident.objects.filter(state_id=34).delete()
        new_crash_list = []
        new_vehicle_list = []
        new_person_list = []
        crashes = pd.read_csv(f"{NEW_JERSEY_PATH}/2006/crash2006.csv")
        vehicles = pd.read_csv(f"{NEW_JERSEY_PATH}/2006/vehicle2006.csv")
        drivers = pd.read_csv(f"{NEW_JERSEY_PATH}/2006/driver2006.csv")
        occupants = pd.read_csv(f"{NEW_JERSEY_PATH}/2006/occupant2006.csv")
        pedestrians = pd.read_csv(f"{NEW_JERSEY_PATH}/2006/pedestrian2006.csv")
        for x in crashes.index:
            crash_severe_injury_count = 0
            lat = crashes['lat'][x]
            lon = crashes['lon'][x]
            if not lat or not lon:
                lat, lon = None, None
            state_crash_id = crashes['id'][x]
            new_crash = InjuryAccident(
                state_id=34,
                state_accident_id=state_crash_id,
                dt = crashes['dt'][x],
                latitude = lat,
                longitude = lon,
                county = crashes['county'][x],
                city = crashes['city'][x],
                street_1 = crashes['street_1'][x],
                street_2 = crashes['street_2'][x],
                death_count=0
            )
            crash_vehicles = vehicles[vehicles['id']==state_crash_id]
            crash_drivers = drivers[drivers['id']==state_crash_id]
            crash_occupants = occupants[occupants['id']==state_crash_id]
            crash_pedestrians = pedestrians[pedestrians['id']==state_crash_id]
            
            for y in crash_vehicles.index:
                hit_and_run = False
                if crash_vehicles['hit_run'][y] == "Y":
                    print("HIT AND RUN")
                    hit_and_run = True
                veh_num = crash_vehicles['vehicle_number'][y]
                new_vehicle = InjuryVehicle(
                    injury_accident = new_crash,
                    vehicle_number = veh_num,
                    make = f"{crash_vehicles['year'][y]} {crash_vehicles['make'][y]}",
                    model = crash_vehicles['model'][y],
                    hit_and_run = hit_and_run
                )
                new_vehicle_list += [new_vehicle]
                
                for z in crash_occupants.index:
                    if crash_occupants['vehicle_number'][z] == veh_num:
                        if crash_occupants['position'][z] == "01":
                            charge = crash_drivers[crash_drivers['vehicle_number']==veh_num].reset_index()['charge'][0]
                            person_type = "Driver"
                        else:
                            charge = None
                            person_type = "Passenger"
                        injury_severity = injury_severity_processor(crash_occupants['condition'][z])
                        age = crash_occupants['age'][z]
                        if pd.isnull(age):
                            age = None
                        else:
                            try:
                                age = int(age)
                            except:
                                age = None
                        new_person = InjuryPerson(
                            injury_accident=new_crash,
                            injury_vehicle=new_vehicle,
                            person_type = person_type,
                            sex = crash_occupants['sex'][z],
                            age = age,
                            injury_severity = injury_severity
                        )
                        new_person_list += [new_person]
                        if injury_severity == 3:
                            crash_severe_injury_count += 1
            for z in crash_pedestrians.index:
                person_type = "Pedestrian"
                if crash_pedestrians['bike'][z] == "Y":
                    person_type = "Bicycle"
                injury_severity = injury_severity_processor(crash_pedestrians['condition'][z])
                age = crash_pedestrians['age'][z]
                if pd.isnull(age):
                    age = None
                else:
                    try:
                        age = int(age)
                    except:
                        age = None
                new_person = InjuryPerson(
                        injury_accident=new_crash,
                        person_type = person_type,
                        sex = crash_pedestrians['sex'][z],
                        age = age,
                        injury_severity = injury_severity
                    )
                new_person_list += [new_person]
                if injury_severity == 3:
                    crash_severe_injury_count += 1  
            new_crash.severe_injury_count = crash_severe_injury_count
            print(f"crash {state_crash_id} had {crashes['death_count'][x]} deaths and {crash_severe_injury_count} serious injuries")
            new_crash_list += [new_crash]
        InjuryAccident.objects.bulk_create(new_crash_list)
        InjuryVehicle.objects.bulk_create(new_vehicle_list)
        InjuryPerson.objects.bulk_create(new_person_list)



#crash id,dt,lat,lon,city,county,street_1,street_2,crash_type,death_count,severity
#veh id,vehicle_number,year,make,model,hit_run
#occupant id,vehicle_number,position,occupant_number,age,sex,condition
#driver id,vehicle_number,charge
#pedestrian id,bike,age,sex,condition




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