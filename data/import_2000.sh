export CSV_PATH="/root/ntsb/data/csvs/"

python3 manage.py 2000_accident > /var/log/2000_accident.txt
python3 manage.py 2000_vehicle > /var/log/2000_vehicle.txt
python3 manage.py 2000_person > /var/log/2000_person.txt
python3 manage.py 2000_cevent > /var/log/2000_cevent.txt
python3 manage.py 2000_crashrf > /var/log/2000_crashrf.txt
python3 manage.py 2000_weather > /var/log/2000_weather.txt
python3 manage.py 2000_damage > /var/log/2000_damage.txt
python3 manage.py 2000_drimpair > /var/log/2000_drimpair.txt
python3 manage.py 2000_factor > /var/log/2000_factor.txt
python3 manage.py 2000_maneuver > /var/log/2000_maneuver.txt
python3 manage.py 2000_violatn > /var/log/2000_violatn.txt
python3 manage.py 2000_vision > /var/log/2000_vision.txt
python3 manage.py 2000_vehiclesf > /var/log/2000_vehiclesf.txt
python3 manage.py 2000_driverrf > /var/log/2000_driverrf.txt
python3 manage.py 2000_drugs > /var/log/2000_drugs.txt
python3 manage.py 2000_race > /var/log/2000_race.txt
python3 manage.py 2000_personrf > /var/log/2000_personrf.txt