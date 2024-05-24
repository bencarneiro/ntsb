from django.core.management.base import BaseCommand
from fatalities.models import ParkedVehicle, Vehicle, Accident, CrashEvent
from fatalities.data_processing import get_data_source
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        CrashEvent.objects.filter(accident__year=2022).delete()
        model_fields =  [ "crash_event_number",
             "area_of_impact_1",
             "area_of_impact_2",
             "sequence_of_events"]

        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/cevent.csv", encoding='latin-1')
        
        for x in csv.index:
            accident = Accident.objects.get(st_case=csv['ST_CASE'][x])
            
  
            data_to_save = {
                "accident": accident,
            }
            try:
                vehicle_1 = Vehicle.objects.get(accident=accident, vehicle_number=csv['VNUMBER1'][x])
            except:
                vehicle_1 = None
            data_to_save['vehicle_1'] = vehicle_1
            try:
                parked_vehicle_1 = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv['VNUMBER1'][x])
            except:
                parked_vehicle_1 = None
            data_to_save['parked_vehicle_1'] = parked_vehicle_1
            try:
                vehicle_2 = Vehicle.objects.get(accident=accident, vehicle_number=csv['VNUMBER2'][x])
            except:
                vehicle_2 = None
            data_to_save['vehicle_2'] = vehicle_2
            try:
                parked_vehicle_2 = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv['VNUMBER2'][x])
            except:
                parked_vehicle_2 = None
            data_to_save['parked_vehicle_2'] = parked_vehicle_2

            for model_field_name in model_fields:
                data_source = get_data_source("crash_event." + model_field_name, 2022)
                csv_field_name = data_source.split(".")[1]
                data_to_save[model_field_name] = csv[csv_field_name][x]
            print(data_to_save)
            CrashEvent.objects.create(**data_to_save)
            # break
