from django.core.management.base import BaseCommand
from data.settings import VIRGINIA_PATH
import pandas as pd
from datetime import datetime
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson
    
def format_military_time(time_int: int) -> str:
    time_str = str(time_int).zfill(4)

    if len(time_str) > 4:
        raise ValueError(f"Invalid military time: {time_int}")

    hours = int(time_str[0:2])
    minutes = int(time_str[2:4])

    if not (0 <= hours <= 23):
        raise ValueError(f"Invalid hours: {hours}")
    if not (0 <= minutes <= 59):
        raise ValueError(f"Invalid minutes: {minutes}")

    return f"{hours:02d}:{minutes:02d}:00"

def get_injury_severity(code):
    if code == "K":
        return 4
    if code == "A":
        return 3
    if code == "B":
        return 2
    if code == "C":
        return 1
    if code == "PDO":
        return 0
    return 9

# the rows don't line up between the basic and detail spreadsheets

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=51).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=51).delete()
        InjuryAccident.objects.filter(state_id=51).delete()
        
        basic = pd.read_csv(f"{VIRGINIA_PATH}/basic.csv").sort_values(by="Document Nbr").reset_index()
        basic = basic[(basic['Crash Severity'] == "A") | (basic['Crash Severity'] == "K")]
        detail = pd.read_csv(f"{VIRGINIA_PATH}/detail.csv").sort_values(by="Document_Nbr").reset_index()
        print(len(basic))
        print(len(detail))
        new_crash_list = []
        new_vehicle_list = []
        new_person_list = []

        for x in basic.index:
            state_accident_id = basic['Document Nbr'][x]
            print(state_accident_id)
            lat = basic['LAT'][x]
            lon = basic['LON'][x]
            street_1 = basic['Route or Street Name'][x]
            date = basic['Crash Date'][x]
            month = date.split("/")[0].zfill(2)
            day = date.split("/")[1].zfill(2)
            year = date.split("/")[2].split(" ")[0]
            time = format_military_time(basic['Crash Military Time'][x])
            dt = datetime.strptime(f"{year}-{month}-{day}T{time}", "%Y-%m-%dT%H:%M:%S")
            city = basic['MPO Name'][x]
            death_count = basic['K_People'][x]
            severe_injury_count = basic['A_People'][x]
            crash_severity = basic['Crash Severity'][x]
            crash_type = detail['Most_Harmful_Crash_Event_Cd'][x]
            if pd.isnull(city):
                city = None
            else:
                city = f"{city} (Metro)"
            
            new_injury_crash = InjuryAccident(
                state_accident_id=state_accident_id,
                state_id=51,
                dt=dt,
                street_1=street_1,
                latitude=lat,
                longitude=lon,
                death_count=death_count,
                severe_injury_count=severe_injury_count,
                crash_type=crash_type,
                city=city,
                crash_severity=crash_severity
            )
            new_crash_list += [new_injury_crash]
                
            vehicles = detail['Vehiclenumber'][x].split(";")
            drivers = detail['Driver_VehicleNumber'][x] 
            if pd.isnull(drivers):
                drivers = []
            else:
                drivers = drivers.split(";")
            passengers = detail['Pass_vehiclenumber'][x] 
            if pd.isnull(passengers):
                passengers = []
            else:
                passengers = passengers.split(";")
            pedestrians = detail['Ped_Number'][x] 
            if pd.isnull(pedestrians):
                pedestrians = []
            else:
                pedestrians = str(pedestrians).split(";")
            bicycles = detail['Bike_VehicleNumber'][x] 
            if pd.isnull(bicycles):
                bicycles = []
            else:
                bicycles = str(bicycles).split(";") 
            vehicle_dict = {}
            print(state_accident_id)
            print("vehicles")
            print(vehicles)
            print("drivers")
            print(drivers)
            print("passengers")
            print(passengers)
            print("pedestrians")
            print(pedestrians)
            print("bicycles")
            print(bicycles)
            for vehicle_number in vehicles:
                vehicle_number = int(vehicle_number)
                index = int(vehicle_number) - 1
                try:
                    body_type = detail['Vehicle_Body_Type_Cd'][x].split(";")[index]
                except:
                    body_type = "Unknown"
                if "Bicycle" in body_type:
                    continue
                try:
                    make = detail['Vehicle_Make_Nm'][x].split(";")[index]
                except:
                    make = None
                try:
                    year = detail['Vehicle_Year_Nbr'][x].split(";")[index]
                    model = detail['Vehicle_Model_Nm'][x].split(";")[index]
                    yearmodel = f"{year} {model}"
                except:
                    yearmodel = None
                try:
                    violation = detail['Summons_Issued_Cd'][x].split(";")[index]
                except:
                    violation = None
                try:
                    hit_run = False
                    if detail['Driver_Fled_Scene_Ind'][x].split(";")[index] == "Yes":
                        hit_run = True 
                except:
                    hit_run = False
                new_vehicle = InjuryVehicle(
                    vehicle_number=vehicle_number,
                    injury_accident=new_injury_crash,
                    body_type = body_type,
                    make = make,
                    model = yearmodel,
                    violation=violation,
                    hit_and_run=hit_run
                )
                new_vehicle_list += [new_vehicle]
                vehicle_dict[vehicle_number] = new_vehicle
            for vehicle_number in drivers:
                vehicle_number = int(vehicle_number)
                if vehicle_number not in vehicle_dict:
                    continue
                index = int(vehicle_number) - 1
                try:
                    age = detail['Driver_Age'][x].split(";")[index]
                except:
                    age = None 
                try:
                    sex = detail['Driver_Gender'][x].split(";")[index]
                except:
                    sex = None
                try:
                    inj_sev = get_injury_severity(detail['Driver_InjuryType'][x].split(";")[index])
                except:
                    inj_sev = 9
                # print(f"{age} {sex} injured? {inj_sev}")
                new_driver = InjuryPerson(
                    injury_accident = new_injury_crash,
                    injury_vehicle = vehicle_dict[vehicle_number],
                    age = age,
                    sex = sex,
                    injury_severity = inj_sev,
                    person_type = "Driver"
                )
                new_person_list += [new_driver]
            index = 0
            for vehicle_number in passengers:
                vehicle_number = int(vehicle_number)
                if vehicle_number not in vehicle_dict:
                    continue
                try:
                    age = int(str(detail['Pass_age'][x]).split(";")[index])
                except:
                    age = None
                try:
                    sex = detail['Pass_gender'][x].split(";")[index]
                except:
                    sex = "Unknown"
                inj_sev = get_injury_severity(str(detail['Pass_InjuryType'][x]).split(";")[index])
                index += 1
                new_passenger = InjuryPerson(
                    injury_accident = new_injury_crash,
                    injury_vehicle = vehicle_dict[vehicle_number],
                    age=age,
                    sex=sex,
                    injury_severity=inj_sev,
                    person_type = "Passenger"
                )
                new_person_list += [new_passenger]
            index = 0
            for pedestrian in pedestrians:
                try:
                    age = int(str(detail['PED_Age'][x]).split(";")[index])
                except:
                    age = None
                sex = detail['Ped_Gender'][x].split(";")[index]
                inj_sev = get_injury_severity(str(detail['Ped_InjuryType'][x]).split(";")[index])
                new_pedestrian = InjuryPerson(
                    injury_accident=new_injury_crash,
                    age=age,
                    sex=sex,
                    injury_severity=inj_sev,
                    person_type = "Pedestrian"
                )
                new_person_list += [new_pedestrian]
                index += 1
            index = 0
            for bike in bicycles:
                try:
                    age = int(str(detail['Bike_Age'][x]).split(";")[index])
                except:
                    age = None
                sex = detail['Bike_Gender'][x].split(";")[index]
                inj_sev = get_injury_severity(str(detail['Bike_InjuryType'][x]).split(";")[index])
                new_bicycle = InjuryPerson(
                    injury_accident=new_injury_crash,
                    age=age,
                    sex=sex,
                    injury_severity=inj_sev,
                    person_type = "Bicycle"
                )
                new_person_list += [new_bicycle]
                index += 1
    
            # if x > 10:
            #     break
        InjuryAccident.objects.bulk_create(new_crash_list)
        InjuryVehicle.objects.bulk_create(new_vehicle_list)
        InjuryPerson.objects.bulk_create(new_person_list)