#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"

python3 manage.py 2009_accident > /var/log/2009_accident.txt
python3 manage.py 2009_vehicle > /var/log/2009_vehicle.txt
python3 manage.py 2009_parkwork > /var/log/2009_parkwork.txt
python3 manage.py 2009_person > /var/log/2009_person.txt
python3 manage.py 2009_cevent > /var/log/2009_cevent.txt
python3 manage.py 2009_crashrf > /var/log/2009_crashrf.txt
python3 manage.py 2009_weather > /var/log/2009_weather.txt
python3 manage.py 2009_damage > /var/log/2009_damage.txt
python3 manage.py 2009_drimpair > /var/log/2009_drimpair.txt
python3 manage.py 2009_factor > /var/log/2009_factor.txt
python3 manage.py 2013_maneuver > /var/log/2013_maneuver.txt
python3 manage.py 2012_maneuver > /var/log/2012_maneuver.txt
python3 manage.py 2011_maneuver > /var/log/2011_maneuver.txt
python3 manage.py 2010_maneuver > /var/log/2010_maneuver.txt
python3 manage.py 2009_maneuver > /var/log/2009_maneuver.txt
python3 manage.py 2009_violatn > /var/log/2009_violatn.txt
python3 manage.py 2009_vision > /var/log/2009_vision.txt
python3 manage.py 2009_vehiclesf > /var/log/2009_vehiclesf.txt
python3 manage.py 2009_driverrf > /var/log/2009_driverrf.txt
python3 manage.py 2009_pvehiclesf > /var/log/2009_pvehiclesf.txt
python3 manage.py 2009_drugs > /var/log/2009_drugs.txt
python3 manage.py 2009_race > /var/log/2009_race.txt
python3 manage.py 2009_personrf > /var/log/2009_personrf.txt
