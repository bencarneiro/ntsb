from fatalities.data_dictionary import FARS_DATA_DICTIONARY
from fatalities.models import City, County, State, Vehicle

def get_column_history(column):
    return FARS_DATA_DICTIONARY[column]

def get_data_source(column, year):
    for period in FARS_DATA_DICTIONARY[column]:
        if period['range']['start'] <= year and ((not period['range']['end']) or period['range']['end'] >= year):
            return period['key']
    return None,

def get_multiple_data_sources(column, year):
    locations = []
    for period in FARS_DATA_DICTIONARY[column]:
        if period['range']['start'] <= year and ((not period['range']['end']) or period['range']['end'] >= year):
            locations += [period['key']]
    return locations
    
def get_county(state_id, county_id):
    return County.objects.get(state_id=state_id, county_id=county_id)

def year_converter(year_field, year):
    if year < 1998:
        return 1900 + int(year_field)
    return int(year_field)

def route_signing_converter(route_signing, year):
    if year < 1981:
        if route_signing in [2,5]:
            return 8
        if route_signing == 3:
            return 2
        if route_signing == 4:
            return 3
        if route_signing == 6:
            return 4
        if route_signing == 7:
            return 6
            
    return route_signing 

def land_use_converter(land_use, year):
    if year < 1987:
        return land_use
    if year < 2015:
        if land_use in {1,2,3,4,5,6,9}:
            return 1
        if land_use in {11,12,13,14,15,16,19}:
            return 2
        return 9
    return land_use

def functional_system_converter(functional_system, year):
    if year < 1981:
        return None
    if year < 1987:
        if functional_system in {6}:
            return 5
        if functional_system in {7}:
            return 6
        if functional_system in {8}:
            return 7
        if functional_system in {9}:
            return 99
        return functional_system
    if year < 2015:
        if functional_system in {1,11}:
            return 1
        if functional_system in {12}:
            return 2
        if functional_system in {2,13}:
            return 3
        if functional_system in {3,14}:
            return 4
        if functional_system in {4,15}:
            return 5
        if functional_system in {5}:
            return 6
        if functional_system in {6,16}:
            return 7
        if functional_system in {9,19,99}:
            return 99      
    return functional_system 
    
def dms2dd(degrees, minutes, seconds):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    return dd

def latitude_converter(latitude, year):
    if year < 1999:
        return None
    if year < 2010:
        if isinstance(latitude, int):
            if latitude > 72000000:
                return None
            str_lat = str(latitude)
            return dms2dd(str_lat[:2],str_lat[2:4],str_lat[4:])
            
        if isinstance(latitude, float):
            return latitude
    if latitude > 72:
        return None
    return latitude


def longitude_converter(longitude, year):
    if year < 1999:
        return None
    if year < 2010:
        if isinstance(longitude, int):
            if longitude > 179000000:
                return None
            str_lat = str(longitude)
            if len(str_lat) == 9:
                return -1 * dms2dd(str_lat[:3],str_lat[3:5],str_lat[5:])
            else:
                return -1 * dms2dd(str_lat[:2],str_lat[2:4],str_lat[4:])
        if isinstance(longitude, float):
            return longitude
    if longitude > 179:
        return None
    return longitude

def soe_converter(soe, year):
    if year < 1982:
        if soe in {16}:
            return 18
        if soe in {17}:
            return 21
        if soe in {18}:
            return 19
        if soe in {19}:
            return 32
        if soe in {20}:
            return 33
        if soe in {21}:
            return 29
        if soe in {22}:
            return 35
        if soe in {23}:
            return 38
        if soe in {25}:
            return 30
        if soe in {26}:
            return 59
        if soe in {27}:
            return 42
        if soe in {28}:
            return 30
        if soe in {29}:
            return 31
        if soe in {30}:
            return 20
        if soe in {31}:
            return 43
        if soe in {32}:
            return 21
        if soe in {33}:
            return 23
        return soe
    
    if soe in {13}:
        return 12
    if soe in {22}:
        return 23
    if soe in {27,28}:
        return 59
    if soe in {29}:
        return 30
    if soe in {36,37}:
        return 35
    
    return soe

def manner_of_collision_converter(moc, year):
    if year < 2002:
        if moc in {3}:
            return 10
        if moc in {4}:
            return 6
        if moc in {5}:
            return 7
        if moc in {6}:
            return 8
        if moc in {9}:
            return 99
        return moc
    if year < 2010:
        if moc in {3,4,5}:
            return 6
    return moc

def within_interchange_area_converter(value, year):
    if year < 2010:
        if value in {1,2,3,4,5,6,7,8,9}:
            return 0
        if value in {10,11,12,13,14,15,19}:
            return 1
        return 9
    return value

def relation_to_junction_converter(value, year): 
    if year < 1991:
        if value in {4}:
            return 2
        if value in {5}:
            return 4
        if value in {6}:
            return 5
        if value in {7}:
            return 6
        if value in {8}:
            return 7
        if value in {9}:
            return 99
        return value
    if year < 2010:
        if value in {9}:
            return 99
        if value in {10}:
            return 2
        if value in {11}:
            return 3
        if value in {12}:
            return 4
        if value in {13}:
            return 5
        if value in {14}:
            return 7
        if value in {15}:
            return 19   
        
    return value

