#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"

python3 manage.py 2005_accident > /var/log/2005_accident.txt
python3 manage.py 2005_vehicle > /var/log/2005_vehicle.txt
python3 manage.py 2005_parkwork > /var/log/2005_parkwork.txt
python3 manage.py 2005_person > /var/log/2005_person.txt
python3 manage.py 2005_cevent > /var/log/2005_cevent.txt
python3 manage.py 2005_crashrf > /var/log/2005_crashrf.txt
python3 manage.py 2005_weather > /var/log/2005_weather.txt
python3 manage.py 2005_damage > /var/log/2005_damage.txt
python3 manage.py 2005_drimpair > /var/log/2005_drimpair.txt
python3 manage.py 2005_factor > /var/log/2005_factor.txt
python3 manage.py 2005_maneuver > /var/log/2005_maneuver.txt
python3 manage.py 2005_violatn > /var/log/2005_violatn.txt
python3 manage.py 2005_vision > /var/log/2005_vision.txt
python3 manage.py 2005_vehiclesf > /var/log/2005_vehiclesf.txt
python3 manage.py 2005_driverrf > /var/log/2005_driverrf.txt
python3 manage.py 2005_pvehiclesf > /var/log/2005_pvehiclesf.txt
python3 manage.py 2005_drugs > /var/log/2005_drugs.txt
python3 manage.py 2005_race > /var/log/2005_race.txt
python3 manage.py 2005_personrf > /var/log/2005_personrf.txt