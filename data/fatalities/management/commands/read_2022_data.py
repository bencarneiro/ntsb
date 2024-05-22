from django.core.management.base import BaseCommand
from fatalities.models import Accident, City, County, State
from fatalities.data_processing import get_data_source
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        accident_model_fields = [
            'st_case',
            'number_of_persons_not_in_motor_vehicles',
            'number_of_persons_not_in_motor_vehicles_in_transport',
            'number_of_vehicles',
            'number_of_vehicles_in_transit',
            'number_of_parked_vehicles',
            'number_of_persons_in_motor_vehicles',
            'number_of_persons_in_motor_vehicles_in_transport',
            'month',
            'day',
            'day_of_the_week',
            'year',
            'hour',
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
            'at_intersection',
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
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/accident.csv", encoding='latin-1')
        for x in csv.head(30).index:
            print(csv['STATE'][x])
            print(csv['COUNTY'][x])
            print(csv['CITY'][x])
            
            state = State.objects.get(id=csv['STATE'][x])
            if csv['COUNTY'][x]:
                county = County.objects.get(state=state, county_id=csv['COUNTY'][x])
            else: 
                county = None
            if csv['CITY'][x]:
                city = City.objects.get(state=state, city_id=csv['CITY'][x])
            else: 
                city = None
            data_to_save = {
                "year": 2022,
                "state": state,
                "county": county,
                "city": city
            }
            for model_field_name in accident_model_fields:
                data_source = get_data_source("accident." + model_field_name, 2022)
                csv_field_name = data_source.split(".")[1]
                data_to_save[model_field_name] = csv[csv_field_name][x]
            print(data_to_save)
            Accident.objects.create(**data_to_save)
            
                