def type_of_intersection_converter(value, year):
    if year < 2013:
        if value in {8}:
            return 98
        if value in {9}:
            return 99
    return value

def relation_to_road_converter(value, year):
    if year < 1998:
        if value in {9}:
            return 99
        return value
    
def work_zone_converter(value, year):
    if year < 1982:
        if value in {3}:
            return 4
        return value
    if value in {8}:
        return 0
    return value

def light_condition_converter(value, year):
    if year < 1980:
        if value in {6}:
            return 5
    return value

def atmospheric_condition_converter(value, year):
    if year < 1980:
        if value in {7}:
            return [10]
        if value in {9}:
            return [99]
        return [value]
    if year < 2007:
        if value in {8}:
            return [5]
        if value in {6}:
            return [2,5]
        if value in {7}:
            return [3,5]
        if value in {9}:
            return [99]
        return [value]
    if year < 2010:
        if value in {0}:
            return 1
        if value in {9}:
            return [99]
    return [value]

def school_bus_related_converter(value, year):
    if value in {1}:
        return True
    return False

def hit_and_run_converter(value, year):
    if value in {1,2,3,4,5}:
        return 1
    if value in {0,8,9}:
        return 0
    return value

def registration_state_converter(value, year):
    if year < 2008:
        if value in {94}:
            return 93
        if value in {95,96}:
            return 94
    return value

def model_year_converter(value, year):
    if year < 1998:
        if value in {99}:
            return 9999
        return int("19"+str(value))
    return value

def ncsa_model_converter(model, year):
    if year < 1991:
        if model in {57}:
            return 59
        if model in {60,61,62,63,64,65,69}:
            return model + 10
        if model in {67}:
            return 76
        if model in {70}:
            return 78
        if model in {88}:
            return 89
    return model

def ncsa_body_type_converter(value, year):
    if year < 1982:
        if value in {3}:
            return 4
        if value in {4}:
            return 7
        if value in {5}:
            return 10
        if value in {7}:
            return 14
        if value in {8}:
            return 9
        if value in {15}:
            return 80
        if value in {16}:
            return 81
        if value in {17}:
            return 88
        if value in {18}:
            return 89
        if value in {25,26,27}:
            return value + 25
        if value in {28,29}:
            return value + 30
        if value in {35}:
            return 91
        if value in {36}:
            return 92
        if value in {37}:
            return 97
        if value in {38}:
            return 93
        if value in {39}:
            return 11
        if value in {40}:
            return 12
        if value in {41}:
            return 73
        if value in {42}:
            return 78
        if value in {43}:
            return 14
        if value in {44}:
            return 79
        if value in {45}:
            return 79
        if value in {50}:
            return 39
        if value in {51}:
            return 29
        if value in {52}:
            return 16
        if value in {53}:
            return 61
        if value in {54}:
            return 62
        if value in {55}:
            return 63
        if value in {56}:
            return 64
        if value in {57,58,59}:
            return 66
        if value in {60}:
            return 79
        return value
    if year < 1991:
        if value in {12}:
            return 14
        if value in {13}:
            return 12
        if value in {14}:
            return 13
        if value in {20}:
            return 80
        if value in {21}:
            return 81
        if value in {27}:
            return 82
        if value in {28}:
            return 88
        if value in {29}:
            return 89
        if value in {30,31,32,38,39}:
            return value + 20
        if value in {40}:
            return 22
        if value in {41}:
            return 22
        if value in {42}:
            return 21
        if value in {48}:
            return 28
        if value in {49}:
            return 29
        if value in {50}:
            return 39
        if value in {51}:
            return 39
        if value in {52}:
            return 42
        if value in {53}:
            return 40
        if value in {54}:
            return 41
        if value in {55}:
            return 16
        if value in {56}:
            return 15
        if value in {58}:
            return 48
        if value in {59}:
            return 49
        if value in {67}:
            return 19
        if value in {69}:
            return 49
        if value in {70}:
            return 61
        if value in {71}:
            return 62
        if value in {72}:
            return 63
        if value in {73}:
            return 65
        if value in {74}:
            return 66
        if value in {75}:
            return 78
        if value in {76}:
            return 78
        if value in {77}:
            return 73
        if value in {78}:
            return 64
        if value in {80}:
            return 91
        if value in {81}:
            return 92
        if value in {82}:
            return 97
        if value in {83}:
            return 93
        if value in {88,89,90}:
            return 9
        return value
    if year < 1994:
        if value in {8}:
            return 9
    if value in {23,24,25}:
        return 21
    if value in {30,31}:
        return 34
    if value in {68}:
        return 64
    return value

def vehicle_trailing_converter(value, year):
    if year < 1982:
        if value in {1}:
            return 4
        return value
    if year < 1983:
        if value in {5}:
            return 4
        return value
    return value

def vehicle_configuration_converter(value, year):
    if year < 1995:
        if value in {3}:
            return 4
        if value in {4}:
            return 5
        if value in {5}:
            return 6
        if value in {6}:
            return 19
        if value in {7}:
            return 21
        if value in {9}:
            return 99
        return value
    if year < 2001:
        if value in {7}:
            return 19
        if value in {8}:
            return 21
        if value in {9}:
            return 99
        return value
    return value

