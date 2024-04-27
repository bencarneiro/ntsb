from django.shortcuts import render


FARS_DATA_DICTIONARY = {
    #C3
    "accident.number_of_persons_not_in_motor_vehicles": [
        {
            "range": {
                "start": 1991,
                "end": None
            },
            "key": "accident.PEDS"
        }
    ],
    #C3A
    "accident.number_of_persons_not_in_motor_vehicles_in_transport": [
        {
            "range": {
                "start": 2011,
                "end": None
            },
            "key": "accident.PERNOTMVIT"
        }
    ],
    #C4
    "accident.number_of_vehicles": [
        {
            "range": {
                "start": 2005,
                "end": None
            },
            "key": "accident.VE_TOTAL"
        }
    ],
    #C4A
    "accident.number_of_vehicles_in_transit": [

        {
            "range": {
                "start": 1976,
                "end": None
            },
            "key": "accident.VE_FORMS"
        }
    ],
    #C4B
    "accident.number_of_parked_vehicles": [

        {
            "range": {
                "start": 2011,
                "end": None
            },
            "key": "accident.PVH_INVL"
        }
    ],
    #C5
    "accident.number_of_persons_in_motor_vehicles": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.PERSONS"
        }
    ],
    #C5A
    "accident.number_of_persons_in_motor_vehicles_in_transport": [

        {
            "range": {
                "start": 2011,
                "end": None
            },
            "key": "accident.PERMVIT"
        }
    ],
    #C6
    "accident.county": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.COUNTY"
        }
    ],
    #c7
    "accident.city": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.CITY"
        }
    ],
    #C8A
    "accident.month": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.MONTH"
        }
    ],
    #C8B
    "accident.day": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.DAY"
        }
    ],
    #C8C
    "accident.day_of_the_week": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.DAY_WEEK"
        }
    ],
    #C8D
    "accident.year": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.YEAR"
        }
    ],
    #C9A
    "accident.hour": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.HOUR"
        }
    ],
    # C9B
    "accident.minute": [

        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.MINUTE"
        }
    ],
    # C10
    "accident.trafficway_identifier_1": [

        {
            "range": {
                "start": 1982,
                "end": None
            },
            "key": "accident.TWAY_ID"
        }
    ],
    "accident.trafficway_identifier_2": [

        {
            "range": {
                "start": 1982,
                "end": None
            },
            "key": "accident.TWAY_ID2"
        }
    ],
    #C11
    "accident.route_signing": [
        {
            "range": {
                "start": 1975,
                "end": 1980
            },
            "key": "accident.CL_TWAY"
        },
        {
            "range": {
                "start": 1982,
                "end": 1986
            },
            "key": "accident.CL_TWAY"
        },
        {
            "range": {
                "start": 1987,
                "end": None
            },
            "key": "accident.ROUTE"
        }
    ],
    #C12A
    "accident.rural_urban": [
        {
            "range": {
                "start": 1975,
                "end": 1986
            },
            "key": "accident.LAND_USE"
        },
        {
            "range": {
                "start": 1987,
                "end": 2014
            },
            "key": "accident.ROAD_FNC"
        },
        {
            "range": {
                "start": 2015,
                "end": None
            },
            "key": "accident.RUR_URB"
        }
    ],
    #C12B
    "accident.functional_system": [
        {
            "range": {
                "start": 1981,
                "end": 2014
            },
            "key": "accident.ROAD_FNC"
        },
        {
            "range": {
                "start": 2015,
                "end": None
            },
            "key": "accident.FUNC_SYS"
        }
    ],
    #C13
    "accident.road_owner": [
        {
            "range": {
                "start": 2015,
                "end": None
            },
            "key": "accident.RD_OWNER"
        }
    ],
    #C14
    "accident.national_highway_system": [
        {
            "range": {
                "start": 1994,
                "end": None
            },
            "key": "accident.NHS"
        }
    ],
    #C15
    "accident.special_jurisdiction": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.SP_JUR"
        }
    ],
    #C16
    "accident.milepoint": [
        {
            "range": {
                "start": 1982,
                "end": None
            },
            "key": "accident.MILEPT"
        }
    ],
    #C17A
    "accident.latitude": [
        {
            "range": {
                "start": 1999,
                "end": None
            },
            "key": "accident.LATITUDE"
        }
    ],
    #C17B
    "accident.longitude": [
        {
            "range": {
                "start": 1999,
                "end": None
            },
            "key": "accident.LONGITUD"
        }
    ],
    #C19
    "accident.first_harmful_event": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.HARM_EV"
        }
    ],
    #C20
    "accident.manner_of_collision_of_first_harmful_event": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.MAN_COLL"
        }
    ],
    #C21
    "accident.at_intersection": [
        {
            "range": {
                "start": 2010,
                "end": None
            },
            "key": "accident.RELJCT1"
        }
    ],
    #c21B
    "accident.relation_to_junction": [
        {
            "range": {
                "start": 1975,
                "end": 2009
            },
            "key": "accident.REL_JUNC"
        },
        {
            "range": {
                "start": 2010,
                "end": None
            },
            "key": "accident.RELJCT2"
        }
    ],
    #C22
    "accident.type_of_intersection": [
        {
            "range": {
                "start": 2010,
                "end": None
            },
            "key": "accident.TYP_INT"
        }
    ],
    #c23
    "accident.relationship_to_road": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.REL_ROAD"
        }
    ],
    #c24
    "accident.work_zone": [
        {
            "range": {
                "start": 1980,
                "end": 2008
            },
            "key": "accident.C_M_ZONE"
        },

        {
            "range": {
                "start": 2009,
                "end": None
            },
            "key": "accident.WRK_ZONE"
        }
    ],
    #c25
    "accident.light_condition": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.LGT_COND"
        }
    ],
    #C26
    "accident.atmospheric_condition": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.WEATHER"
        }
    ],
    #C27
    "accident.school_bus_involved": [
        {
            "range": {
                "start": 1977,
                "end": None
            },
            "key": "accident.SCH_BUS"
        }
    ],
    #c28
    "accident.rail_grade_crossing_identifier": [
        {
            "range": {
                "start": 1979,
                "end": None
            },
            "key": "accident.RAIL"
        }
    ],
    #c29A
    "accident.ems_notified_hour": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.NOT_HOUR"
        }
    ],
    #c29B
    "accident.ems_notified_minute": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.NOT_MIN"
        }
    ],
    #c30A
    "accident.ems_arrived_hour": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.ARR_HOUR"
        }
    ],
    #c30B
    "accident.ems_arrived_minute": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.ARR_MIN"
        }
    ],
    #C31A
    "accident.arrived_at_hospital_hour": [
        {
            "range": {
                "start": 1987,
                "end": None
            },
            "key": "accident.HOSP_HOUR"
        }
    ],
    #c31B
    "accident.arrived_at_hospital_minute": [
        {
            "range": {
                "start": 1987,
                "end": None
            },
            "key": "accident.HOSP_MIN"
        }
    ],
    #C101
    "accident.fatalities": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "accident.FATALS"
        }
    ]


}

