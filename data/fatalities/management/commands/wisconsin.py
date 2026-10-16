from django.core.management.base import BaseCommand
from data.settings import WISCONSIN_PATH
import pandas as pd
from fatalities.models import InjuryAccident
from datetime import datetime

from django.utils.timezone import make_aware, utc


def convert_to_iso(date_str: str) -> str:
    time_str = "00:00:00"
    datetime_str = f"{date_str} {time_str}"
    parsed_dt = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")
    return parsed_dt.isoformat()

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        crash_list = []
        InjuryAccident.objects.filter(state_id=55).delete()
        crashes = pd.read_csv(f"{WISCONSIN_PATH}/wisconsin_crashes_K_A_2000_2026.csv")
        for x in crashes.index:
            print(x)
            state_accident_id = crashes['id'][x]
            properties = crashes['properties'][x]
            print(properties)
            geometry = crashes['geometry'][x]
            print(geometry)
            date = properties.split("'date': '")[1].split("',")[0]
            dt = convert_to_iso(date)
            try:
                street_1 = properties.split("'onrdwy': '")[1].split("'}")[0]
            except:
                street_1 = properties.split("'onrdwy': ")[1].split('",')[0]
            try:
                street_2 = properties.split("'atrdwy': '")[1].split("',")[0]
            except:
                street_2 = properties.split("'atrdwy': ")[1].split('",')[0]

            death_count = int(properties.split(", 'totfatl': '")[1].split("',")[0])
            severity = "Suspected Serious Injury Crash"
            if death_count > 0:
                severity = "Fatal Crash"
            county = properties.split("'cnytname': '")[1].split("',")[0]
            try:
                city = properties.split("'muniname': '")[1].split("',")[0]
            except:
                city = properties.split("'muniname': ")[1].split('",')[0]
            crash_type = properties.split("'flags': ")[1].split(", 'atrdwy':")[0]
            if pd.isnull(geometry):
                lat, lon = None, None
            else:
                lon = geometry.split("{'coordinates': [")[1].split(", ")[0]
                lat = geometry.split("{'coordinates': [")[1].split(", ")[1].split("]")[0]
            print(date)
            new_injury_accident = InjuryAccident(
                state_id = 55,
                city=city,
                county=county,
                state_accident_id = state_accident_id,
                latitude=lat,
                longitude=lon,
                crash_severity = severity,
                dt=dt,
                street_1=street_1,
                street_2=street_2,
                crash_type = crash_type
            )
            crash_list += [new_injury_accident]
            if x % 100 == 0:
                InjuryAccident.objects.bulk_create(crash_list)
                crash_list = []

        InjuryAccident.objects.bulk_create(crash_list)