def cargo_body_type_converter(value, year):
    if year < 1995:
        if value in {8}:
            return 97
        if value in {9}:
            return 22
        return value
    if year < 2001:
        if value in {8}:
            return 22
        return value
    if value in {20,21}:
        return 22
    return value

def hazardous_material_class_number_converter(value, year):
    if year == 2007 and value == 8:
        return 88
    return value

def bus_use_converter(value, year):
    if year < 2010:
        if value in {1,2,3}:
            return 1
        if value in {9}:
            return 97
        return value
    return value

def special_use_converter(value, year):
    if value in {13}:
        return 11
    return value

def underride_override_converter(value, year):
    if year < 1994:
        if value in {15}:
            return 1
        if value in {16}:
            return 2
        return 0
    if year < 2021:
        if value in {1,2,3,4,5,6}:
            return 1
        if value in {7,8}:
            return 2
        return value
    return value

def rollover_converter(value, year):
    if value in {1,2,9}:
        return 3
    return value

def vehicle_towed_converter(value, year):
    if year < 1976:
        if value in {2}:
            return 6
        if value in {4}:
            return 5
        return value
    if year < 2009:
        if value in {1,3}:
            return 5
        if value in {2}:
            return 6
        return value
    if year < 2013:
        if value in {1,4}:
            return 5
        if value in {2,3}:
            return 6
        return value
    if year < 2022:
        if value in {2,3,7}:
            return 6
        return value
    return value

def fire_occurence_converter(value, year):
    if value == 2:
        return 1
    return value

def driver_present_converter(value, year):
    if year < 2009:
        if value in {2,3,4}:
            return 0
        return value
    return value

def non_cdl_license_status_converter(value, year):
    if year < 1982:
        if value in {0,1,2}:
            return 0
        if value in {3,7}:
            return 6
        if value in {4,5,6}:
            return value - 3
        return value
    
        
    if year < 1987:
        if value in {0,1}:
            return 0
        if value in {2,7,8}:
            return 6
        if value in {3,4,5,6}:
            return value - 2
        return value
        
    if year < 1993:
        if value in {5,6,7,8}:
            return 6
        return value
    if year < 2004:
        if value in {7,8}:
            return 6
        return value
    return value

def cdl_license_status_converter(value, year):
    if year < 1993:
        if value in {0,1,2}:
            return 0
        if value in {3,4,5}:
            return 6
        if value in {6,7,9}:
            return 99
    if value in {9}:
        return 99
    return value

def license_compliance_with_class_of_vehicle_converter(value, year):
    if year < 1987:
        if value in {0}:
            return 1
        if value in {1}:
            return 2
        if value in {2,4}:
            return 3
        if value in {3,5}:
            return 2
        return value
    return value

def year_of_violation_converter(value, year):
    if year < 1998:
        if value in {99}:
            return 9999
        return int("19"+str(value))
    return value

def speeding_related_converter(value, source, year):
    #this one is tricky- need to look in driver related factors field and violations field for different codes which all indicate speeding related
    # see page c-38 of FARS analytics manual 2022

    if year < 2009 and source == "drf":
        if value in {46}:
            return 2
        if value in {44}:
            return 3
        if value in {43}:
            return 4
        return None
    if year < 2002 and source == "violation":
        if value in {2,3}:
            return 5
        return None
    if year < 2009 and source == "violation":
        if value in {21}:
            return 2
        if value in {22,24}:
            return 3
        if value in {23,25}:
            return 4
        if value in {29}:
            return 5
        return None
    
    if year >= 2009 and source == "speeding":
        return value
    
def trafficway_description_converter(value, year):
    if year < 1982:
        if value in {1}:
            return 2
        if value in {2,3}:
            return 3
        if value in {4}:
            return 1
        if value in {5}:
            return 4
        return value
    return value

def roadway_alignment_converter(value, year):
    if year < 2010:
        if value in {2}:
            return 4
        return value
    return value

def roadway_surface_type_converter(value, year):
    if year < 2010:
        if value in {8}:
            return 7
        return value
    return value

def roadway_surface_condition_converter(value, year):
    if year < 2010:
        if value in {9}:
            return 99
        return value
    return value

def traffic_control_device_converter(value, year):
    if year < 1982:
        if value in {1}:
            return 4
        if value in {2}:
            return 3
        if value in {3}:
            return 20
        if value in {4}:
            return 21
        if value in {5,6,7}:
            return 65
        if value in {8}:
            return 23
        if value in {10}:
            return 2
        return value
    if year < 2010:
        if value in {5,6}:
            return 4
        if value in {30,31,38,39}:
            return 23
        if value in {41}:
            return 40
        if value in {60,61,62,63,64,68,69,70,71,72,73,78,79,80}:
            return 65
        return value
    if year < 2011:
        if value in {32}:
            return 23
    return value

def traffic_control_device_functioning_converter(value, year):
    if year < 1982:
        if value in {0}:
            return 0
        if value in {9}:
            return 1
        return 3
    return value

def attempted_avoidance_maneuver_converter(value, year):
    if year < 2016:
        if value in {2,3,4}:
            return 15
        return value
    return value

def age_converter(value, year):
    if year < 2009:
        if value == 99:
            return 999
    return value

