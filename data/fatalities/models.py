from django.db import models

# Create your models here.

class State(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = "state"
        managed = True


class County(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=512, null=False)

    class Meta:
        db_table = "county"
        managed = True

class City(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=512, null=False)

    class Meta:
        db_table = "county"
        managed = True

class Accident(models.Model):
    year
    st_case = models.PositiveIntegerField(null=False)
    #c3
    num_persons_not_in_motor_vehicles
    #c3a
    num_persons_not_in_motor_vehicles_in_transport
    #c4
    num_vehicles
    #c4a
    num_vehicles_in_transit
    #c4b
    num_parked_vehicles
    #c5
    num_persons_in_motor_vehicles
    #c5a
    num_persons_in_motor_vehicles_in_transport
    # C6 County COUNTY 40
    county
    # C7 City CITY 41
    city
    # C8A Month of Crash MONTH 42
    # C8B Day of Crash DAY 42
    # C8C Day of Week DAY_WEEK 43
    # C8D Year of Crash YEAR 43
    # C9A Hour of Crash HOUR 44
    # C9B Minute of Crash MINUTE 44
    datetime
    #c11
    route_signing # needs a table for codes
    #c15
    special_jurisdiction # needs a table for codes
    #c16
    milepoint
    #c17
    latitude
    longitude
    #c19
    first_harmful_event # needs a table for codes
    #c20
    manner_of_collision_of_first_harmful_event # needs a table for codes
    #c21B
    relation_to_junction # needs a table for codes
    #c23
    relation_to_trafficway # needs a table for codes
    #c24
    work_zone # needs a table for codes
    #c25
    light_condition # needs a table for codes
    #c26
    atmospheric_condition # needs a table for codes
    #c27
    school_bus_related # needs a table for codes
    #c28
    rail_grade_crossing_identifier #seven-char string
    #c29
    ems_notification_time
    #c30
    ems_accident_arrival_time
    #c31
    ems_hospital_arrival_time
    #c101
    fatalities

    #discontinued 2008
    hit_and_run
    #discontinued 2015 DRUNK_DR
    num_drunk_drivers # needs a table for codes
    # discontinued ALIGNMNT
    roadway_alignment
    #discontinued ROAD_FNC
    roadway_function
    # discontinued PROFILE
    roadway_profile
    # discontinued SUR_COND
    roadway_surface_condition
    # discontinued PAVE_TYP
    pavement_type
    # discontinued SP_LIMIT
    speed_limit
    # discontinued NO_LANES
    num_lanes_in_roadway
    # discontinued TRA_CONT
    traffic_control_device # This one needs a huge table
    # discontinued T_CONT_F
    traffic_control_device_functioning

    

class Vehicle(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    accident = models.ForeignKey(Accident, on_delete=models.DO_NOTHING)
    vehicle_number = models.PositiveSmallIntegerField(null=False)
    #v4
    num_occupants
    # v6
    hit_and_run
    #v7 
    registration_state
    #v9
    vehicle_identification_number
    #v10 
    vehicle_model_year
    #v14
    ncsa_make # needs a table for codes
    #v15
    ncsa_model # needs a table for codes
    #v16
    body_type # needs a table for codes
    #v19 
    vehicle_trailing  # needs a table for codes
    #v22 
    jackknife  # needs a table for codes


    #v26a HAZ_INV
    hazardous_material_involvement
    #v26B HAZPLAC
    hazardous_material_placard
    # V26C - HAZ_ID
    hazardous_material_id
    # v26D HAZ_CNO
    hazardous_material_class_number
    # v26E HAZ_REL
    release_of_hazardous_material
    
    #v28
    special_vehicle_use  # needs a table for codes
    #v29
    emergency_vehicle_use  # needs a table for codes
    #v30
    travel_speed
    #v32 
    rollover  # needs a table for codes
    #V34A
    initial_contact_point   # needs a table for codes
    #v35
    extent_of_damage   # needs a table for codes
    #v36
    vehicle_towed # needs a table for codes
    #v38
    most_harmful_event # needs a table for codes
    #v39
    fire_occurence  # needs a table for codes
    #v40a
    automation_system_present  # needs a table for codes
    #v40b
    type_of_automation_system_present  # needs a table for codes
    #v40c
    type_of_automation_system_engaged  # needs a table for codes
    #v150
    fatalities
    #v151
    driver_drinking # needs a table for codes
    #d4
    driver_presence # needs a table for codes
    #d5
    driver_license_state # needs a table for codes
    #d6 DRIMPAIR
    driver_zip_code
    #d7b
    non_cdl_license_status # needs a table for codes
    #d8
    cdl_license_status # needs a table for codes
    #d10
    license_compliance_with_class_of_vehicle # needs a table for codes
    #d11
    compliance_with_license_restrictions # needs a table for codes
    #d12 (inches)
    driver_height
    #d13 (lbs)
    driver_weight
    #d14
    previous_recorded_crashes # needs a table for codes
    #d16
    previous_dwi_convictions # needs a table for codes
    #d17
    previous_speeding_convictions # needs a table for codes
    #d18
    previous_other_moving_violations # needs a table for codes
    #d19a
    month_of_oldest_violation
    #d19b
    year_of_oldest_violation
    #d20a
    month_of_newest_violation
    #d20b
    year_of_newest_violation
    #pc5
    trafficway_description # need table
    # pc6
    total_lanes_in_roadway # need table
    #pc7
    speed_limit #need table
    #pc8
    roadway_alignment #needs a table for codes
    #pc9
    roadway_grade #needs a table for codes
    #pc10
    roadway_surface_type #needs a table for codes
    #pc11
    roadway_surface_condition #needs a table for codes
    #pc12
    traffic_control_device #needs a table for codes
    #pc13
    traffic_control_device_functioning #needs a table for codes
    

class Person(models.Model):
    accident = models.ForeignKey(Accident, on_delete=models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True)
    person_number = models.PositiveSmallIntegerField(null=False)
    # id = models.PositiveBigIntegerField(primary_key = True)
    
    #p5
    age = models.PositiveSmallIntegerField(null = True)
    #p6 
    sex # need table
    #p7 PER_TYP
    person_type
    #p8 injury_severity
    injury_severity
    #p9 seating position
    seating_position
    #P10A restraint system use
    restraint_system_use
    #P10B restraint system use
    restraint_system_misuse
    # P11A Helmet Use 
    helmet_use
    #p11b
    helmet_misuse
    # p12
    airbag_deployed
    # p13
    ejection
    # p14 ejectionpath
    ejection_path
    #p15
    extrication
    #p16
    alcohol_involvement
    #p17
    method_of_alcohol_determination
    #p18a
    alcohol_test
    #p18b
    alcohol_test_type
    #P18C
    alcohol_test_result
    #p19
    drug_involvement
    #p20
    method_of_drug_determination
    #p21 
    drug_test_status
    #p22
    transported_to_medical_facility_by
    #p24a
    month_of_death
    #p24b
    day_of_death
    #p24c
    year_of_death
    #p25
    time_of_death
    #p100a
    lag_hours
    #p100b
    lag_minutes
    #NM4
    vehicle_which_struck_non_motorist = models.ForeignKey(vehicle)
    #nm10
    non_motorist_location
    #sp2
    at_work

# A class for parked cars involved with a given fatal crash
    
class ParkedVehicle(models.Model):
    accident = models.ForeignKey(Accident, on_delete=models.DO_NOTHING)
    vehicle_number = models.PositiveSmallIntegerField(null=False)
    #c4a #PVE_FORMS
    num_vehicles_in_transit
    #c19 PHARM_EV
    first_harmful_event
    # c20 PMAN_COLL
    manner_of_collision_of_first_harmful_event
    #v4 PNUMOCCS
    num_occupants
    #v5 PTYPE
    unit_type
    #v6 PHIT_RUN
    hit_and_run
    # v7 PREG_STAT
    registration_state
    # v8 POWNER
    vehicle_owner
    # v9 PVIN
    vehicle_identification_number
    # v10 PMODYEAR
    vehicle_model_year
    # v14 PMAKE
    ncsa_make
    # V15 PMODEL
    ncsa_model
    # V16 PBODYTYP
    body_type
    # V19 PTRAILER
    vehicle_trailing
    # V23 PMCARR_ID
    motor_carrier_identification_number
    #v24 PV_CONFIG
    vehicle_configuration
    #v25 PCARGTYP
    cargo_body_type
    #v26a PHAZ_INV
    hazardous_material_involvement
    #v26B PHAZPLAC
    hazardous_material_placard
    # V26C - PHAZ_ID
    hazardous_material_id
    # v26D PHAZ_CNO
    hazardous_material_class_number
    # v26E PHAZ_REL
    release_of_hazardous_material
    #V27 PBUS_USE
    bus_use
    #v28 PSP_USE
    special_vehicle_use
    #v29 PEM_USE
    emergency_vehicle_use
    # V34A PIMPACT1
    initial_contact_point
    #v35 PVEH_SEV
    extent_of_damage
    #v36 PTOWED
    vehicle_towed
    #v38 PM_HARM
    most_harmful_event
    #v39 PFIRE
    fire_occurence

class PBType(models.Model):
    accident = models.ForeignKey(Accident, null=False, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True)
    #p5 PBAGE
    age
    # p6 PBSEX
    sex
    #p7 PBPTYPE
    person_type
    # NM11-PB27 PBCWALK
    on_sidewalk
    # NM11-PB28 PBSWALK
    at_marked_crosswalk
    # NM11-PB29 PBSZONE
    in_school_zone
    # NM11-PB30 PEDCTYPE
    pedestrian_crash_type
    # NM11-PB30B BIKECTYPE
    bicycle_crash_type
    # NM11-PB31 PEDLOC
    pedestrian_location
    # NM11-PB31B BIKELOC
    bicycle_location
    # NM11-PB32 PEDPOS
    pedestrian_position
    # NM11-PB32B BIKEPOS
    bicycle_position
    # NM11-PB33 PEDDIR
    pedestrian_direction
    # NM11-PB33B BIKEDIR
    bicycle_direction
    # NM11-PB34 MOTDIR
    motorist_direction
    # NM11-PB35  MOTMAN
    motorist_maneuver
    # NM11-PB36 PEDLEG
    intersection_leg
    # NM11-PB37 PEDSNR
    pedestrian_scenario
    # NM11-PB38 PEDCGP
    pedestrian_crash_group
    # NM11-PB38B BIKECGP
    bike_crash_group

class CrashEvent(models.Model):
    accident = models.ForeignKey(Accident, null=False, on_delete=models.DO_NOTHING)
    event_num = models.PositiveSmallIntegerField(null=False)
    # VNUMBER1 c18a
    vehicle_1 = models.ForeignKey(Vehicle, null=True, blank=True)
    # C18B AOI1 
    area_of_impact_1
    # V37 SOE
    sequence_of_events
    # C18C VNUMBER2
    vehicle_2 - models.ForeignKey(Vehicle, null=True, blank=True)
    # C18D AOI2
    area_of_impact_2

class VehicleEvent(models.Model):
    accident = models.ForeignKey(Accident, null=False, on_delete=models.DO_NOTHING)
    event_num = models.PositiveSmallIntegerField(null=False)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True)
    # VNUMBER1 C18A
    vehicle_1 = models.ForeignKey(Vehicle, null=True, blank = True)
    # C18B AOI1 
    area_of_impact_1
    # V37 SOE
    sequence_of_events
    # C18C VNUMBER2
    vehicle_2 - models.ForeignKey(Vehicle, null=True, blank=True)
    # C18D AOI2
    area_of_impact_2
    
class VehicleSequenceOfEvents(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle_event = models.ForeignKey(Vehicle, null=False, blank=False, on_delete = models.DO_NOTHING)
    # C18E AOI
    area_of_impact
    # V37 SOE
    sequence_of_events

class CrashRelatedFactors(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    # CRASHRF C32
    crash_related_factor
    

class Weather(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    #c26 weather
    atmospheric_condition

    

class VehicleRelatedFactor(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    # v41 VEHICLESF
    vehicle_related_factor

class ParkedVehicleRelatedFactor(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    parked_vehicle = models.ForeignKey(ParkedVehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    # v41 VEHICLESF
    parked_vehicle_related_factor

class DriverRelatedFactor(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    # DRIVERRF D24
    driver_related_factor

class Damage(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    # MDAREAS DAMAGE  V34B
    area_of_impact

class DriverDistracted(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    # MDRDSTRD DRDISTRACT PC16
    distracted_by

class DriverImpaired:
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)

    # DRIMPAIR D23
    driver_impaired

class VehicleFactor():
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    
    # PC4 MFACTOR VEHICLECC
    contributing_cause

class Maneuver(): 
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    
    # MDRMANAV MANEUVER PC15
    driver_maneuvered_to_avoid

class Violation():
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)

    # MVIOLATN VIOLATION D21
    moving_violation

class Vision():
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)

    # MVISOBSC VISION PC14
    visibility


class PersonRelatedFactor():
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, Blank=True, on_delete = models.DO_NOTHING)

    # PERSONRF P24/NM26 
    person_related_factor

class Drugs():
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, Blank=True, on_delete = models.DO_NOTHING)

    # P19/NM21 DRUGSPEC
    drug_test_type
    # P19C/NM21C  DRUGRES
    drug_test_results

class Race():
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, Blank=True, on_delete = models.DO_NOTHING)

    # SP3A RACE
    race
    # SP3AA MULTRACE
    is_multiple_races
    # ORDER
    order

class NonMotoristCrash(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, Blank=True, on_delete = models.DO_NOTHING)

    # NM14 MTM_CRSH NMCC
    nonmotorist_contributing_circumstance

class NonmotoristDistracted(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, Blank=True, on_delete = models.DO_NOTHING)

    # NM15 MNMDSTRD NMDISTRACT
    nonmotorist_distracted

class NonmotoristImpaired(models.Model):
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, Blank=True, on_delete = models.DO_NOTHING)

    #NM17 NMIMPAIR
    nonmotorist_impaired

class NonmotoristPriorAction(models.Model):

    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, Blank=True, on_delete = models.DO_NOTHING)

    # MPR_ACT NMACTION NM13
    nonmotorist_prior_action

class SafetyEquipment(models.Model):

    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete = models.DO_NOTHING)
    person = models.ForeignKey(Person, null=True, Blank=True, on_delete = models.DO_NOTHING)

    # NM16A NMHELMET
    helmet
    # NM16B NMPROPAD
    pads
    # NM16C NMOTHPRO
    other_protective_equipment
    # NM16D NMREFCLO
    reflective_equipment
    # NM16E NMLIGHT
    lights
    # NM16F NMOTHPRE
    other_preventative_equipment






# The ACCIDENT Data File 33
# C3 Number of Forms Submitted for Persons
# Not in Motor Vehicles PEDS 34
# C3A Number of Persons Not in Motor Vehicles
# In-Transport (MVIT) PERNOTMVIT 34
    
# C4 Number of Vehicle Forms Submitted- ALL VE_TOTAL 35
# C4A Number of Motor Vehicles In-Transport (MVIT) VE_FORMS 36
    
# C4B Number of Parked/Working Vehicles PVH_INVL 37
# C5 Number of Forms Submitted for Persons
# in Motor Vehicles PERSONS 38
# C5A Number of Persons in Motor Vehicles
# In-Transport (MVIT) PERMVIT 39
    
# C6 County COUNTY 40
# C7 City CITY 41
# C8A Month of Crash MONTH 42
# C8B Day of Crash DAY 42
# C8C Day of Week DAY_WEEK 43
# C8D Year of Crash YEAR 43
# C9A Hour of Crash HOUR 44
# C9B Minute of Crash MINUTE 44
    
# C10 Trafficway Identifier TWAY_ID 45
# C10 Trafficway Identifier TWAY_ID2 45
# C11 Route Signing ROUTE 46
# C12A Land Use RUR_URB 47
# C12B Functional System FUNC_SYS 47
# 13
# C13 Ownership RD_OWNER 48
# C14 National Highway System NHS 49
# C15 Special Jurisdiction SP_JUR 50
# C16 Milepoint MILEPT 51
# C17A Latitude LATITUDE 52
# C17B Longitude LONGITUD 53
    
# C19 First Harmful Event HARM_EV 54
# C20 Manner of Collision of the First Harmful Event MAN_COLL 58
# C21A Relation to Junction- Within Interchange Area RELJCT1 60
# C21B Relation to Junction- Specific Location RELJCT2 61
# C22 Type of Intersection TYP_INT 63
# C23 Relation to Trafficway REL_ROAD 64
# C24 Work Zone WRK_ZONE 65
# C25 Light Condition LGT_COND 66
# C26 Atmospheric Conditions WEATHER 67
# C27 School Bus Related SCH_BUS 69
# C28 Rail Grade Crossing Identifier RAIL 70
# C29A Hour of Notification NOT_HOUR 71
# C29B Minute of Notification NOT_MIN 71
# C30A Hour of Arrival at Scene ARR_HOUR 72
# C30B Minute of Arrival at Scene ARR_MIN 72
# C31A Hour of EMS Arrival at Hospital HOSP_HR 73
# C31B Minute of EMS Arrival at Hospital HOSP_MN 73
# C101 Fatalities FATALS 74
# Atmospheric Conditions (discontinued) WEATHER1 75
# Atmospheric Conditions (discontinued) WEATHER2 75
# Federal Highway (discontinued) FED_AID 76
# Hit-and-Run (discontinued) HIT_RUN 77
# Land Use (discontinued) LAND_USE 78
# Number of Drinking Drivers (discontinued) DRUNK_DR 79
# Related Factors- Crash Level (discontinued) CF1 80
# Related Factors- Crash Level (discontinued) CF2 80
# Related Factors- Crash Level (discontinued) CF3 80
# Roadway Alignment (discontinued) ALIGNMNT 82
# Roadway Function Class (discontinued) ROAD_FNC 83
# Roadway Profile (discontinued) PROFILE 84
# Roadway Surface Condition (discontinued) SUR_COND 84
# Roadway Surface Type (discontinued) PAVE_TYP 85
# Speed Limit (discontinued) SP_LIMIT 85
# 14
# Total Lanes in Roadway (discontinued) NO_LANES 86
# Traffic Control Device (discontinued) TRA_CONT 87
# Traffic Control Device Functioning
# (discontinued) T_CONT_F 89
# Trafficway Description (discontinued) TRAF_FLO 89
# Vehicles In-Transport (discontinued) VEHICLES 90






# class Accident(models.Model):
    # STATE
    # COUNTY
    # MONTH
    # DAY
    # HOUR
    # MINUTE
    # VE_FORMS
    # PERSONS
    # PEDS
    # NHS
    # ROAD_FNC
    # ROUTE
    # SP_JUR
    # HARM_EV
    # MAN_COLL
    # REL_JUNC
    # REL_ROAD
    # TRAF_FLO
    # NO_LANES
    # SP_LIMIT
    # ALIGNMNT
    # PROFILE
    # PAVE_TYP
    # SUR_COND
    # TRA_CONT
    # T_CONT_F
    # HIT_RUN
    # LGT_COND
    # WEATHER
    # C_M_ZONE
    # NOT_HOUR
    # NOT_MIN
    # ARR_HOUR
    # ARR_MIN
    # HOSP_HR
    # HOSP_MN
    # SCH_BUS
    # CF1
    # CF2
    # CF3
    # FATALS
    # DAY_WEEK
    # DRUNK_DR
    # ST_CASE
    # CITY
    # MILEPT
    # YEAR
    # TWAY_ID
    # RAIL
    # latitude
    # longitud

#     class Meta:
#         db_table = "accident"
#         managed = True


# 2021 accidents table
# STATE,STATENAME,ST_CASE,PEDS,PERNOTMVIT,VE_TOTAL,VE_FORMS,PVH_INVL,PERSONS,PERMVIT,COUNTY,COUNTYNAME,CITY,CITYNAME,MONTH,MONTHNAME,DAY,DAYNAME,DAY_WEEK,DAY_WEEKNAME,YEAR,HOUR,HOURNAME,MINUTE,MINUTENAME,TWAY_ID,TWAY_ID2,ROUTE,ROUTENAME,RUR_URB,RUR_URBNAME,FUNC_SYS,FUNC_SYSNAME,RD_OWNER,RD_OWNERNAME,NHS,NHSNAME,SP_JUR,SP_JURNAME,MILEPT,MILEPTNAME,LATITUDE,LATITUDENAME,LONGITUD,LONGITUDNAME,HARM_EV,HARM_EVNAME,MAN_COLL,MAN_COLLNAME,RELJCT1,RELJCT1NAME,RELJCT2,RELJCT2NAME,TYP_INT,TYP_INTNAME,REL_ROAD,REL_ROADNAME,WRK_ZONE,WRK_ZONENAME,LGT_COND,LGT_CONDNAME,WEATHER,WEATHERNAME,SCH_BUS,SCH_BUSNAME,RAIL,RAILNAME,NOT_HOUR,NOT_HOURNAME,NOT_MIN,NOT_MINNAME,ARR_HOUR,ARR_HOURNAME,ARR_MIN,ARR_MINNAME,HOSP_HR,HOSP_HRNAME,HOSP_MN,HOSP_MNNAME,FATALS
# 2001 accidents table
# STATE,COUNTY,MONTH,DAY,HOUR,MINUTE,VE_FORMS,PERSONS,PEDS,NHS,ROAD_FNC,ROUTE,SP_JUR,HARM_EV,MAN_COLL,REL_JUNC,REL_ROAD,TRAF_FLO,NO_LANES,SP_LIMIT,ALIGNMNT,PROFILE,PAVE_TYP,SUR_COND,TRA_CONT,T_CONT_F,HIT_RUN,LGT_COND,WEATHER,C_M_ZONE,NOT_HOUR,NOT_MIN,ARR_HOUR,ARR_MIN,HOSP_HR,HOSP_MN,SCH_BUS,CF1,CF2,CF3,FATALS,DAY_WEEK,DRUNK_DR,ST_CASE,CITY,MILEPT,YEAR,TWAY_ID,RAIL,latitude,longitud