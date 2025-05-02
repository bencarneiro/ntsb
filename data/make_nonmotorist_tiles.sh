#!/bin/bash

seq 2001 2023 | parallel tippecanoe -f -o ~/app/ntsb/data/fatalities/templates/static/tiles/nonmotorist_tiles/{}.pmtiles -r1 -y st_case -y fatalities -y month -y day -y year ~/Downloads/nonmotorist_fatalities_{}.csv