def person_type_converter(value, year):
    if year < 1982:
        if value in {5}:
            return 4
        if value in {4}:
            return 6
        if value in {3}:
            return 5
        if value in {8}:
            return 19
        return value
    if year < 1994:
        if value in {8}:
            return 19
        return value
    if year < 2007:
        if value in {8,99}:
            return 19
        return value
    if year < 2022:
        if value in {11,12,13}:
            return 8
        return value
    return value

def injury_severity_converter(value, year):
    if value in {8}:
        return 9
    return value

def seating_position_converter(value, year):
    if year < 1982:
        if value in {1,2,3}:
            return value + 10
        if value in {4,5,6}:
            return value + 17
        if value in {7,8,9}:
            return value + 24
        if value in {10}:
            return 18
        if value in {11}:
            return 28
        if value in {12}:
            return 38
        if value in {13}:
            return 51
        if value in {14}:
            return 50
        if value in {15}:
            return 55
        return value
    return value

def restraint_system_use_converter(value, year):
    if year < 1994:
        if value in {5}:
            return 20
        if value in {9}:
            return 99
        return value
    if year < 2019:
        if value in {5,6,7,15,16,17,19}:
            return 20
        if value in {13,14}:
            return 4
        if value in {29}:
            return 99
        return value
    return value

def helmet_use_converter(value, year):
    if year < 1994:
        if value in {5}:
            return 5
        return 20
    if year < 2010:
        if value in {5}:
            return 5
        if value in {6}:
            return 16
        if value in {15}:
            return 19
        return 20
    if year < 2019:
        if value in {5}:
            return 5
        if value in {16,19}:
            return 19
        if value in {17}:
            return 17
        if value in {29}:
            return 99
        return 20
    return value

def helmet_misuse_converter(restraint_system, restraint_system_misuse, helmet_misuse, year):
    if year < 2019:
        if restraint_system in {5,15,16,19} and restraint_system_misuse in {1}:
            return 1

        if restraint_system in {5} and restraint_system_misuse in {0}:
            return 0
        return 7
    return helmet_misuse
        
    
def airbag_deployed_converter(value, year):
    if year < 1998:
        if value in {3}:
            return 9
        if value in {4}:
            return 20
        if value in {9}:
            return 99
    if year < 2009:
        if value in {29}:
            return 99
        if value in {30,31,32}:
            return 20
        return value
    return value

def alcohol_test_given_converter(value, year):
    if value in {1}:
        return 0
    return value

def alcohol_test_type_converter(value, year):
    if year < 2010:
        if value in {9}:
            return 99
        return value
    return value

def alcohol_test_result_converter(value, year):
    if year < 2015:
        if value in {95,96,97,98,99}:
            return 900 + value
        return value * 10
    return value

def drug_tested_converter(value, year):
    if value in {1}:
        return 0
    return value

def transported_to_medical_facility_by_converter(value, year):
    if year < 2001:
        if value in {1}:
            return 4
        if value in {7,8}:
            return 0
        return value
    if year < 2007:
        if value in {1}:
            return 4
        return value
    return value

def died_en_route_converter(value, year):
    if year < 2001:
        if value in {1}:
            return 0
        return value
    return value

def month_of_death_converter(value, year):
    if year < 2008:
        if value in {0}:
            return 88
    return value

def day_of_death_converter(value, year):
    if year < 2008:
        if value in {0}:
            return 88
    return value

def year_of_death_converter(value, year):
    if year < 1998:
        if value in {99}:
            return 9999
        return 1900 + value
    if year < 2008:
        if value in {0}:
            return 8888
    return value

def lag_hours_converter(value, year):
    if year < 2009:
        if value in {99}:
            return 999
        return value
    return value

def vehicle_which_struck_non_motorist_converter(value, year, accident_id):
    if value in {0}:
        return None
    if year < 2009:
        if value in {99}:
            return None
        vehicle = Vehicle.objects.get(accident_id=accident_id, vehicle_number=value)
        return vehicle
    if value in {999}:
        return None
    vehicle = Vehicle.objects.get(accident_id=accident_id, vehicle_number=value)
    return vehicle

def nonmotorist_location_converter(value, year):
    if year < 1982:
        if value in {7}:
            return 16
        if value in {8}:
            return 20
        if value in {9}:
            return 25
        if value in {10}:
            return 13
        if value in {11}:
            return 14
        if value in {12}:
            return 13
        if value in {99}:
            return 99
        return value
    if year < 2010:
        if value in {4}:
            return 2
        if value in {5}:
            return 25
        if value in {12}:
            return 11
        if value in {17,18}:
            return 25
        if value in {19}:
            return 99
        return value

    return value

def hispanic_converter(value, year):
    if year < 2000:
        if value in {5}:
            return 6
        return value
    return value

def crash_related_factor_converter(value, year):
    if value in {99}:
        return 999
    if year < 1982:
        if value in {41}:
            return 1
        if value in {43,44}:
            return 2
        if value in {47}:
            return 3
        if value in {48}:
            return 4
        if value in {49}:
            return 5
        if value in {50}:
            return 6
        if value in {51}:
            return 7
        return None
    return value
        
        
def vehicle_related_factor_converter(value, year):
    if year < 2020:
        if value > 28:
            return value
        return 0
    return value

def parked_vehicle_related_factor_converter(value, year):
    if year < 2010:
        if value > 28:
            return value
        return 0
    return value

