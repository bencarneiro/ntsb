from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import State, County, City, Accident

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        Accident.objects.all().delete()
        City.objects.all().delete()
        County.objects.all().delete()
        State.objects.all().delete()
        cities = pd.read_excel("https://www.gsa.gov/system/files/FRPP_GLC_United_States_May_14_2024.xlsx")
        for x in cities.index:
            try:
                state = State.objects.get(id=cities['State Code'][x])
            except:
                state = State(
                    id=cities['State Code'][x],
                    name=cities['State Name'][x]
                )
                state.save()
            try:
                county = County.objects.get(state=state, county_id=cities['County Code'][x])
            except:
                state_code = str(cities['State Code'][x])
                while len(state_code) < 2:
                    state_code = "0" + state_code
                county_code = str(cities['County Code'][x])
                while len(county_code) < 3:
                    county_code = "0" + county_code
                primary_key = state_code + county_code


                county = County(
                    id=primary_key,
                    state=state, 
                    county_id=cities['County Code'][x],
                    name=cities['County Name'][x]
                )
                county.save()
            try:
                city = City.objects.get(state=state, city_id=cities['City Code'][x])
            except:
                state_code = str(cities['State Code'][x])
                while len(state_code) < 2:
                    state_code = "0" + state_code
                county_code = str(cities['County Code'][x])
                while len(county_code) < 3:
                    county_code = "0" + county_code
                city_code = str(cities['City Code'][x])
                while len(city_code) < 4:
                    city_code = "0" + city_code
                primary_key = state_code + county_code + city_code
                city = City(
                    id=primary_key,
                    state=state,
                    city_id=cities['City Code'][x],
                    name=cities['City Name'][x]
                )
            city.save()
            print(f"saved {city.name}, {city.state.name} in {county.name} county")
            
            
