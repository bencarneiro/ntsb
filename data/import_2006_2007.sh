#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"


python3 manage.py 2007_accident > /var/log/2007_accident.txt
python3 manage.py 2007_vehicle > /var/log/2007_vehicle.txt
python3 manage.py 2007_parkwork > /var/log/2007_parkwork.txt
python3 manage.py 2007_person > /var/log/2007_person.txt
python3 manage.py 2007_cevent > /var/log/2007_cevent.txt
python3 manage.py 2007_crashrf > /var/log/2007_crashrf.txt
python3 manage.py 2007_weather > /var/log/2007_weather.txt
python3 manage.py 2007_damage > /var/log/2007_damage.txt
python3 manage.py 2007_drimpair > /var/log/2007_drimpair.txt
python3 manage.py 2007_factor > /var/log/2007_factor.txt
python3 manage.py 2007_maneuver > /var/log/2007_maneuver.txt
python3 manage.py 2007_violatn > /var/log/2007_violatn.txt
python3 manage.py 2007_vision > /var/log/2007_vision.txt
python3 manage.py 2007_vehiclesf > /var/log/2007_vehiclesf.txt
python3 manage.py 2007_driverrf > /var/log/2007_driverrf.txt
python3 manage.py 2007_pvehiclesf > /var/log/2007_pvehiclesf.txt
python3 manage.py 2007_drugs > /var/log/2007_drugs.txt
python3 manage.py 2007_race > /var/log/2007_race.txt
python3 manage.py 2007_personrf > /var/log/2007_personrf.txt

python3 manage.py 2006_accident > /var/log/2006_accident.txt
python3 manage.py 2006_vehicle > /var/log/2006_vehicle.txt
python3 manage.py 2006_parkwork > /var/log/2006_parkwork.txt
python3 manage.py 2006_person > /var/log/2006_person.txt
python3 manage.py 2006_cevent > /var/log/2006_cevent.txt
python3 manage.py 2006_crashrf > /var/log/2006_crashrf.txt
python3 manage.py 2006_weather > /var/log/2006_weather.txt
python3 manage.py 2006_damage > /var/log/2006_damage.txt
python3 manage.py 2006_drimpair > /var/log/2006_drimpair.txt
python3 manage.py 2006_factor > /var/log/2006_factor.txt
python3 manage.py 2006_maneuver > /var/log/2006_maneuver.txt
python3 manage.py 2006_violatn > /var/log/2006_violatn.txt
python3 manage.py 2006_vision > /var/log/2006_vision.txt
python3 manage.py 2006_vehiclesf > /var/log/2006_vehiclesf.txt
python3 manage.py 2006_driverrf > /var/log/2006_driverrf.txt
python3 manage.py 2006_pvehiclesf > /var/log/2006_pvehiclesf.txt
python3 manage.py 2006_drugs > /var/log/2006_drugs.txt
python3 manage.py 2006_race > /var/log/2006_race.txt
python3 manage.py 2006_personrf > /var/log/2006_personrf.txt