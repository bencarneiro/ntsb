#!/bin/bash

seq 2001 2023 | parallel tippecanoe -f -o ~/app/ntsb/data/fatalities/templates/static/tiles/total_tiles/{}.pmtiles -r1 -y st_case -y fatalities -y month -y day -y year ~/Downloads/total_fatalities_{}.csv

# tippecanoe -f -o ~/app/ntsb/data/fatalities/templates/static/tiles/total_tiles/2023.pmtiles -r1 -y st_case -y fatalities -y month -y day -y year ~/Downloads/total_fatalities_2023.csv
# tippecanoe -f -o ~/app/ntsb/data/fatalities/templates/static/tiles/vehicle_tiles/2023.pmtiles -r1 -y st_case -y fatalities -y month -y day -y year ~/Downloads/vehicle_fatalities_2023.csv
# tippecanoe -f -o ~/app/ntsb/data/fatalities/templates/static/tiles/nonmotorist_tiles/2023.pmtiles -r1 -y st_case -y fatalities -y month -y day -y year ~/Downloads/nonmotorist_fatalities_2023.csv