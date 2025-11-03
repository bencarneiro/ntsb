tippecanoe -zg -o ~/app/ntsb/data/fatalities/templates/static/tiles/texas/texas_injuries.pmtiles --coalesce-densest-as-needed -y id -y fatalities -y serious_injuries -y dt ~/Downloads/texas_injuries.csv
tippecanoe -zg -o ~/app/ntsb/data/fatalities/templates/static/tiles/texas/texas_fatalities.pmtiles --coalesce-densest-as-needed -y st_case -y fatalities -y serious_injuries -y dt ~/Downloads/texas_fatalities.csv

# tippecanoe -f -o ~/app/ntsb/data/fatalities/templates/static/tiles/total_tiles/2023.pmtiles -r1 -y st_case -y fatalities -y month -y day -y year ~/Downloads/total_fatalities_2023.csv
# tippecanoe -f -o ~/app/ntsb/data/fatalities/templates/static/tiles/vehicle_tiles/2023.pmtiles -r1 -y st_case -y fatalities -y month -y day -y year ~/Downloads/vehicle_fatalities_2023.csv
# tippecanoe -f -o ~/app/ntsb/data/fatalities/templates/static/tiles/nonmotorist_tiles/2023.pmtiles -r1 -y st_case -y fatalities -y month -y day -y year ~/Downloads/nonmotorist_fatalities_2023.csv