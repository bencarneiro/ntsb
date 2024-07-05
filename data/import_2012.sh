#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"

python3 manage.py 2012_accident > /var/log/2012_accident.txt
python3 manage.py 2012_vehicle > /var/log/2012_vehicle.txt
python3 manage.py 2012_parkwork > /var/log/2012_parkwork.txt
python3 manage.py 2012_person > /var/log/2012_person.txt
python3 manage.py 2012_cevent > /var/log/2012_cevent.txt
python3 manage.py 2012_crashrf > /var/log/2012_crashrf.txt
python3 manage.py 2012_weather > /var/log/2012_weather.txt
python3 manage.py 2012_safetyeq > /var/log/2012_safetyeq.txt
python3 manage.py 2012_damage > /var/log/2012_damage.txt
python3 manage.py 2012_distract > /var/log/2012_distract.txt
python3 manage.py 2012_drimpair > /var/log/2012_drimpair.txt
python3 manage.py 2012_factor > /var/log/2012_factor.txt
python3 manage.py 2012_maneuver > /var/log/2012_maneuver.txt
python3 manage.py 2012_violatn > /var/log/2012_violatn.txt
python3 manage.py 2012_vision > /var/log/2012_vision.txt
python3 manage.py 2012_vehiclesf > /var/log/2012_vehiclesf.txt
python3 manage.py 2012_driverrf > /var/log/2012_driverrf.txt
python3 manage.py 2012_pvehiclesf > /var/log/2012_pvehiclesf.txt
python3 manage.py 2012_drugs > /var/log/2012_drugs.txt
python3 manage.py 2012_race > /var/log/2012_race.txt
python3 manage.py 2012_personrf > /var/log/2012_personrf.txt
python3 manage.py 2012_nmcrash > /var/log/2012_nmcrash.txt
python3 manage.py 2012_nmimpair > /var/log/2012_nmimpair.txt
python3 manage.py 2012_nmprior > /var/log/2012_nmprior.txt
