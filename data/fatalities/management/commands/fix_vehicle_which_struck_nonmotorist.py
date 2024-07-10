from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        csv_2002 = pd.read_csv(f"{CSV_PATH}2002/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2002.index:
            if not csv_2002['VEH_NO'][x]:
                accident = Accident.objects.get(year=2002, st_case=csv_2002['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, person_number=csv_2002['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2002['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"DO NOTHING for {person.id}")
                

        csv_2003 = pd.read_csv(f"{CSV_PATH}2003/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2003.index:
            if not csv_2003['VEH_NO'][x]:
                accident = Accident.objects.get(year=2003, st_case=csv_2003['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, person_number=csv_2003['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2003['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"DO NOTHING for {person.id}")

        csv_2004 = pd.read_csv(f"{CSV_PATH}2004/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2004.index:
            if not csv_2004['VEH_NO'][x]:
                accident = Accident.objects.get(year=2004, st_case=csv_2004['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, person_number=csv_2004['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2004['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"DO NOTHING for {person.id}")

        csv_2005 = pd.read_csv(f"{CSV_PATH}2005/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2005.index:
            if not csv_2005['VEH_NO'][x]:
                accident = Accident.objects.get(year=2005, st_case=csv_2005['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, person_number=csv_2005['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2005['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"DO NOTHING for {person.id}")


        csv_2006 = pd.read_csv(f"{CSV_PATH}2006/FARS2006NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)

        for x in csv_2006.index:
            if not csv_2006['VEH_NO'][x]:
                accident = Accident.objects.get(year=2006, st_case=csv_2006['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, person_number=csv_2006['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2006['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"DO NOTHING for {person.id}")


        csv_2007 = pd.read_csv(f"{CSV_PATH}2007/FARS2007NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)

        for x in csv_2007.index:
            if not csv_2007['VEH_NO'][x]:
                accident = Accident.objects.get(year=2007, st_case=csv_2007['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, person_number=csv_2007['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2007['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"DO NOTHING for {person.id}")


        csv_2008 = pd.read_csv(f"{CSV_PATH}2008/FARS2008NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2008.index:
            if not csv_2008['VEH_NO'][x]:
                accident = Accident.objects.get(year=2008, st_case=csv_2008['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, person_number=csv_2008['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2008['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"DO NOTHING for {person.id}")


        csv_2009 = pd.read_csv(f"{CSV_PATH}2009/FARS2009NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2009.index:
            if not csv_2009['VEH_NO'][x]:
                accident = Accident.objects.get(year=2009, st_case=csv_2009['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, person_number=csv_2009['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2009['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"DO NOTHING for {person.id}")