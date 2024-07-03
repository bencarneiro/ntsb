#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2015_accident > /var/log/2015_accident.txt
python3 manage.py 2015_vehicle > /var/log/2015_vehicle.txt
python3 manage.py 2015_parkwork > /var/log/2015_parkwork.txt
python3 manage.py 2015_person > /var/log/2015_person.txt
python3 manage.py 2015_cevent > /var/log/2015_cevent.txt
python3 manage.py 2015_crashrf > /var/log/2015_crashrf.txt
python3 manage.py 2016_weather > /var/log/2016_weather.txt
python3 manage.py 2015_weather > /var/log/2015_weather.txt
python3 manage.py 2015_pbtype > /var/log/2015_pbtype.txt
python3 manage.py 2015_safetyeq > /var/log/2015_safetyeq.txt
python3 manage.py 2015_damage > /var/log/2015_damage.txt
python3 manage.py 2015_distract > /var/log/2015_distract.txt
python3 manage.py 2015_drimpair > /var/log/2015_drimpair.txt
python3 manage.py 2015_factor > /var/log/2015_factor.txt
python3 manage.py 2015_maneuver > /var/log/2015_maneuver.txt
python3 manage.py 2015_violatn > /var/log/2015_violatn.txt
python3 manage.py 2015_vision > /var/log/2015_vision.txt
python3 manage.py 2015_vehiclesf > /var/log/2015_vehiclesf.txt
python3 manage.py 2015_driverrf > /var/log/2015_driverrf.txt
python3 manage.py 2015_pvehiclesf > /var/log/2015_pvehiclesf.txt
python3 manage.py 2015_drugs > /var/log/2015_drugs.txt
python3 manage.py 2015_race > /var/log/2015_race.txt
python3 manage.py 2015_personrf > /var/log/2015_personrf.txt
python3 manage.py 2015_nmcrash > /var/log/2015_nmcrash.txt
python3 manage.py 2015_nmimpair > /var/log/2015_nmimpair.txt
python3 manage.py 2015_nmprior > /var/log/2015_nmprior.txt