def driver_related_factor_converter(value, year):
    if value in {43}:
        return 44
    if year < 1995:
        if value in {8,10}:
            return 11
        return value
    if year < 2002:
        if value in {73}:
            return 72
        if value in {74}:
            return 0
        return value
    if year < 2010:
        if value in {9}:
            return 11
        if value in {89}:
            return 101
        if value in {93,94,95,96,97,98}:
            return 93
        return value
    return value

def driver_impaired_converter(value, year):
    if year < 1982:
        if value in {1}:
            return 2
        if value in {2}:
            return 1
        if value in {3}:
            return 8
        if value in {4,5}:
            return 9
        if value in {7}:
            return 10
        return None
    if year < 2010:
        if value in {1}:
            return 2
        if value in {2}:
            return 1
        if value in {3}:
            return 8
        if value in {4,5}:
            return 9
        if value in {7,8}:
            return 4
        if value in {9}:
            return 5
        if value in {10}:
            return 6
        if value in {11}:
            return 96
        return None
    return value

def vehicle_factor_converter(value, year):
    if year < 2010:
        if value in {10}:
            return 18
        if value in {12}:
            return 10
        if value in {13}:
            return 19
        if value in {16}:
            return 11
        if value in {17,18,19}:
            return 16
        if value < 20:
            return value
        return None
    return value

        
def nonmotorist_impaired_converter(value, year):
    if year < 1995:
        if value in {15}:
            return 6
    if year < 2010:
        if value in {6}:
            return 1
        if value in {7}:
            return 8
        if value in {11}:
            return 3
        if value in {12,13}:
            return 4
        if value in {14}:
            return 5
        if value in {15}:
            return 9
        return None
    return value
        

def drug_test_type_converter(value, year):
    if year < 2018:
        if value in {3}:
            return 1
        if value in {6,7,8,9}:
            return 90 + value
        return value
    return value

def visibility_converter(value, year):
    if year < 1982:
        if value in {1,2,3,4,5,6,7}:
            return value
        if value in {8}:
            return 98
        return None
    if year < 2009:
        if value in {60}:
            return 1
        if value in {61}:
            return 2
        if value in {62}:
            return 3
        if value in {63}:
            return 4
        if value in {64}:
            return 5
        if value in {65}:
            return 6
        if value in {66}:
            return 7
        if value in {67}:
            return 8
        if value in {68}:
            return 10
        if value in {69}:
            return 11
        if value in {70,71}:
            return 12
        if value in {72}:
            return 98
        return None
    return value
        

def person_related_factor_converter(value, year):
    if year < 1982:
        if value in {1}:
            return 17
        if value in {2,3,4,5,6}:
            return value - 1
        return value

    # throw away some stuff which was tested for a couple years
    if year in {2000,2001} and value in {20}:
        return None
    if year in {2008,2009} and value in {15}:
        return None
    
    if year < 2010:
        if value in {10}:
            return None
        return value
    return value

def violation_converter(value, year):
    if year < 1982:
        if value in {0}:
            return 0
        if value in {9}:
            return 99
        if value in {1,2}:
            return 98
        return value
    if year < 1997:
        if value in {4}:
            return 2
        if value in {6,8}:
            return 98
        if value in {9}:
            return 99
        if value in {7}:
            return 79
        if value in {5}:
            return 71
        if value in {2}:
            return 22
        if value in {1,3}:
            return 19
        return value
    return value

        
def maneuver_converter(value, year):
    if year < 1982:
        if value in {23,24,25,26}:
            return value - 22
        if value in {27}:
            return 92
        if value in {28}:
            return 5
        if value in {29}:
            return 2
        return None
    if year < 2010:
        if value in {81,82,83,84}:
            return value - 80
        if value in {85}:
            return 92
        if value in {86}:
            return 5
        if value in {87}:
            return 2
        return None
    return value



