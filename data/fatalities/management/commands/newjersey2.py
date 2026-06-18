from django.core.management.base import BaseCommand
from data.settings import NEW_JERSEY_PATH
import pandas as pd
from datetime import datetime
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson
from collections import Counter

def injury_severity_processor(code):
    if code == "No Apparent Injury (O)":
        return 0
    if code == "Possible Injury (C)":
        return 1
    if code == "Suspected Minor Injury (B)":
        return 2
    if code == "Suspected Serious Injury (A)":
        return 3
    if code == "Fatal Injury (K)":
        return 4
    return 9
    

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=34, injury_accident__dt__year__gte=2019).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=34, injury_accident__dt__year__gte=2019).delete()
        InjuryAccident.objects.filter(state_id=34, dt__year__gte=2019).delete()
        crashes = pd.read_csv(f"{NEW_JERSEY_PATH}/crash.csv")
        crashes['Vehicle Type'] = crashes['Vehicle Type'].fillna("")
        crashes['Hit and Run'] = crashes['Hit and Run'].fillna("")
        crashes['Citation Issued'] = crashes['Citation Issued'].fillna("")
        crashes['Vehicle Make'] = crashes['Vehicle Make'].fillna("")
        crashes['Vehicle ID'] = crashes['Vehicle ID'].fillna("")
        crashes['Sex'] = crashes['Sex'].fillna("")
        crashes['Age'] = crashes['Age'].fillna("")
        crash_object_list = []
        vehicle_object_list = []
        person_object_list = []
        for x in crashes.index[1:]:
            print(x)
            crash_id = crashes['Crash ID'][x]
            street_1 = crashes['Street Name'][x]
            street_2 = crashes['Intersect Street Name'][x]
            lat = crashes['Latitude'][x]
            lon = crashes['Longitude'][x]
            if not lat or not lon or pd.isnull(lat) or pd.isnull(lon):
                lat, lon = None, None
            county = crashes['County'][x]
            city = crashes['Municipality'][x]
            crash_type = crashes['Crash Type'][x]
            dt = datetime.strptime(crashes['Date & Time of Crash'][x][:-4], "%Y-%m-%dT%H:%M:%S")
            new_injury_accident = InjuryAccident(
                state_id=34,
                state_accident_id=crash_id,
                street_1=street_1,
                street_2=street_2,
                dt=dt,
                latitude=lat,
                longitude=lon,
                county=county,
                city=city,
                crash_type = crash_type,
            )
            vehicle_ids = crashes['Vehicle ID'][x].replace('[','').replace(']','').replace('"','').split(",")
            print(crashes['Vehicle Type'][x])
            vehicle_types = crashes['Vehicle Type'][x].replace('[','').replace(']','').replace('"','').split(",")
            vehicle_makes = crashes['Vehicle Make'][x].replace('[','').replace(']','').replace('"','').split(",")
            hit_and_runs = crashes['Hit and Run'][x].replace('[','').replace(']','').replace('"','').split(",")
            citation_issued = crashes['Citation Issued'][x].replace('[','').replace(']','').replace('"','').split(",")
            unit_ids = crashes['Unit ID'][x].replace("[","").replace("]","").split(",")
            unit_types = crashes['Unit Type'][x].replace("[","").replace("]","").replace('"','').split(",")
            person_ids = crashes['Person ID'][x].replace("[","").replace("]","").split(",")
            person_types = crashes['Person Type'][x].replace("[","").replace("]","").split(",")
            ages = crashes['Age'][x].replace("[","").replace("]","").split(",")
            sexes = crashes['Sex'][x].replace("[","").replace("]","").split(",")
            injury_severities = crashes['Severity Rating (Person)'][x].replace("[","").replace("]","").split(",")
            
            unit_ids_saved = set()
            veh_ids_saved = set()
            person_number = 0
            unit_number = 0
            vehicle_number = 0
            last_unit_id = 0
            death_count = 0
            severe_injury_count = 0
            for person_id in person_ids:
                person_type = person_types[person_number]
                age = ages[person_number]
                try:
                    sex = sexes[person_number]
                except:
                    sex = "Unknown"
                try:
                    injury_severity = injury_severity_processor(injury_severities[person_number])
                except:
                    injury_severity = 9
                if injury_severity == 3:
                    severe_injury_count += 1
                if injury_severity == 4:
                    death_count += 1
                unit_id = unit_ids[person_number]
                unit_type = unit_types[unit_number]
                if unit_type == "Vehicle" and unit_id != last_unit_id:
                    vehicle_id = vehicle_ids[vehicle_number]
                    veh_type = vehicle_types[vehicle_number]
                    veh_make = vehicle_makes[vehicle_number]
                    hitrun = False
                    if hit_and_runs[vehicle_number] == "Yes":
                        hitrun = True
                    citation = citation_issued[vehicle_number]
                    if vehicle_id not in veh_ids_saved:
                        new_injury_vehicle = InjuryVehicle(
                            injury_accident=new_injury_accident,
                            vehicle_number = vehicle_number + 1,
                            make = veh_make,
                            body_type = veh_type,
                            hit_and_run = hitrun,
                            violation=citation
                        )
                        vehicle_object_list += [new_injury_vehicle]
                        veh_ids_saved.add(vehicle_id)
                        vehicle_number += 1
                        if len(veh_ids_saved) == 1:
                            vehicle_number -= 1
                if unit_type == "Vehicle":
                    new_injury_person = InjuryPerson(
                        injury_accident=new_injury_accident,
                        injury_vehicle=new_injury_vehicle,
                        age = age,
                        sex = sex,
                        injury_severity = injury_severity,
                        person_type = person_type
                    )
                    person_object_list += [new_injury_person]
                else:
                    new_injury_person = InjuryPerson(
                        injury_accident=new_injury_accident,
                        age = age,
                        sex = sex,
                        injury_severity = injury_severity,
                        person_type = person_type
                    )
                    person_object_list += [new_injury_person]
                if unit_id not in unit_ids_saved:
                    unit_ids_saved.add(unit_id)
                    unit_number += 1
                    if len(unit_ids_saved) == 1:
                        unit_number -= 1
                person_number += 1
                last_unit_id = unit_id
                new_injury_accident.death_count = death_count
                new_injury_accident.severe_injury_count = severe_injury_count
                crash_object_list += [new_injury_accident]
        InjuryAccident.objects.bulk_create(crash_object_list)
        InjuryVehicle.objects.bulk_create(vehicle_object_list)
        InjuryPerson.objects.bulk_create(person_object_list)






            # unit_keys = []
            # for key in units:
            #     unit_keys += [key]
            # unit_num = 0
            # veh_num = 0
            # unit_members = []
            # for unit_type in unit_types:
            #     unit_number = unit_keys[unit_num]
            #     unit_instances = units[unit_number]
            #     print(f"unit type {unit_type}")
            #     print(F"unit ID: {unit_number}")
            #     print(F"unit Instances: {unit_instances}")
            #     if unit_type == "Vehicle":
            #         print("ITS A VEH")
            #         vehicle_id = vehicle_ids[veh_num]
            #         veh_type = vehicle_types[veh_num]
            #         veh_make = vehicle_makes[veh_num]
            #         hitrun = hit_and_runs[veh_num]
            #         print(vehicle_id)
            #         print(veh_make)
            #         print(veh_type)
            #         print(hitrun)
            #     else:
            #         print("no")
                    

            # ind = 0
            # for vehicle in vehicle_ids:
            #     print("VEHICLE ID")
            #     print(int(vehicle))
            #     veh_type = vehicle_types[ind]
            #     veh_make = vehicle_makes[ind]
            #     hitrun = hit_and_runs[ind]
            #     print(veh_make)
            #     print(veh_type)
            #     print(hitrun)
            
            
            # print("UNIT TYPES")
            # print(unit_types)
            # print(units)

            # unit_num = 1

            # for unit_type in crashes['Unit Type'][x]:
            #     if unit_type == "Vehicle":
            #         print("THIS IS A VEHICLE")
            #     vehicle = crashes['Vehicle ID']
            

            # print("VEHICLE")
            # print(crashes['Unit ID'][x])
            # print(crashes['Unit Type'][x])
            # print(crashes['Vehicle ID'][x])
            # print(crashes['Vehicle Make'][x])
            # # print(crashes['Vehicle Model'][x])
            # print(crashes['Vehicle Type'][x])
            # print(crashes['Hit and Run'][x])
            # print(crashes['Citation Issued'][x])
            # print("PERSON")
            # print(crashes['Occupant ID'][x])
            # print(crashes['Person ID'][x])
            # print(crashes['Person Type'][x])
            # print(crashes['Severity Rating (Person)'][x])
            # print(crashes['Sex'][x])
            # print(crashes['Age'][x])
            # break