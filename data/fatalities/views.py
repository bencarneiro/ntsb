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
    ],

    # VEHICLES

    # V4
    "vehicle.number_of_occupants": [
        {
            "range": {
                "start": 1975,
                "end": 2008
            },
            "key": "vehicle.OCUPANTS"
        },
        {
            "range": {
                "start": 2009,
                "end": None
            },
            "key": "vehicle.NUMOCCS"
        }
    ],

    #V6
    "vehicle.hit_and_run": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.HIT_RUN"
        }
    ],

    #V7 
    "vehicle.registration_state": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.REG_STAT"
        }
    ],

    #V8
    "vehicle.registered_vehicle_owner": [
        {
            "range": {
                "start": 1991,
                "end": None
            },
            "key": "vehicle.OWNER"
        }
    ],

    # V9
    "vehicle.vehicle_identification_number": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.VIN"
        }
    ],

    # V10
    "vehicle.model_year": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.MOD_YEAR"
        }
    ],

    # V11
    "vehicle.vpic_make": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.VPICMAKE"
        }
    ],

    # V12
    "vehicle.vpic_model": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.VPICMODEL"
        }
    ],

    # V13
    "vehicle.vpic_body_class": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.VPICBODYCLASS"
        }
    ],

    # V14
    "vehicle.ncsa_make": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.MAKE"
        }
    ],


    # V15
    "vehicle.ncsa_model": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.MODEL"
        }
    ],


    # V16
    "vehicle.body_type": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.BODY_TYP"
        }
    ],
    # V17
    "vehicle.final_stage_body_class": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.ICFINALBODY"
        }
    ],
    # V18
    "vehicle.gross_vehicle_weight_rating_lower": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.GVWR_FROM"
        }
    ],
    # V18
    "vehicle.gross_vehicle_weight_rating_upper": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.GVWR_TO"
        }
    ],
    
    # V19
    "vehicle.vehicle_trailing": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.TOW_VEH"
        }
    ],
    #v20
    "vehicle.trailer_vin_1": [
        {
            "range": {
                "start": 2016,
                "end": None
            },
            "key": "vehicle.TRLR1VIN"
        }
    ],
    "vehicle.trailer_vin_2": [
        {
            "range": {
                "start": 2016,
                "end": None
            },
            "key": "vehicle.TRLR2VIN"
        }
    ],
    "vehicle.trailer_vin_3": [
        {
            "range": {
                "start": 2016,
                "end": None
            },
            "key": "vehicle.TRLR3VIN"
        }
    ],
    #V21
    "vehicle.trailer_weight_rating_1": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.TRLR1GVWR"
        }
    ],
    "vehicle.trailer_weight_rating_2": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.TRLR2GVWR"
        }
    ],
    "vehicle.trailer_weight_rating_3": [
        {
            "range": {
                "start": 2020,
                "end": None
            },
            "key": "vehicle.TRLR3GVWR"
        }
    ],
    #V22
    
    "vehicle.jackknife": [
        {
            "range": {
                "start": 1980,
                "end": None
            },
            "key": "vehicle.J_KNIFE"
        }
    ],

    #V23
    "vehicle.motor_carrier_issuing_authority": [
        {
            "range": {
                "start": 2007,
                "end": None
            },
            "key": "vehicle.MCARR_I1"
        }
    ],
    "vehicle.motor_carrier_identification_number": [
        {
            "range": {
                "start": 2007,
                "end": None
            },
            "key": "vehicle.MCARR_I2"
        }
    ],
    #V24
    
    "vehicle.vehicle_configuration": [
        {
            "range": {
                "start": 1991,
                "end": None
            },
            "key": "vehicle.V_CONFIG"
        }
    ],
    #v25
    "vehicle.cargo_body_type": [
        {
            "range": {
                "start": 1991,
                "end": None
            },
            "key": "vehicle.CARGO_BT"
        }
    ],
    #V26
    "vehicle.hazardous_material_involvement": [
        {
            "range": {
                "start": 2007,
                "end": None
            },
            "key": "vehicle.HAZ_INV"
        }
    ],
    "vehicle.hazardous_material_placard": [
        {
            "range": {
                "start": 2007,
                "end": None
            },
            "key": "vehicle.HAZ_PLAC"
        }
    ],
    "vehicle.hazardous_material_id": [
        {
            "range": {
                "start": 2007,
                "end": None
            },
            "key": "vehicle.HAZ_ID"
        }
    ],
    "vehicle.hazardous_material_class_number": [
        {
            "range": {
                "start": 2007,
                "end": None
            },
            "key": "vehicle.HAZ_CNO"
        }
    ],
    #V27

    "vehicle.bus_use": [
        {
            "range": {
                "start": 2000,
                "end": None
            },
            "key": "vehicle.BUS_USE"
        }
    ],
    #v28

    "vehicle.special_vehicle_use": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.SPEC_USE"
        }
    ],
    #v29

    "vehicle.emergency_vehicle_use": [
        {
            "range": {
                "start": 1977,
                "end": None
            },
            "key": "vehicle.EMER_USE"
        }
    ],
    #v30
    "vehicle.travel_speed": [
        {
            "range": {
                "start": 1975,
                "end": None
            },
            "key": "vehicle.TRAV_SP"
        }
    ],
    #v31
    "vehicle.under_override": [
        {
            "range": {
                "start": 2021,
                "end": None
            },
            "key": "vehicle.UNDEROVERRIDE"
        }
    ],
    #v32
    "vehicle.rollover": [
        {
            "range": {
                "start": 1978,
                "end": None
            },
            "key": "vehicle.ROLLOVER"
        }
    ],
    #v33
    "vehicle.rollover_location": [
        {
            "range": {
                "start": 2009,
                "end": None
            },
            "key": "ROLINLOC"
        }
    ]
    




}
