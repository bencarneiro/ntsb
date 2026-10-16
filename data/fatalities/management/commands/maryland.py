from django.core.management.base import BaseCommand
from data.settings import MARYLAND_PATH
import pandas as pd
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson
from datetime import datetime, timezone

def get_inj_sev_code(severity):
    if severity == "Fatal Injury":
        return 4
    if severity == "Suspected Serious Injury":
        return 3
    if severity == "Suspected Minor Injury":
        return 2
    if severity == "Possible Injury":
        return 1
    if severity == "No Apparent Injury":
        return 0
    return 9

def convert_to_iso(date_str: str, time_str: str) -> str:
    if pd.isnull(time_str):
        time_str = "00:00:00"
    datetime_str = f"{date_str} {time_str}"
    parsed_dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return parsed_dt.isoformat()

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=24).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=24).delete()
        InjuryAccident.objects.filter(state_id=24).delete()
        crashes = pd.read_csv(f"{MARYLAND_PATH}/crashes.csv")
        vehicles = pd.read_csv(f"{MARYLAND_PATH}/vehicles.csv")
        drivers = pd.read_csv(f"{MARYLAND_PATH}/drivers.csv")
        passengers = pd.read_csv(f"{MARYLAND_PATH}/passengers.csv")
        nonmotorists = pd.read_csv(f"{MARYLAND_PATH}/nonmotorists.csv")
        accident_list = []
        vehicle_list = []
        person_list = []
        for x in crashes.index:
            death_count = 0
            injury_count = 0
            crash_id = crashes['Reportnumber'][x]
            date = crashes['Crashdate'][x]
            time = crashes['Timeofcrash'][x]
            dt = convert_to_iso(date, time)
            latitude = crashes['Latitude'][x]
            longitude = crashes['Longitude'][x]
            if pd.isnull(latitude) or pd.isnull(longitude):
                latitude, longitude = None, None
            street_2 = crashes['Reference_Roadname'][x]
            if pd.isnull(street_2):
                street_2 = None
            crash_type = crashes['Collisiontype'][x]
            if pd.isnull(crash_type):
                crash_type = "Unknown -"
            if pd.notnull(crashes['Harmfuleventone'][x]):
                crash_type += f" {crashes['Harmfuleventone'][x]}"
            new_injury_accident = InjuryAccident(
                state_id=24,
                state_accident_id = crash_id,
                dt=dt,
                latitude=latitude,
                longitude=longitude,
                county = crashes['CountyOfCrash'][x],
                street_1 = crashes['Road_Name'][x],
                street_2 = street_2,
                crash_type=crash_type,  
            )
            crash_vehicles = vehicles[vehicles['Reportnumber']==crash_id]
            veh_num = 0
            for y in crash_vehicles.index:
                veh_num += 1
                veh_id = crash_vehicles['Vehicleid'][y]
                make = crash_vehicles['Vehiclemake'][y]
                model = crash_vehicles['Vehiclemodel'][y]
                body_type = crash_vehicles['Vehiclebodytype'][y]
                if pd.isnull(make):
                    make = None
                if pd.isnull(model):
                    model = None
                if pd.isnull(body_type):
                    body_type = None
                hit_run = False
                if crash_vehicles['VehicleLeftScene'][y] == "Y":
                    hit_run = True
                new_injury_vehicle = InjuryVehicle(
                    injury_accident=new_injury_accident,
                    vehicle_number = veh_num,
                    make=make,
                    model=model,
                    body_type=body_type,
                    hit_and_run=hit_run,
                )
                vehicle_list += [new_injury_vehicle]
                vehicle_drivers = drivers[drivers['DriverVehicleID']==veh_id]
                vehicle_passengers = passengers[passengers['PassengerVehicleID']==veh_id]
                for z in vehicle_drivers.index:
                    try:
                        age = floor(vehicle_drivers['DriverAge'][z])
                    except:
                        age = None
                    sex = vehicle_drivers['DriverSex'][z]
                    inj_sev = get_inj_sev_code(vehicle_drivers['DriverInjurySeverity'][z])
                    if inj_sev == 3:
                        injury_count += 1
                    if inj_sev == 4:
                        injury_count += 1
                    new_driver = InjuryPerson(
                        injury_accident = new_injury_accident,
                        injury_vehicle = new_injury_vehicle,
                        age = age,
                        sex = sex,
                        injury_severity = inj_sev,
                        person_type = "Driver"
                    )
                    person_list += [new_driver]
                for z in vehicle_passengers.index:
                    try:
                        age = floor(vehicle_passengers['PassengerAge'][z])
                    except:
                        age = None
                    sex = vehicle_passengers['PassengerSex'][z]
                    inj_sev = get_inj_sev_code(vehicle_passengers['PassengerInjurySeverity'][z])
                    if inj_sev == 3:
                        injury_count += 1
                    if inj_sev == 4:
                        injury_count += 1
                    new_passenger = InjuryPerson(
                        injury_accident = new_injury_accident,
                        injury_vehicle = new_injury_vehicle,
                        age = age,
                        sex = sex,
                        injury_severity = inj_sev,
                        person_type = "Passenger"
                    )
                    person_list += [new_passenger]
            crash_nonmotorists = nonmotorists[nonmotorists['Reportnumber']==crash_id]
            for z in crash_nonmotorists.index:
                try:
                    age = floor(crash_nonmotorists['NonMotoristAge'][z])
                except:
                    age = None
                sex = crash_nonmotorists['NonMotoristSex'][z]
                inj_sev = get_inj_sev_code(crash_nonmotorists['NonMotoristInjurySeverity'][z])
                if inj_sev == 3:
                    injury_count += 1
                if inj_sev == 4:
                    injury_count += 1
                person_type = crash_nonmotorists['Description'][z]
                new_nonmotorist = InjuryPerson(
                    injury_accident = new_injury_accident,
                    age = age,
                    sex = sex,
                    injury_severity = inj_sev,
                    person_type = person_type
                )
                person_list += [new_nonmotorist]
            new_injury_accident.death_count = death_count
            new_injury_accident.severe_injury_count = injury_count
            accident_list += [new_injury_accident]

        InjuryAccident.objects.bulk_create(accident_list)
        InjuryVehicle.objects.bulk_create(vehicle_list)
        InjuryPerson.objects.bulk_create(person_list)