# # Create your views here.
# 'STATE', 'COUNTY', 'MONTH', 'DAY', 'YEAR', 'HOUR', 'MINUTE', 'VE_FORMS',
#        'PERSONS', 'VEHICLES', 'LAND_USE', 'CL_TWAY', 'ROAD_FNC', 'TA_1_CL',
#        'SP_JUR', 'HARM_EV', 'MAN_COLL', 'REL_JUNC', 'REL_ROAD', 'ROAD_FLO',
#        'NO_LANES', 'SP_LIMIT', 'ALIGNMNT', 'PROFILE', 'PAVE_TYP', 'SUR_COND',
#        'TRA_CONT', 'LGT_COND', 'WEATHER', 'HIT_RUN', 'C_M_ZONE', 'NOT_HOUR',
#        'NOT_MIN', 'ARR_HOUR', 'ARR_MIN', 'SCH_BUS', 'CF1', 'CF2', 'CF3',
#        'FATALS', 'DAY_WEEK', 'DRUNK_DR', 'ST_CASE', 'CITY', 'RAIL'

# column_name_codes_1975 = {
#     "STATE": "state",
#     "COUNTY": "county",
#     "MONTH": "month",
#     "DAY": "day",
#     "YEAR": "year",
#     "HOUR": "hour",
#     "MINUTE": "minute",
#     "VE_FORMS": "number_of_motor_vehicles_in_transit",
#     "PERSONS": "persons",
#     "VEHICLES": "vehicles",
#     "LAND_USE": "land_use",
#     "CL_TWAY": "route_signing",
#     "ROAD_FNC": "roadway_function",
#     "TA_1_CL": "federal_highway",
#     "SP_JUR": "special_jurisdiction",
#     "HARM_EV": "first_harmful_event",
#     "MAN_COLL": "manner_of_collision",
#     "REL_JUNC": "relationship_to_junction",
#     "REL_ROAD": "relationship_to_road",
#     "ROAD_FLO": "trafficway_description", 
#     "NO_LANES": "total_lanes_in_roadway",
#     "SP_LIMIT": "speed_limit",
#     "ALIGNMNT": "roadway_alignment",




# }