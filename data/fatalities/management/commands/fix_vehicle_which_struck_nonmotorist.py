from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):

        csv_2005 = pd.read_csv(f"{CSV_PATH}2005/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2005.index:
            if not csv_2005['VEH_NO'][x]:
                accident = Accident.objects.get(year=2005, st_case=csv_2005['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2005['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2005['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2005['N_MOT_NO'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")



        csv_2006 = pd.read_csv(f"{CSV_PATH}2006/FARS2006NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2006.index:
            if not csv_2006['VEH_NO'][x]:
                accident = Accident.objects.get(year=2006, st_case=csv_2006['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2006['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2006['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2006['N_MOT_NO'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")



        csv_2007 = pd.read_csv(f"{CSV_PATH}2007/FARS2007NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2007.index:
            if not csv_2007['VEH_NO'][x]:
                accident = Accident.objects.get(year=2007, st_case=csv_2007['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2007['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2007['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2007['N_MOT_NO'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")



        csv_2008 = pd.read_csv(f"{CSV_PATH}2008/FARS2008NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2008.index:
            if not csv_2008['VEH_NO'][x]:
                accident = Accident.objects.get(year=2008, st_case=csv_2008['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2008['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2008['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2008['N_MOT_NO'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")



        csv_2009 = pd.read_csv(f"{CSV_PATH}2009/FARS2009NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2009.index:
            if not csv_2009['VEH_NO'][x]:
                accident = Accident.objects.get(year=2009, st_case=csv_2009['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2009['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2009['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2009['N_MOT_NO'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")



        csv_2010 = pd.read_csv(f"{CSV_PATH}2010/FARS2010NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2010.index:
            if not csv_2010['VEH_NO'][x]:
                accident = Accident.objects.get(year=2010, st_case=csv_2010['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2010['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2010['N_MOT_NO'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2010['N_MOT_NO'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")


        csv_2011 = pd.read_csv(f"{CSV_PATH}2011/FARS2011NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2011.index:
            if not csv_2011['VEH_NO'][x]:
                accident = Accident.objects.get(year=2011, st_case=csv_2011['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2011['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2011['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2011['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")



        csv_2012 = pd.read_csv(f"{CSV_PATH}2012/FARS2012NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2012.index:
            if not csv_2012['VEH_NO'][x]:
                accident = Accident.objects.get(year=2012, st_case=csv_2012['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2012['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2012['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2012['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2013 = pd.read_csv(f"{CSV_PATH}2013/FARS2013NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2013.index:
            if not csv_2013['VEH_NO'][x]:
                accident = Accident.objects.get(year=2013, st_case=csv_2013['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2013['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2013['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2013['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2014 = pd.read_csv(f"{CSV_PATH}2014/FARS2014NationalCSV/PERSON.CSV", encoding='latin-1').fillna(0)
        for x in csv_2014.index:
            if not csv_2014['VEH_NO'][x]:
                accident = Accident.objects.get(year=2014, st_case=csv_2014['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2014['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2014['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2014['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2015 = pd.read_csv(f"{CSV_PATH}2015/FARS2015NationalCSV/person.csv", encoding='latin-1').fillna(0)
        for x in csv_2015.index:
            if not csv_2015['VEH_NO'][x]:
                accident = Accident.objects.get(year=2015, st_case=csv_2015['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2015['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2015['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2015['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2016 = pd.read_csv(f"{CSV_PATH}2016/Person.CSV", encoding='latin-1', low_memory=False).fillna(0)
        for x in csv_2016.index:
            if not csv_2016['VEH_NO'][x]:
                accident = Accident.objects.get(year=2016, st_case=csv_2016['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2016['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2016['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2016['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2017 = pd.read_csv(f"{CSV_PATH}2017/Person.CSV", encoding='latin-1').fillna(0)
        for x in csv_2017.index:
            if not csv_2017['VEH_NO'][x]:
                accident = Accident.objects.get(year=2017, st_case=csv_2017['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2017['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2017['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2017['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2018 = pd.read_csv(f"{CSV_PATH}2018/person.csv", encoding='latin-1', low_memory=False).fillna(0)
        for x in csv_2018.index:
            if not csv_2018['VEH_NO'][x]:
                accident = Accident.objects.get(year=2018, st_case=csv_2018['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2018['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2018['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2018['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2019 = pd.read_csv(f"{CSV_PATH}2019/FARS2019NationalCSV/Person.CSV", encoding='latin-1', low_memory=False).fillna(0)
        for x in csv_2019.index:
            if not csv_2019['VEH_NO'][x]:
                accident = Accident.objects.get(year=2019, st_case=csv_2019['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2019['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2019['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2019['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2020 = pd.read_csv(f"{CSV_PATH}2020/FARS2020NationalCSV/person.csv", encoding='latin-1', low_memory=False).fillna(0)
        for x in csv_2020.index:
            if not csv_2020['VEH_NO'][x]:
                accident = Accident.objects.get(year=2020, st_case=csv_2020['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2020['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2020['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2020['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2021 = pd.read_csv(f"{CSV_PATH}2021/FARS2021NationalCSV/person.csv", encoding='latin-1', low_memory=False).fillna(0)
        for x in csv_2021.index:
            if not csv_2021['VEH_NO'][x]:
                accident = Accident.objects.get(year=2021, st_case=csv_2021['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2021['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2021['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2021['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    
        csv_2022 = pd.read_csv(f"{CSV_PATH}2022/FARS2022NationalCSV/person.csv", encoding='latin-1', low_memory=False).fillna(0)
        for x in csv_2022.index:
            if not csv_2022['VEH_NO'][x]:
                accident = Accident.objects.get(year=2022, st_case=csv_2022['ST_CASE'][x])
                person = Person.objects.get(accident=accident, vehicle=None, parked_vehicle=None, person_number=csv_2022['PER_NO'][x])
                try: 
                    vehicle_which_struck_non_motorist = Vehicle.objects.get(accident=accident, vehicle_number=csv_2022['STR_VEH'][x])
                    person.vehicle_which_struck_non_motorist = vehicle_which_struck_non_motorist
                    person.save()
                    print(f"vehicle which struck nonmotorist fixed for {person.id} hit by veh #{vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"vehicle_which_struck_non_motorist NOTHING for {person.id}")
                try: 
                    parked_vehicle_which_struck_non_motorist = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv_2022['STR_VEH'][x])
                    person.parked_vehicle_which_struck_non_motorist = parked_vehicle_which_struck_non_motorist
                    person.save()
                    print(f"parked vehicle which struck nonmotorist fixed for {person.id} hit by veh #{parked_vehicle_which_struck_non_motorist.vehicle_number}")
                except: 
                    print(f"parked_vehicle_which_struck_non_motorist NOTHING for {person.id}")

                    