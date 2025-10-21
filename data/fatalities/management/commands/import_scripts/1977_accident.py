from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import Accident, City, County, State
from fatalities.data_processing import get_data_source, FARS_DATA_CONVERTERS, get_accident_datetime, get_point
import pandas as pd
from datetime import datetime
import numpy as np


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Accident.objects.filter(year=1977).delete()
        missing_counties = []
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
        csv = pd.read_csv(f"{CSV_PATH}1977/ACCIDENT.CSV", encoding='latin-1')
        csv = csv.replace({np.nan: None})
        for x in csv.index:
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            primary_key = f"1977{st_case}"
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
                county_id = int(csv['COUNTY'][x])
                try:
                    if state.name == "FLORIDA" and county_id == 25:
                        county_id = 86
                    county = County.objects.get(state=state, county_id=county_id)
                except:
                    # county_name = input(f"Please enter the name of the county with state code {state_code} and county code {county_code} in all caps: ")
                    county = None
                    missing_counties += [f"state {state.id}, county {county_id}"]
                    # county.save()

            else: 
                county = None
            if csv['CITY'][x] and csv['CITY'][x] not in {9997, 9998, 9999}:
                try:
                    city = City.objects.get(state=state, city_id=csv['CITY'][x])
                except:
                    city = None
            else: 
                city = None
            data_to_save = {
                "id": primary_key,
                "year": 1977,
                "state": state,
                "county": county,
                "city": city
            }
            for model_field_name in accident_model_fields:
                data_source = get_data_source("accident." + model_field_name, 1977)
                if data_source:
                    csv_field_name = data_source.split(".")[1]
                    data_converter_function = FARS_DATA_CONVERTERS["accident." + model_field_name]
                    data_to_save[model_field_name] = data_converter_function(csv[csv_field_name][x], 1977)

            
            print(data_to_save)
            Accident.objects.create(**data_to_save)

        for a in Accident.objects.filter(year=1977).order_by("st_case"):
            dt = get_accident_datetime(a)
            print(dt)
            a.datetime = dt[0]
            a.datetime_is_estimated = dt[1]
            latitude = a.latitude
            longitude = a.longitude
            point = get_point(latitude, longitude)
            if point:
                a.location = point
            else: 
                print("LOCAtION UNKNOWN")
            a.save()
        # print(missing_counties)
                
