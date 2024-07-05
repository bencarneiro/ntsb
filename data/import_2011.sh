#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"

python3 manage.py 2011_accident > /var/log/2011_accident.txt
python3 manage.py 2011_vehicle > /var/log/2011_vehicle.txt
python3 manage.py 2011_parkwork > /var/log/2011_parkwork.txt
python3 manage.py 2011_person > /var/log/2011_person.txt
python3 manage.py 2011_cevent > /var/log/2011_cevent.txt
python3 manage.py 2011_crashrf > /var/log/2011_crashrf.txt
python3 manage.py 2011_weather > /var/log/2011_weather.txt
python3 manage.py 2011_safetyeq > /var/log/2011_safetyeq.txt
python3 manage.py 2011_damage > /var/log/2011_damage.txt
python3 manage.py 2011_distract > /var/log/2011_distract.txt
python3 manage.py 2011_drimpair > /var/log/2011_drimpair.txt
python3 manage.py 2011_factor > /var/log/2011_factor.txt
python3 manage.py 2011_maneuver > /var/log/2011_maneuver.txt
python3 manage.py 2011_violatn > /var/log/2011_violatn.txt
python3 manage.py 2011_vision > /var/log/2011_vision.txt
python3 manage.py 2011_vehiclesf > /var/log/2011_vehiclesf.txt
python3 manage.py 2011_driverrf > /var/log/2011_driverrf.txt
python3 manage.py 2011_pvehiclesf > /var/log/2011_pvehiclesf.txt
python3 manage.py 2011_drugs > /var/log/2011_drugs.txt
python3 manage.py 2011_race > /var/log/2011_race.txt
python3 manage.py 2011_personrf > /var/log/2011_personrf.txt
python3 manage.py 2011_nmcrash > /var/log/2011_nmcrash.txt
python3 manage.py 2011_nmimpair > /var/log/2011_nmimpair.txt
python3 manage.py 2011_nmprior > /var/log/2011_nmprior.txt
