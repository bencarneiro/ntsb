#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2013_accident > /var/log/2013_accident.txt
python3 manage.py 2013_vehicle > /var/log/2013_vehicle.txt
python3 manage.py 2013_parkwork > /var/log/2013_parkwork.txt
python3 manage.py 2013_person > /var/log/2013_person.txt
python3 manage.py 2013_cevent > /var/log/2013_cevent.txt
python3 manage.py 2013_crashrf > /var/log/2013_crashrf.txt
python3 manage.py 2013_weather > /var/log/2013_weather.txt
python3 manage.py 2013_safetyeq > /var/log/2013_safetyeq.txt
python3 manage.py 2015_pbtype > /var/log/2015_pbtype.txt
python3 manage.py 2015_safetyeq > /var/log/2015_safetyeq.txt
python3 manage.py 2013_damage > /var/log/2013_damage.txt
python3 manage.py 2013_distract > /var/log/2013_distract.txt
python3 manage.py 2013_drimpair > /var/log/2013_drimpair.txt
python3 manage.py 2013_factor > /var/log/2013_factor.txt
python3 manage.py 2013_maneuver > /var/log/2013_maneuver.txt
python3 manage.py 2013_violatn > /var/log/2013_violatn.txt
python3 manage.py 2013_vision > /var/log/2013_vision.txt
python3 manage.py 2013_vehiclesf > /var/log/2013_vehiclesf.txt
python3 manage.py 2013_driverrf > /var/log/2013_driverrf.txt
python3 manage.py 2013_pvehiclesf > /var/log/2013_pvehiclesf.txt
python3 manage.py 2013_drugs > /var/log/2013_drugs.txt
python3 manage.py 2013_race > /var/log/2013_race.txt
python3 manage.py 2013_personrf > /var/log/2013_personrf.txt
python3 manage.py 2013_nmcrash > /var/log/2013_nmcrash.txt
python3 manage.py 2013_nmimpair > /var/log/2013_nmimpair.txt
python3 manage.py 2013_nmprior > /var/log/2013_nmprior.txt
