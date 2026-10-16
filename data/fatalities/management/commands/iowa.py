from django.core.management.base import BaseCommand
from data.settings import IOWA_PATH
import pandas as pd
from fatalities.models import InjuryAccident
from datetime import datetime

from django.utils.timezone import make_aware, utc


def convert_to_iso(date_str: str) -> str:
    time_str = "00:00:00"
    datetime_str = f"{date_str} {time_str}"
    parsed_dt = datetime.strptime(datetime_str, "%Y%m%d %H:%M:%S")
    return parsed_dt.isoformat()

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        crash_list = []
        InjuryAccident.objects.filter(state_id=19).delete()
        crashes = pd.read_csv(f"{IOWA_PATH}/iowa")
        for x in crashes.index:
            state_accident_id = crashes['Case Number'][x]
            date = convert_to_iso(crashes['Date of Crash'][x])
            sev = crashes['Crash Severity'][x]
            lat = crashes['Latitude'][x]
            lon = crashes['Longitude'][x]
            if pd.isnull(lat) or pd.isnull(lon):
                lat, lon = None, None
            new_injury_accident = InjuryAccident(
                state_id = 19,
                state_accident_id = state_accident_id,
                latitude=lat,
                longitude=lon,
                crash_severity = sev,
                dt=date
            )
            crash_list += [new_injury_accident]
        InjuryAccident.objects.bulk_create(crash_list)