FARS_DATA_CONVERTERS = {
    'accident.st_case': lambda value, year: value,
    'accident.number_of_persons_not_in_motor_vehicles': lambda value, year: value,
    'accident.number_of_persons_not_in_motor_vehicles_in_transport': lambda value, year: value,
    'accident.number_of_vehicles': lambda value, year: value,
    'accident.number_of_vehicles_in_transport': lambda value, year: value,
    'accident.number_of_parked_vehicles': lambda value, year: value,
    'accident.number_of_persons_in_motor_vehicles': lambda value, year: value,
    'accident.number_of_persons_in_motor_vehicles_in_transport': lambda value, year: value,
    'accident.month': lambda value, year: value,
    'accident.day': lambda value, year: value,
    'accident.day_of_the_week': lambda value, year: value,
    'accident.year': year_converter,
    'accident.hour': lambda value, year: value,
    'accident.minute': lambda value, year: value,
    'accident.trafficway_identifier_1': lambda value, year: value,
    'accident.trafficway_identifier_2': lambda value, year: value,
    'accident.route_signing': route_signing_converter,
    'accident.rural_urban': land_use_converter,
    'accident.functional_system': functional_system_converter,
    'accident.road_owner': lambda value, year: value,
    'accident.national_highway_system': lambda value, year: value,
    'accident.special_jurisdiction': lambda value, year: value,
    'accident.milepoint': lambda value, year: value,
    'accident.latitude': latitude_converter,
    'accident.longitude': longitude_converter,
    'accident.first_harmful_event': soe_converter,
    'accident.manner_of_collision_of_first_harmful_event': manner_of_collision_converter,
    'accident.within_interchange_area': within_interchange_area_converter,
    'accident.relation_to_junction': relation_to_junction_converter,
    'accident.type_of_intersection': type_of_intersection_converter,
    'accident.relation_to_road': relation_to_road_converter,
    'accident.work_zone': work_zone_converter,
    'accident.light_condition': light_condition_converter,
    'accident.atmospheric_condition': atmospheric_condition_converter,
    'accident.school_bus_related': school_bus_related_converter,
    'accident.rail_grade_crossing_identifier': lambda value, year: value,
    'accident.ems_notified_hour': lambda value, year: value,
    'accident.ems_notified_minute': lambda value, year: value,
    'accident.ems_arrived_hour': lambda value, year: value,
    'accident.ems_arrived_minute': lambda value, year: value,
    'accident.arrived_at_hospital_hour': lambda value, year: value,
    'accident.arrived_at_hospital_minute': lambda value, year: value,
    'accident.fatalities': lambda value, year: value,
    'vehicle.vehicle_number': lambda value, year: value,
    'vehicle.number_of_occupants': lambda value, year: value,
    'vehicle.hit_and_run': hit_and_run_converter,
    'vehicle.registration_state': registration_state_converter,
    'vehicle.registered_vehicle_owner': lambda value, year: value,
    'vehicle.vehicle_identification_number': lambda value, year: value,
    'vehicle.vehicle_model_year': model_year_converter,
    'vehicle.vpic_make': lambda value, year: value,
    'vehicle.vpic_model': lambda value, year: value,
    'vehicle.vpic_body_class': lambda value, year: value,
    'vehicle.ncsa_make': lambda value, year: value,
    'vehicle.ncsa_model': ncsa_model_converter,
    'vehicle.body_type': ncsa_body_type_converter,
    'vehicle.final_stage_body_class': lambda value, year: value,
    'vehicle.gross_vehicle_weight_rating_lower': lambda value, year: value,
    'vehicle.gross_vehicle_weight_rating_upper': lambda value, year: value,
    'vehicle.vehicle_trailing': vehicle_trailing_converter,
    'vehicle.trailer_vin_1': lambda value, year: value,
    'vehicle.trailer_vin_2': lambda value, year: value,
    'vehicle.trailer_vin_3': lambda value, year: value,
    'vehicle.trailer_weight_rating_1': lambda value, year: value,
    'vehicle.trailer_weight_rating_2': lambda value, year: value,
    'vehicle.trailer_weight_rating_3': lambda value, year: value,
    'vehicle.jackknife': lambda value, year: value,
    'vehicle.motor_carrier_identification_number': lambda value, year: value,
    'vehicle.vehicle_configuration': vehicle_configuration_converter,
    'vehicle.cargo_body_type': cargo_body_type_converter,
    'vehicle.hazardous_material_involvement': lambda value, year: value,
    'vehicle.hazardous_material_placard': lambda value, year: value,
    'vehicle.hazardous_material_id': lambda value, year: value,
    'vehicle.hazardous_material_class_number': hazardous_material_class_number_converter,
    'vehicle.release_of_hazardous_material': lambda value, year: value,
    'vehicle.bus_use': bus_use_converter,
    'vehicle.special_vehicle_use': special_use_converter,
    'vehicle.emergency_vehicle_use': lambda value, year: value,
    'vehicle.travel_speed': lambda value, year: value,
    'vehicle.underride_override': underride_override_converter,
    'vehicle.rollover': rollover_converter,
    'vehicle.rollover_location': lambda value, year: value,
    'vehicle.initial_contact_point': lambda value, year: value,
    'vehicle.extent_of_damage': lambda value, year: value,
    'vehicle.vehicle_towed': vehicle_towed_converter,
    'vehicle.most_harmful_event': soe_converter,
    'vehicle.fire_occurence': fire_occurence_converter,
    'vehicle.automated_driving_system_present': lambda value, year: value,
    'vehicle.automated_driving_system_level': lambda value, year: value,
    'vehicle.automated_driving_system_engaged': lambda value, year: value,
    'vehicle.combined_make_model_id': lambda value, year: value,
    'vehicle.fatalities': lambda value, year: value,
    'vehicle.driver_drinking': lambda value, year: value,
    'vehicle.driver_present': driver_present_converter,
    'vehicle.drivers_license_state': lambda value, year: value,
    'vehicle.driver_zip_code': lambda value, year: value,
    'vehicle.non_cdl_license_type': lambda value, year: value,
    'vehicle.non_cdl_license_status': non_cdl_license_status_converter,
    'vehicle.cdl_license_status': cdl_license_status_converter,
    'vehicle.cdl_endorsements': lambda value, year: value,
    'vehicle.license_compliance_with_class_of_vehicle': license_compliance_with_class_of_vehicle_converter,
    'vehicle.compliance_with_license_restrictions': lambda value, year: value,
    'vehicle.driver_height': lambda value, year: value,
    'vehicle.driver_weight': lambda value, year: value,
    'vehicle.previous_recorded_crashes': lambda value, year: value,
    'vehicle.previous_bac_suspensions_underage': lambda value, year: value,
    'vehicle.previous_bac_suspensions': lambda value, year: value,
    'vehicle.previous_other_suspensions': lambda value, year: value,
    'vehicle.previous_dwi_convictions': lambda value, year: value,
    'vehicle.previous_speeding_convictions': lambda value, year: value,
    'vehicle.previous_other_moving_violations': lambda value, year: value,
    'vehicle.month_of_oldest_violation': lambda value, year: value,
    'vehicle.year_of_oldest_violation': year_of_violation_converter,
    'vehicle.month_of_newest_violation': lambda value, year: value,
    'vehicle.year_of_newest_violation': year_of_violation_converter,
    'vehicle.speeding_related': speeding_related_converter,
    'vehicle.trafficway_description': trafficway_description_converter,
    'vehicle.total_lanes_in_roadway': lambda value, year: value,
    'vehicle.speed_limit': lambda value, year: value,
    'vehicle.roadway_alignment': roadway_alignment_converter,
    'vehicle.roadway_grade': lambda value, year: value,
    'vehicle.roadway_surface_type': roadway_surface_type_converter,
    'vehicle.roadway_surface_condition': roadway_surface_condition_converter,
    'vehicle.traffic_control_device': traffic_control_device_converter,
    'vehicle.traffic_control_device_functioning': traffic_control_device_functioning_converter,
    'vehicle.pre_event_movement': lambda value, year: value,
    'vehicle.critical_precrash_event': lambda value, year: value,
    'vehicle.attempted_avoidance_maneuver': attempted_avoidance_maneuver_converter,
    'vehicle.precrash_stability': lambda value, year: value,
    'vehicle.preimpact_location': lambda value, year: value,
    'vehicle.crash_type': lambda value, year: value,
    'person.person_number': lambda value, year: value,
    'person.age': age_converter,
    'person.sex': lambda value, year: value,
    'person.person_type': person_type_converter,
    'person.injury_severity': injury_severity_converter,
    'person.seating_position': seating_position_converter,
    'person.restraint_system_use': restraint_system_use_converter,
    'person.restraint_system_misuse': lambda value, year: value,
    'person.helmet_use': helmet_use_converter,
    'person.helmet_misuse': helmet_misuse_converter,
    'person.airbag_deployed': airbag_deployed_converter,
    'person.ejection': lambda value, year: value,
    'person.ejection_path': lambda value, year: value,
    'person.extrication': lambda value, year: value,
    'person.police_reported_alcohol_involvement': lambda value, year: value,
    'person.alcohol_test_given': alcohol_test_given_converter,
    'person.alcohol_test_type': alcohol_test_type_converter,
    'person.alcohol_test_result': alcohol_test_result_converter,
    'person.police_reported_drug_involvement': lambda value, year: value,
    'person.drug_tested': drug_tested_converter,
    'person.transported_to_medical_facility_by': transported_to_medical_facility_by_converter,
    'person.died_en_route': died_en_route_converter,
    'person.month_of_death': month_of_death_converter,
    'person.day_of_death': day_of_death_converter,
    'person.year_of_death': year_of_death_converter,
    'person.hour_of_death': lambda value, year: value,
    'person.minute_of_death': lambda value, year: value,
    'person.lag_hours': lag_hours_converter,
    'person.lag_minutes': lambda value, year: value,
    'person.vehicle_which_struck_non_motorist': vehicle_which_struck_non_motorist_converter,
    'person.non_motorist_device_type': lambda value, year: value,
    'person.non_motorist_device_motorization': lambda value, year: value,
    'person.non_motorist_location': nonmotorist_location_converter,
    'person.at_work': lambda value, year: value,
    'person.hispanic': hispanic_converter,
    'parked_vehicle.vehicle_number': lambda value, year: value,
    'parked_vehicle.first_harmful_event': soe_converter,
    'parked_vehicle.manner_of_collision_of_first_harmful_event': manner_of_collision_converter,
    'parked_vehicle.number_of_occupants': lambda value, year: value,
    'parked_vehicle.unit_type': lambda value, year: value,
    'parked_vehicle.hit_and_run': hit_and_run_converter,
    'parked_vehicle.registration_state': registration_state_converter,
    'parked_vehicle.registered_vehicle_owner': lambda value, year: value,
    'parked_vehicle.vehicle_identification_number': lambda value, year: value,
    'parked_vehicle.vehicle_model_year': model_year_converter,
    'parked_vehicle.vpic_make': lambda value, year: value,
    'parked_vehicle.vpic_model': lambda value, year: value,
    'parked_vehicle.vpic_body_class': lambda value, year: value,
    'parked_vehicle.ncsa_make': lambda value, year: value,
    'parked_vehicle.ncsa_model': ncsa_model_converter,
    'parked_vehicle.body_type': ncsa_body_type_converter,
    'parked_vehicle.final_stage_body_class': lambda value, year: value,
    'parked_vehicle.gross_vehicle_weight_rating_lower': lambda value, year: value,
    'parked_vehicle.gross_vehicle_weight_rating_upper': lambda value, year: value,
    'parked_vehicle.vehicle_trailing': vehicle_trailing_converter,
    'parked_vehicle.trailer_vin_1': lambda value, year: value,
    'parked_vehicle.trailer_vin_2': lambda value, year: value,
    'parked_vehicle.trailer_vin_3': lambda value, year: value,
    'parked_vehicle.trailer_weight_rating_1': lambda value, year: value,
    'parked_vehicle.trailer_weight_rating_2': lambda value, year: value,
    'parked_vehicle.trailer_weight_rating_3': lambda value, year: value,
    'parked_vehicle.motor_carrier_identification_number': lambda value, year: value,
    'parked_vehicle.vehicle_configuration': vehicle_configuration_converter,
    'parked_vehicle.cargo_body_type': cargo_body_type_converter,
    'parked_vehicle.hazardous_material_involvement': lambda value, year: value,
    'parked_vehicle.hazardous_material_placard': lambda value, year: value,
    'parked_vehicle.hazardous_material_id': lambda value, year: value,
    'parked_vehicle.hazardous_material_class_number': hazardous_material_class_number_converter,
    'parked_vehicle.release_of_hazardous_material': lambda value, year: value,
    'parked_vehicle.bus_use': bus_use_converter,
    'parked_vehicle.special_vehicle_use': special_use_converter,
    'parked_vehicle.emergency_vehicle_use': lambda value, year: value,
    'parked_vehicle.underride_override': underride_override_converter,
    'parked_vehicle.initial_contact_point': lambda value, year: value,
    'parked_vehicle.extent_of_damage': lambda value, year: value,
    'parked_vehicle.vehicle_towed': vehicle_towed_converter,
    'parked_vehicle.most_harmful_event': soe_converter,
    'parked_vehicle.fire_occurence': fire_occurence_converter,
    'parked_vehicle.fatalities': lambda value, year: value,
    'parked_vehicle.combined_make_model_id': lambda value, year: value,
    'pedestrian_type.age': age_converter,
    'pedestrian_type.sex': lambda value, year: value,
    'pedestrian_type.person_type': person_type_converter,
    'pedestrian_type.marked_crosswalk_present': lambda value, year: value,
    'pedestrian_type.sidewalk_present': lambda value, year: value,
    'pedestrian_type.in_school_zone': lambda value, year: value,
    'pedestrian_type.pedestrian_crash_type': lambda value, year: value,
    'pedestrian_type.bicycle_crash_type': lambda value, year: value,
    'pedestrian_type.pedestrian_location': lambda value, year: value,
    'pedestrian_type.bicycle_location': lambda value, year: value,
    'pedestrian_type.pedestrian_position': lambda value, year: value,
    'pedestrian_type.bicycle_position': lambda value, year: value,
    'pedestrian_type.pedestrian_direction': lambda value, year: value,
    'pedestrian_type.bicycle_direction': lambda value, year: value,
    'pedestrian_type.motorist_direction': lambda value, year: value,
    'pedestrian_type.motorist_maneuver': lambda value, year: value,
    'pedestrian_type.intersection_leg': lambda value, year: value,
    'pedestrian_type.pedestrian_scenario': lambda value, year: value,
    'pedestrian_type.pedestrian_crash_group': lambda value, year: value,
    'pedestrian_type.bike_crash_group': lambda value, year: value,
    'crash_event.crash_event_number': lambda value, year: value,
    # 'crash_event.vehicle_1': None,
    'crash_event.area_of_impact_1': lambda value, year: value,
    'crash_event.sequence_of_events': soe_converter,
    # 'crash_event.vehicle_2': None,
    'crash_event.area_of_impact_2': lambda value, year: value,
    'crash_related_factors.crash_related_factor': crash_related_factor_converter,
    'weather.weather': atmospheric_condition_converter,
    'vehicle_related_factor.vehicle_related_factor': vehicle_related_factor_converter,
    'parked_vehicle_related_factor.vehicle_related_factor': parked_vehicle_related_factor_converter,
    'driver_related_factor.driver_related_factor': driver_related_factor_converter,
    'damage.area_of_impact': lambda value, year: value,
    'driver_distracted.distracted_by': lambda value, year: value,
    'driver_impaired.driver_impaired': driver_impaired_converter,
    'vehicle_factor.contributing_cause': vehicle_factor_converter,
    'maneuver.driver_maneuvered_to_avoid': maneuver_converter,
    'violation.moving_violation': violation_converter,
    'vision.visibility': visibility_converter,
    'person_related_factor.person_related_factor': person_related_factor_converter,
    'drugs.drug_test_type': drug_test_type_converter,
    'drugs.drug_test_results': lambda value, year: value,
    'race.race': lambda value, year: value,
    'nonmotorist_contributing_circumstance.nonmotorist_contributing_circumstance': lambda value, year: value,
    'nonmotorist_distracted.nonmotorist_distracted_by': lambda value, year: value,
    'nonmotorist_impaired.nonmotorist_impaired': nonmotorist_impaired_converter,
    'nonmotorist_prior_action.nonmotorist_prior_action': lambda value, year: value,
    'safety_equipment.helmet': lambda value, year: value,
    'safety_equipment.pads': lambda value, year: value,
    'safety_equipment.other_protective_equipment': lambda value, year: value,
    'safety_equipment.reflective_equipment': lambda value, year: value,
    'safety_equipment.lights': lambda value, year: value,
    'safety_equipment.other_preventative_equipment': lambda value, year: value,
}
