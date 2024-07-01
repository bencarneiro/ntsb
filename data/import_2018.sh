#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2018_accident > /var/log/2018_accident.txt
python3 manage.py 2018_vehicle > /var/log/2018_vehicle.txt
python3 manage.py 2018_parkwork > /var/log/2018_parkwork.txt
python3 manage.py 2018_person > /var/log/2018_person.txt
python3 manage.py 2018_cevent > /var/log/2018_cevent.txt
python3 manage.py 2018_crashrf > /var/log/2018_crashrf.txt
python3 manage.py 2018_weather > /var/log/2018_weather.txt
python3 manage.py 2018_pbtype > /var/log/2018_pbtype.txt
python3 manage.py 2018_safetyeq > /var/log/2018_safetyeq.txt
python3 manage.py 2018_damage > /var/log/2018_damage.txt
python3 manage.py 2018_distract > /var/log/2018_distract.txt
python3 manage.py 2018_drimpair > /var/log/2018_drimpair.txt
python3 manage.py 2018_factor > /var/log/2018_factor.txt
python3 manage.py 2018_maneuver > /var/log/2018_maneuver.txt
python3 manage.py 2018_violatn > /var/log/2018_violatn.txt
python3 manage.py 2018_vision > /var/log/2018_vision.txt
python3 manage.py 2018_vehiclesf > /var/log/2018_vehiclesf.txt
python3 manage.py 2018_driverrf > /var/log/2018_driverrf.txt
python3 manage.py 2018_pvehiclesf > /var/log/2018_pvehiclesf.txt
python3 manage.py 2018_drugs > /var/log/2018_drugs.txt
python3 manage.py 2018_race > /var/log/2018_race.txt
python3 manage.py 2018_personrf > /var/log/2018_personrf.txt
python3 manage.py 2018_nmcrash > /var/log/2018_nmcrash.txt
python3 manage.py 2018_nmimpair > /var/log/2018_nmimpair.txt
python3 manage.py 2018_nmprior > /var/log/2018_nmprior.txt
