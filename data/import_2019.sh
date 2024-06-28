#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2019_accident > /var/log/2019_accident.txt
python3 manage.py 2019_vehicle > /var/log/2019_vehicle.txt
python3 manage.py 2019_parkwork > /var/log/2019_parkwork.txt
python3 manage.py 2019_person > /var/log/2019_person.txt
python3 manage.py 2019_cevent > /var/log/2019_cevent.txt
python3 manage.py 2019_crashrf > /var/log/2019_crashrf.txt
python3 manage.py 2019_weather > /var/log/2019_weather.txt
python3 manage.py 2019_pbtype > /var/log/2019_pbtype.txt
python3 manage.py 2019_safetyeq > /var/log/2019_safetyeq.txt
python3 manage.py 2019_damage > /var/log/2019_damage.txt
python3 manage.py 2019_distract > /var/log/2019_distract.txt
python3 manage.py 2019_drimpair > /var/log/2019_drimpair.txt
python3 manage.py 2019_factor > /var/log/2019_factor.txt
python3 manage.py 2019_maneuver > /var/log/2019_maneuver.txt
python3 manage.py 2019_violatn > /var/log/2019_violatn.txt
python3 manage.py 2019_vision > /var/log/2019_vision.txt
python3 manage.py 2019_vehiclesf > /var/log/2019_vehiclesf.txt
python3 manage.py 2019_driverrf > /var/log/2019_driverrf.txt
python3 manage.py 2019_pvehiclesf > /var/log/2019_pvehiclesf.txt
python3 manage.py 2019_drugs > /var/log/2019_drugs.txt
python3 manage.py 2019_race > /var/log/2019_race.txt
python3 manage.py 2019_personrf > /var/log/2019_personrf.txt
python3 manage.py 2019_nmcrash > /var/log/2019_nmcrash.txt
python3 manage.py 2019_nmimpair > /var/log/2019_nmimpair.txt
python3 manage.py 2019_nmdistract > /var/log/2019_nmdistract.txt
python3 manage.py 2019_nmprior > /var/log/2019_nmprior.txt
