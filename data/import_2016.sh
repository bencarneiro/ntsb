#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2016_accident > /var/log/2016_accident.txt
python3 manage.py 2016_vehicle > /var/log/2016_vehicle.txt
python3 manage.py 2016_parkwork > /var/log/2016_parkwork.txt
python3 manage.py 2016_person > /var/log/2016_person.txt
python3 manage.py 2016_cevent > /var/log/2016_cevent.txt
python3 manage.py 2016_crashrf > /var/log/2016_crashrf.txt
python3 manage.py 2016_weather > /var/log/2016_weather.txt
python3 manage.py 2016_pbtype > /var/log/2016_pbtype.txt
python3 manage.py 2016_safetyeq > /var/log/2016_safetyeq.txt
python3 manage.py 2016_damage > /var/log/2016_damage.txt
python3 manage.py 2016_distract > /var/log/2016_distract.txt
python3 manage.py 2016_drimpair > /var/log/2016_drimpair.txt
python3 manage.py 2016_factor > /var/log/2016_factor.txt
python3 manage.py 2016_maneuver > /var/log/2016_maneuver.txt
python3 manage.py 2016_violatn > /var/log/2016_violatn.txt
python3 manage.py 2016_vision > /var/log/2016_vision.txt
python3 manage.py 2016_vehiclesf > /var/log/2016_vehiclesf.txt
python3 manage.py 2016_driverrf > /var/log/2016_driverrf.txt
python3 manage.py 2016_pvehiclesf > /var/log/2016_pvehiclesf.txt
python3 manage.py 2016_drugs > /var/log/2016_drugs.txt
python3 manage.py 2016_race > /var/log/2016_race.txt
python3 manage.py 2016_personrf > /var/log/2016_personrf.txt
python3 manage.py 2016_nmcrash > /var/log/2016_nmcrash.txt
python3 manage.py 2016_nmimpair > /var/log/2016_nmimpair.txt
python3 manage.py 2016_nmprior > /var/log/2016_nmprior.txt
