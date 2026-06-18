from django.core.management.base import BaseCommand
from data.settings import NEW_JERSEY_PATH
import pandas as pd
from datetime import datetime
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson
from collections import Counter

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
        InjuryPerson.objects.filter(injury_accident__state_id=34, injury_accident__dt__year__gte=2019).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=34, injury_accident__dt__year__gte=2019).delete()
        InjuryAccident.objects.filter(state_id=34, dt__year__gte=2019).delete()
        crashes = pd.read_csv(f"{NEW_JERSEY_PATH}/crash.csv")
        for x in crashes.index[1:]:
            crash_id = crashes['Crash ID'][x]
            street_1 = crashes['Street Name'][x]
            street_2 = crashes['Intersect Street Name'][x]
            lat = crashes['Latitude'][x]
            lon = crashes['Longitude'][x]
            county = crashes['County'][x]
            city = crashes['Municipality'][x]
            crash_type = crashes['Crash Type'][x]
            dt = datetime.strptime(crashes['Date & Time of Crash'][x][:-4], "%Y-%m-%dT%H:%M:%S")

            vehicle_ids = crashes['Vehicle ID'][x].replace('[','').replace(']','').replace('"','').split(",")
            vehicle_types = crashes['Vehicle Type'][x].replace('[','').replace(']','').replace('"','').split(",")
            vehicle_makes = crashes['Vehicle Make'][x].replace('[','').replace(']','').replace('"','').split(",")
            hit_and_runs = crashes['Hit and Run'][x].replace('[','').replace(']','').replace('"','').split(",")
            citation_issued = crashes['Citation Issued'][x].replace('[','').replace(']','').replace('"','').split(",")
            units = dict(Counter(crashes['Unit ID'][x].replace("[","").replace("]","").split(",")))
            unit_types = crashes['Unit Type'][x].replace("[","").replace("]","").replace('"','').split(",")
            unit_keys = []
            for key in units:
                unit_keys += [key]
            unit_num = 0
            veh_num = 0
            unit_members = []
            for unit_type in unit_types:
                unit_number = unit_keys[unit_num]
                unit_instances = units[unit_number]
                print(f"unit type {unit_type}")
                print(F"unit ID: {unit_number}")
                print(F"unit Instances: {unit_instances}")
                if unit_type == "Vehicle":
                    print("ITS A VEH")
                    vehicle_id = vehicle_ids[veh_num]
                    veh_type = vehicle_types[veh_num]
                    veh_make = vehicle_makes[veh_num]
                    hitrun = hit_and_runs[veh_num]
                    print(vehicle_id)
                    print(veh_make)
                    print(veh_type)
                    print(hitrun)
                else:
                    print("no")
                    

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