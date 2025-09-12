from django.core.management.base import BaseCommand
from data.settings import ACCIDENT_CSV_PATHS, CSV_PATH
from fatalities.models import Accident, County, State
import pandas as pd

import csv


def stringify_county_code(state_id, county_id):
    state_id = str(state_id)
    while len(state_id) < 2:
        state_id = "0" + state_id
    county_id = str(county_id)
    while len(county_id) < 3:
        county_id = "0" + county_id

    return state_id + county_id

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        states = State.objects.all()
        for state in states:
            try:
                null_county = County.objects.get(id=int(state.id * 1000 + 999))
                null_county_crashes = Accident.objects.filter(county=null_county)
                for crash in null_county_crashes:
                    crash.county = None
                    crash.save()
            except:
                null_county = County(id=int(1000 * state.id + 999),county_id=999,state=state, name="Unknown County")
                null_county.save()
            # break
        alaska = State.objects.get(id=2)
        former_alaskan_counties = [
            (2010, "(FORMER) Aleutian Islands Census Area"),
            (2030, "(FORMER) Angoon Division"),
            (2040, "(FORMER) Barrow Division"),
            (2080, "(FORMER) Cordova-McCarthy Division"),
            (2120, "(FORMER) Kenai-Cook Inlet Division"),
            (2160, "(FORMER) Kuskokwim Division"),
            (2190, "(FORMER) Outer Ketchikan Division"),
            (2200, "(FORMER) Prince of Wales Division"),
            (2210, "(FORMER) Seward"),
            (2230, "(FORMER) Skagway-Yakutat Division"),
            (2250, "(FORMER) Upper Yukon Division"),
            (2260, "(FORMER) Valdez-Chitina-Whittier Division")
        ]
        for ak in former_alaskan_counties:
            try:
                new_ak_county = County(state=alaska, id=ak[0], county_id = ak[0] - 2000, name=ak[1])
                new_ak_county.save()
                print(f"new alaskan county saved {new_ak_county.name}")
            except:
                print("new alaska county already exists")
            


        result_dict = {}
        for year in range(1975,2024):
            accident_csv = pd.read_csv(f"{CSV_PATH}{ACCIDENT_CSV_PATHS[year]}", encoding="latin-1")
            countyless_crashes = Accident.objects.filter(year=year, county__isnull=True)
            for crash in countyless_crashes:
                st_case = str(crash.id)[4:]
                csv_crash = accident_csv[accident_csv['ST_CASE']==int(st_case)].reset_index()
                state_id = csv_crash['STATE'][0]
                county_id = csv_crash['COUNTY'][0]
                if int(county_id) == 0 or int(county_id) == 997 or int(county_id == 998):
                    county_id = 999
                full_county_id = stringify_county_code(state_id, county_id)
                if full_county_id == "02140":
                    full_county_id = "02188"
                if full_county_id == "13510":
                    full_county_id = "13215"
                if full_county_id == "46131":
                    full_county_id = "46071"
                if full_county_id == "29193":
                    full_county_id = "29186"
                if full_county_id == "51039":
                    full_county_id = "51036"
                try:
                    c = County.objects.get(id=int(full_county_id))
                    crash.county = c
                    crash.save()
                except:
                    unknown_county = County.objects.get(state_id=state_id, county_id=999)
                    crash.county=unknown_county
                    crash.save()
                    if full_county_id in result_dict:
                        result_dict[full_county_id] += 1
                    else:
                        result_dict[full_county_id] = 1
        print(result_dict)
        with open('countyless_crashes.csv', 'w', newline='') as file:
            for key in result_dict:
                print(key)
                print(result_dict[key])
                file.write(f"{key}, {result_dict[key]}\n")
            