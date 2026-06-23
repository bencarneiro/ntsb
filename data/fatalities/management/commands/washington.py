from django.core.management.base import BaseCommand
from data.settings import WASHINGTON_PATH
import pandas as pd
from datetime import datetime
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson
    
def get_inj_sev(sev_str):
    if sev_str in ["Dead on Arrival", "Dead at Scene", "Died at Hospital"]:
        return 4
    if sev_str in ["Suspected Serious Injury"]:
        return 3
    if sev_str in ["Suspected Minor Injury"]:
        return 2
    if sev_str in ["Possible Injury"]:
        return 1
    if sev_str in ["No Apparent Injury"]:
        return 0
    if sev_str in ["'Non-Traffic Fatality"]:
        return 6
    return 9

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=53).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=53).delete()
        InjuryAccident.objects.filter(state_id=53).delete()
        
        crashes = pd.read_csv(f"{WASHINGTON_PATH}/washington_crashes.csv")
        new_crash_list = []
        new_vehicle_list = []
        new_person_list = []
        for x in crashes.index:
            ## CRASH CRASH CRASH CRASH
            state_id = 53
            state_accident_id = crashes['REPORT NUMBER'][x]
            city = crashes['CITY'][x]
            if pd.isnull(city):
                city = None
            county = crashes['COUNTY'][x]
            street_1 = crashes['PRIMARY TRAFFICWAY'][x]
            street_2 = crashes['INTERSECTING TRAFFICWAY'][x]
            if pd.isnull(street_2):
                street_2 = None
            death_count = crashes['TOTAL FATALITIES'][x]
            severe_injury_count = crashes['TOTAL SERIOUS INJURIES'][x]
            lat = crashes['Latitude'][x]
            lon = crashes['Longitude'][x]
            if pd.isnull(lat) or pd.isnull(lon):
                lat, lon = None, None
            crash_type = crashes['FIRST COLLISION TYPE / OBJECT STRUCK'][x]
            if pd.notnull(crashes['SECOND COLLISION TYPE / OBJECT STRUCK'][x]):
                crash_type += " - " + crashes['SECOND COLLISION TYPE / OBJECT STRUCK'][x]
            if pd.notnull(crashes['LIGHTING CONDITIONS'][x]):
                crash_type += " - " + crashes['LIGHTING CONDITIONS'][x]
            if crashes['HIT & RUN'][x] == "Yes":
                crash_type = "Hit and Run - " + crash_type
            date = crashes['DATE'][x]
            month = date.split("/")[0].zfill(2)
            day = date.split("/")[1].zfill(2)
            year = date.split("/")[2]
            dt = datetime.strptime(f"{year}-{month}-{day}T00:00:00", "%Y-%m-%dT%H:%M:%S")
            total_vehicles = crashes['TOTAL VEHICLES'][x]
            total_nonmotorists = crashes['TOTAL PEDESTRIANS INVOLVED'][x] + crashes['TOTAL BICYCLISTS INVOLVED'][x]
            new_injury_crash = InjuryAccident(
                state_id=state_id,
                state_accident_id=state_accident_id,
                city=city,
                county=county,
                street_1=street_1,
                street_2=street_2,
                death_count=death_count,
                severe_injury_count=severe_injury_count,
                number_of_vehicles=total_vehicles,
                number_of_nonmotorists=total_nonmotorists,
                dt=dt,
                latitude=lat,
                longitude=lon,
                crash_type=crash_type
            )
            new_crash_list += [new_injury_crash]

            # VEHICLE VEHICLE VEHICLE VEHICLE

            if pd.notnull(crashes['VEH 1 TYPE'][x]):
                body_type = f"{crashes['VEH 1 TYPE'][x]} - {crashes['VEH 1 STYLE'][x]}"
                make = crashes['VEH 1 MAKE'][x]
                model = crashes['VEH 1 MODEL'][x]
                vehicle_number = 1
                new_injury_vehicle = InjuryVehicle(
                    injury_accident = new_injury_crash,
                    body_type = body_type,
                    make=make,
                    model=model,
                    vehicle_number = 1
                )
                new_vehicle_list += [new_injury_vehicle]

                # DRIVER DRIVER DRIVER DRIVER

                age = crashes['VEH 1 MV DRIVER AGE'][x]
                if pd.isnull(age):
                    age = None
                sex = crashes['VEH 1 MV DRIVER GENDER'][x]
                inj_sev = crashes['VEH 1 MV DRIVER INJURY TYPE'][x]
                new_driver = InjuryPerson(
                    injury_accident=new_injury_crash,
                    injury_vehicle=new_injury_vehicle,
                    person_type="Driver",
                    age=age,
                    sex=sex,
                    injury_severity = get_inj_sev(inj_sev)
                )
                new_person_list += [new_driver]

            # VEHICLE VEHICLE VEHICLE VEHICLE
            if pd.notnull(crashes['VEH 2 TYPE'][x]):
                body_type = f"{crashes['VEH 2 TYPE'][x]} - {crashes['VEH 2 STYLE'][x]}"
                make = crashes['VEH 2 MAKE'][x]
                model = crashes['VEH 2 MODEL'][x]
                vehicle_number = 2
                new_injury_vehicle = InjuryVehicle(
                    injury_accident = new_injury_crash,
                    body_type = body_type,
                    make=make,
                    model=model,
                    vehicle_number = 2
                )
                new_vehicle_list += [new_injury_vehicle]

                # DRIVER DRIVER DRIVER DRIVER

                age = crashes['VEH 2 MV DRIVER AGE'][x]
                if pd.isnull(age):
                    age = None
                sex = crashes['VEH 2 MV DRIVER GENDER'][x]
                inj_sev = crashes['VEH 2 MV DRIVER INJURY TYPE'][x]
                new_driver = InjuryPerson(
                    injury_accident=new_injury_crash,
                    injury_vehicle=new_injury_vehicle,
                    person_type="Driver",
                    age=age,
                    sex=sex,
                    injury_severity = get_inj_sev(inj_sev)
                )
                new_person_list += [new_driver]

            # VEHICLE VEHICLE VEHICLE VEHICLE
            if pd.notnull(crashes['VEH 3 TYPE'][x]):
                body_type = f"{crashes['VEH 3 TYPE'][x]} - {crashes['VEH 3 STYLE'][x]}"
                make = crashes['VEH 3 MAKE'][x]
                model = crashes['VEH 3 MODEL'][x]
                vehicle_number = 3
                new_injury_vehicle = InjuryVehicle(
                    injury_accident = new_injury_crash,
                    body_type = body_type,
                    make=make,
                    model=model,
                    vehicle_number = 3
                )
                new_vehicle_list += [new_injury_vehicle]

                # DRIVER DRIVER DRIVER DRIVER

                age = crashes['VEH 3 MV DRIVER AGE'][x]
                if pd.isnull(age):
                    age = None
                sex = crashes['VEH 3 MV DRIVER GENDER'][x]
                inj_sev = crashes['VEH 3 MV DRIVER INJURY TYPE'][x]
                new_driver = InjuryPerson(
                    injury_accident=new_injury_crash,
                    injury_vehicle=new_injury_vehicle,
                    person_type="Driver",
                    age=age,
                    sex=sex,
                    injury_severity = get_inj_sev(inj_sev)
                )
                new_person_list += [new_driver]


            # PEDESTRIANS PEDESTRIANS PEDESTRIANS PEDESTRIANS

            if pd.notnull(crashes['UNIT 2 PEDESTRIAN ACTION'][x]):
                ped_age = crashes['UNIT 2 PEDESTRIAN AGE'][x]
                if pd.isnull(ped_age):
                    ped_age = None
                ped_sex = crashes['UNIT 2 PEDESTRIAN GENDER'][x]
                ped_inj_sev = crashes['UNIT 2 PEDESTRIAN INJURY TYPE'][x]
                new_pedestrian = InjuryPerson(
                    injury_accident=new_injury_crash,
                    person_type="Pedestrian",
                    age=ped_age,
                    sex=ped_sex,
                    injury_severity=get_inj_sev(ped_inj_sev)
                )
                new_person_list += [new_pedestrian]
                

            if pd.notnull(crashes['UNIT 3 PEDESTRIAN ACTION'][x]):
                ped_age = crashes['UNIT 3 PEDESTRIAN AGE'][x]
                if pd.isnull(ped_age):
                    ped_age = None
                ped_sex = crashes['UNIT 3 PEDESTRIAN GENDER'][x]
                ped_inj_sev = crashes['UNIT 3 PEDESTRIAN INJURY TYPE'][x]
                new_pedestrian = InjuryPerson(
                    injury_accident=new_injury_crash,
                    person_type="Pedestrian",
                    age=ped_age,
                    sex=ped_sex,
                    injury_severity=get_inj_sev(ped_inj_sev)
                )
                new_person_list += [new_pedestrian]
                
            if pd.notnull(crashes['UNIT 1 BICYCLIST ACTION'][x]):
                bike_age = crashes['UNIT 1 BICYCLIST AGE'][x]
                if pd.isnull(bike_age):
                    bike_age = None
                bike_sex = crashes['UNIT 1 BICYCLIST GENDER'][x]
                bike_inj_sev = crashes['UNIT 1 BICYCLIST INJURY TYPE'][x]
                new_cyclist = InjuryPerson(
                    injury_accident=new_injury_crash,
                    person_type="Cyclist",
                    age=bike_age,
                    sex=bike_sex,
                    injury_severity=get_inj_sev(bike_inj_sev)
                )
                new_person_list += [new_cyclist]
            
            if pd.notnull(crashes['UNIT 2 BICYCLIST ACTION'][x]):
                bike_age = crashes['UNIT 2 BICYCLIST AGE'][x]
                if pd.isnull(bike_age):
                    bike_age = None
                bike_sex = crashes['UNIT 2 BICYCLIST GENDER'][x]
                bike_inj_sev = crashes['UNIT 2 BICYCLIST INJURY TYPE'][x]
                new_cyclist = InjuryPerson(
                    injury_accident=new_injury_crash,
                    person_type="Cyclist",
                    age=bike_age,
                    sex=bike_sex,
                    injury_severity=get_inj_sev(bike_inj_sev)
                )
                new_person_list += [new_cyclist]
            
            if pd.notnull(crashes['UNIT 3 BICYCLIST ACTION'][x]):
                bike_age = crashes['UNIT 3 BICYCLIST AGE'][x]
                if pd.isnull(bike_age):
                    bike_age = None
                bike_sex = crashes['UNIT 3 BICYCLIST GENDER'][x]
                bike_inj_sev = crashes['UNIT 3 BICYCLIST INJURY TYPE'][x]
                new_cyclist = InjuryPerson(
                    injury_accident=new_injury_crash,
                    person_type="Cyclist",
                    age=bike_age,
                    sex=bike_sex,
                    injury_severity=get_inj_sev(bike_inj_sev)
                )
                new_person_list += [new_cyclist]

        InjuryAccident.objects.bulk_create(new_crash_list)
        InjuryVehicle.objects.bulk_create(new_vehicle_list)
        InjuryPerson.objects.bulk_create(new_person_list)