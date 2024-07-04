#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2014_accident > /var/log/2014_accident.txt
python3 manage.py 2014_vehicle > /var/log/2014_vehicle.txt
python3 manage.py 2014_parkwork > /var/log/2014_parkwork.txt
python3 manage.py 2014_person > /var/log/2014_person.txt
python3 manage.py 2014_cevent > /var/log/2014_cevent.txt
python3 manage.py 2014_crashrf > /var/log/2014_crashrf.txt
python3 manage.py 2014_weather > /var/log/2014_weather.txt
python3 manage.py 2014_pbtype > /var/log/2014_pbtype.txt
python3 manage.py 2014_safetyeq > /var/log/2014_safetyeq.txt
python3 manage.py 2014_damage > /var/log/2014_damage.txt
python3 manage.py 2014_distract > /var/log/2014_distract.txt
python3 manage.py 2014_drimpair > /var/log/2014_drimpair.txt
python3 manage.py 2014_factor > /var/log/2014_factor.txt
python3 manage.py 2014_maneuver > /var/log/2014_maneuver.txt
python3 manage.py 2014_violatn > /var/log/2014_violatn.txt
python3 manage.py 2014_vision > /var/log/2014_vision.txt
python3 manage.py 2014_vehiclesf > /var/log/2014_vehiclesf.txt
python3 manage.py 2014_driverrf > /var/log/2014_driverrf.txt
python3 manage.py 2014_pvehiclesf > /var/log/2014_pvehiclesf.txt
python3 manage.py 2014_drugs > /var/log/2014_drugs.txt
python3 manage.py 2014_race > /var/log/2014_race.txt
python3 manage.py 2014_personrf > /var/log/2014_personrf.txt
python3 manage.py 2014_nmcrash > /var/log/2014_nmcrash.txt
python3 manage.py 2014_nmimpair > /var/log/2014_nmimpair.txt
python3 manage.py 2014_nmprior > /var/log/2014_nmprior.txt
