from django.core.management.base import BaseCommand
from data.settings import ARIZONA_PATH
import pandas as pd
from fatalities.models import InjuryAccident, InjuryVehicle, InjuryPerson
from datetime import datetime, timezone

from django.utils.timezone import make_aware, utc

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=4).delete()
        InjuryAccident.objects.filter(state_id=4).delete()
        new_crash_list = []
        new_person_list = []
        last_crash_id = None
        last_injury_accident = None
        persons = pd.read_csv(f"{ARIZONA_PATH}/arizona_crash_data.csv").sort_values(by="IncidentID")
        persons[['Sev5_count','Sev4_count']] = persons[['Sev5_count','Sev4_count']].fillna(0)
        for x in persons.index:
            crash_id = persons['IncidentID'][x]
            print(crash_id)
            state_id=4
            dt = persons['AccidentDateTime_Text'][x]
            latitude = persons['Latitude'][x]
            longitude = persons['Longitude'][x]
            city = persons['City'][x]
            county = persons['County'][x]
            street1 = persons['Onroad'][x]
            street2 = persons['CrossingFeature'][x]
            crash_type = persons["IncidentFirstHarmfulEventDesc"][x]
            death_count = persons['Sev5_count'][x]
            severe_injury_count = persons['Sev4_count'][x]
            age = persons['PersonAge'][x]
            if pd.isnull(age):
                age = None
            sex = persons['PersonSex'][x]
            person_type = persons['PersonTypeDesc'][x]
            if persons['PersonInjuryStatusDesc'][x] == "SUSPECTED_SERIOUS_INJURY":
                inj_sev = 3
            if persons['PersonInjuryStatusDesc'][x] == "FATAL":
                inj_sev = 4

            if crash_id != last_crash_id:
                new_injury_accident = InjuryAccident(
                    state_accident_id=crash_id,
                    state_id=state_id,
                    dt=dt,
                    city=city,
                    county=county,
                    street_1=street1,
                    street_2=street2,
                    crash_type=crash_type,
                    death_count=death_count,
                    severe_injury_count=severe_injury_count,
                    latitude=latitude,
                    longitude=longitude
                )
                new_crash_list += [new_injury_accident]
                new_injury_person = InjuryPerson(
                    injury_accident=new_injury_accident,
                    age=age,
                    sex=sex,
                    injury_severity=inj_sev
                )
                new_person_list += [new_injury_person]

            else:
                new_injury_person = InjuryPerson(
                    injury_accident=last_injury_accident,
                    age=age,
                    sex=sex,
                    injury_severity=inj_sev
                )
                new_person_list += [new_injury_person]
            last_crash_id = crash_id
            last_injury_accident = new_injury_accident

        InjuryAccident.objects.bulk_create(new_crash_list)
        InjuryPerson.objects.bulk_create(new_person_list)
