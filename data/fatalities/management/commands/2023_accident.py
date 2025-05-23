from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import Accident, City, County, State
from fatalities.data_processing import get_data_source
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Accident.objects.filter(year=2023).delete()
        accident_model_fields = [
            'st_case',
            'number_of_persons_not_in_motor_vehicles',
            'number_of_persons_not_in_motor_vehicles_in_transport',
            'number_of_vehicles',
            'number_of_vehicles_in_transport',
            'number_of_parked_vehicles',
            'number_of_persons_in_motor_vehicles',
            'number_of_persons_in_motor_vehicles_in_transport',
            'month',
            'day',
            'day_of_the_week',
            'year',
            'hour',
            'minute',
            'trafficway_identifier_1',
            'trafficway_identifier_2',
            'route_signing',
            'rural_urban',
            'functional_system',
            'road_owner',
            'national_highway_system',
            'special_jurisdiction',
            'milepoint',
            'latitude',
            'longitude',
            'first_harmful_event',
            'manner_of_collision_of_first_harmful_event',
            'within_interchange_area',
            'relation_to_junction',
            'type_of_intersection',
            'relation_to_road',
            'work_zone',
            'light_condition',
            'atmospheric_condition',
            'school_bus_related',
            'rail_grade_crossing_identifier',
            'ems_notified_hour',
            'ems_notified_minute',
            'ems_arrived_hour',
            'ems_arrived_minute',
            'arrived_at_hospital_hour',
            'arrived_at_hospital_minute',
            'fatalities'
        ]
        csv = pd.read_csv(f"{CSV_PATH}2023/FARS2023NationalCSV/accident.csv", encoding='latin-1')
        for x in csv.index:

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            primary_key = f"2023{st_case}"
            # print(f"saving data for accident #{primary_key}")

            state = State.objects.get(id=csv['STATE'][x])
            state_code = str(csv['STATE'][x])
            while len(state_code) > 2:
                state_code = "0" + state_code
            county_code = str(csv['COUNTY'][x])
            while len(county_code) > 3:
                county_code = "0" + county_code
            city_code = str(csv['CITY'][x])
            while len(city_code) > 4:
                city_code = "0" + city_code

            if csv['COUNTY'][x] and csv['COUNTY'][x] not in {997, 998, 999}:
                try:
                    county = County.objects.get(state=state, county_id=csv['COUNTY'][x])
                except:
                    county = County(
                        id=f"{state_code}{county_code}",
                        state=state, 
                        county_id=csv['COUNTY'][x],
                        name=csv['COUNTYNAME'][x]
                    )
                    county.save()

            else: 
                county = None
            if csv['CITY'][x] and csv['CITY'][x] not in {9997, 9998, 9999}:
                try:
                    city = City.objects.get(state=state, city_id=csv['CITY'][x])
                except:
                    city = City(
                        id=f"{state_code}{city_code}",
                        state=state, 
                        city_id=csv['CITY'][x],
                        name=csv['CITYNAME'][x]
                    )
                    city.save()
            else: 
                city = None
            data_to_save = {
                "id": primary_key,
                "year": 2023,
                "state": state,
                "county": county,
                "city": city
            }
            for model_field_name in accident_model_fields:
                data_source = get_data_source("accident." + model_field_name, 2023)
                csv_field_name = data_source.split(".")[1]
                data_to_save[model_field_name] = csv[csv_field_name][x]
            print(data_to_save)
            Accident.objects.create(**data_to_save)
            
                
