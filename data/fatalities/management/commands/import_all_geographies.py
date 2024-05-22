from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import State, County, City

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
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
                county = County(
                    state=state, 
                    county_id=cities['County Code'][x],
                    name=cities['County Name'][x]
                )
                county.save()

            city = City(
                state=state,
                county=county,
                city_id=cities['City Code'][x],
                name=cities['City Name'][x]
            )
            city.save()
            print(f"saved {city.name}, {city.state.name} in {city.county.name} county")
            
            
