from django.db import models
from django.contrib.gis.db import models as gismodels

# Create your models here.

class State(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = "state"
        managed = True


class County(models.Model):
    state = models.ForeignKey(State, null=False, blank=False)
    id = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=512, null=False)

    class Meta:
        unique_together = [["state", "id"]]
        db_table = "county"
        managed = True

class City(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    county = models.ForeignKey(County, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=512, null=False)

    class Meta:
        db_table = "city"
        managed = True

class Accident(models.Model):
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    st_case = models.PositiveIntegerField(null=False)
    #c3
    number_of_persons_not_in_motor_vehicles = models.PositiveSmallIntegerField(default=0)
    #c3a
    number_of_persons_not_in_motor_vehicles_in_transport = models.PositiveSmallIntegerField(default=0)
    #c4
    number_of_vehicles = models.PositiveSmallIntegerField(default=0)
    #c4a
    number_of_vehicles_in_transit = models.PositiveSmallIntegerField(default=0)
    #c4b
    number_of_parked_vehicles = models.PositiveSmallIntegerField(default=0)
    #c5
    number_of_persons_in_motor_vehicles = models.PositiveSmallIntegerField(default=0)
    #c5a
    number_of_persons_in_motor_vehicles_in_transport = models.PositiveSmallIntegerField(default=0)
    # C6 County COUNTY 40
    county = models.ForeignKey(County, null=True, blank=True, on_delete = models.DO_NOTHING)
    # C7 City CITY 41
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.DO_NOTHING)
    # C8A Month of Crash MONTH 42
    months = [
        (1, "January"), (2, "February"), (3, "March"), (4, "April"), (5, "May"), (6, "June"), 
        (7, "July"), (8, "August"), (9, "September"), (10, "October"), (11, "November"), (12, "December"), (99, "Unknown")
    ]
    month = models.PositiveSmallIntegerField(choices=months, default=99)
    # C8B Day of Crash DAY 42
    day = models.PositiveSmallIntegerField(null=True, blank=True)
    # C8C Day of Week DAY_WEEK 43
    days_of_the_week = [(1, "Sunday"), (2, "Monday"), (3, "Tuesday"), (4, "Wednesday"), (5, "Thursday"), (6, "Friday"), (7, "Saturday"), (99, "Unknown")]
    day_of_the_week = models.PositiveSmallIntegerField(choices=days_of_the_week, default=99)
    # C8D Year of Crash YEAR 43
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    # C9A Hour of Crash HOUR 44
    hour = models.PositiveSmallIntegerField(null=True, blank=True)
    # C9B Minute of Crash MINUTE 44

    hour = models.PositiveSmallIntegerField(null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)

    #C10
    trafficway_identifier_1 = models.CharField(max_length=256, null=True, blank=True)
    trafficway_identifier_2 = models.CharField(max_length=256, null=True, blank=True)
    #c11
    route_signing_types = [
        (1, "Interstate"),
        (2, "U.S. Highway"),
        (3, "State Highway"),
        (4, "County Road"),
        (5, "Local Street - Township"),
        (6, "Local Street - Municipality"),
        (7, "Local Street - Frontage Road"),
        (8, "Other"),
        (9, "Unknown"),
    ]
    route_signing = models.PositiveSmallIntegerField(choices=route_signing_types, default=9)
    #C12A
    rural_urban_choices = [
        (1, "Rural"),
        (2, "Urban"),
        (6, "Trafficway Not In State Inventory"),
        (8, "Not Reported"),
        (9, "Unknown")
    ]
    rural_urban = models.PositiveSmallIntegerField(choices=rural_urban_choices, default=9)
    #C12B
    functional_system_choices = [
        (1, "Interstate"),
        (2, "Principal Arterial - Other Freeways and Expressways"),
        (3, "Principal Arterial -Other"),
        (4, "Minor Arterial"),
        (5, "Major Collector"), 
        (6, "Minor Collector")
        (7, "Local"),
        (96, "Trafficway Not In State Inventory"),
        (98, "Not Reported"),
        (99, "Unknown")

    ]
    functional_system = models.PositiveSmallIntegerField(choices=functional_system_choices, default=9)
    #C13
    road_owner_choices = [
        (1, 'State Highway Agency'),
        (2, 'County Highway Agency'),
        (3, 'Town or Township Highway Agency'),
        (4, 'City or Municipal Highway Agency'),
        (11, 'State Park, Forest or Reservation Agency'),
        (12, 'Local Park, Forest or Reservation Agency'),
        (21, 'Other State Agency'),
        (25, 'Other Local Agency'),
        (26, 'Private (other than Railroad)'),
        (27, 'Railroad'),
        (31, 'State Toll Road'),
        (32, 'Local Toll Authority'),
        (40, 'Other Public Instrumentality (i.e., Airport)'),
        (50, 'Indian Tribe Nation'),
        (60, 'Other Federal Agency'),
        (62, 'Bureau of Indian Affairs'),
        (63, 'Bureau of Fish and Wildlife'),
        (64, 'U.S. Forest Service'),
        (66, 'National Park Service'),
        (67, 'Tennessee Valley Authority'),
        (68, 'Bureau of Land Management'),
        (69, 'Bureau of Reclamation'),
        (70, 'Corps of Engineers'),
        (72, 'Air Force'),
        (74, 'Navy/Marines'),
        (80, 'Army'),
        (96, 'Trafficway Not in State Inventory'),
        (98, 'Not Reported'),
        (99, 'Unknown')
    ]
    road_owner = models.PositiveSmallIntegerField(choices=road_owner_choices, default=99)
    #C14
    national_highway_system_choices = [
        (0, "Not in the National Highway System"),
        (1, "Part of the National Highway System"),
        (9, "Unknown")
    ]
    national_highway_system = models.PositiveSmallIntegerField(choices=national_highway_system_choices, default=9)

    #c15
    special_jurisdiction_choices = [
        (0, 'No Special Jurisdiction (Includes National Forests Since 2008)'),
        (1, 'National Park Service'),
        (2, 'Military'),
        (3, 'Indian Reservation'),
        (4, 'College/University Campus'),
        (5, 'Other Federal Properties (Since 1977)'),
        (8, 'Other (Since 1976)'),
        (9, 'Unknown')
    ]
    special_jurisdiction = models.PositiveSmallIntegerField(choices=special_jurisdiction_choices, default=9)
    #c16
    milepoint = models.PositiveIntegerField(null=True, blank=True)
    #c17
    latitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
    longitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
    exact_location = gismodels.PointField(null=True, blank=True)
    exact_location_best_guess = gismodels.PointField(null=True, blank=True)
    #c19
    first_harmful_event_options = [
        (1, 'Rollover/Overturn'),
        (2, 'Fire/Explosion'),
        (3, 'Immersion or Partial Immersion (Since 2012)'),
        (4, 'Gas Inhalation'),
        (5, 'Fell/Jumped From Vehicle'),
        (6, 'Injured in Vehicle (Non-Collision)'),
        (7, 'Other Non-Collision'),
        (8, 'Pedestrian'),
        (9, 'Pedalcyclist'),
        (10, 'Railway Vehicle'),
        (11, 'Live Animal'),
        (12, 'Motor Vehicle In-Transport'),
        (14, 'Parked Motor Vehicle (Not In-Transport)'),
        (15, 'Non-Motorist on Personal Conveyance'),
        (16, 'Thrown or Falling Object'),
        (17, 'Boulder'),
        (18, 'Other Object (Not Fixed)'),
        (19, 'Building'),
        (20, 'Impact Attenuator/Crash Cushion'),
        (21, 'Bridge Pier or Support'),
        (23, 'Bridge Rail (Includes Parapet)'),
        (24, 'Guardrail Face'),
        (25, 'Concrete Traffic Barrier'),
        (26, 'Other Traffic Barrier'),
        (30, 'Utility Pole/Light Support'),
        (31, 'Post, Pole, or Other Supports'),
        (32, 'Culvert'),
        (33, 'Curb'),
        (34, 'Ditch'),
        (35, 'Embankment'),
        (38, 'Fence'),
        (39, 'Wall'),
        (40, 'Fire Hydrant'),
        (41, 'Shrubbery'),
        (42, 'Tree (Standing Only)'),
        (43, 'Other Fixed Object'),
        (44, 'Pavement Surface Irregularity (Ruts, Potholes, Grates, etc.)'),
        (45, 'Working Motor Vehicle'),
        (46, 'Traffic Signal Support'),
        (48, 'Snow Bank'),
        (49, 'Ridden Animal or Animal-Drawn Conveyance (Since 1998)'),
        (50, 'Bridge Overhead Structure'),
        (51, 'Jackknife (Harmful to This Vehicle)'),
        (52, 'Guardrail End'),
        (53, 'Mail Box'),
        (55, 'Motor Vehicle in Motion Outside the Trafficway (Since 2008)'),
        (57, 'Cable Barrier (Since 2008)'),
        (58, 'Ground'),
        (59, 'Traffic Sign Support'),
        (72, 'Cargo/Equipment Loss, Shift, or Damage (Harmful)'),
        (73, 'Object That Had Fallen From Motor Vehicle In-Transport'),
        (74, 'Road Vehicle on Rails'),
        (91, 'Unknown Object Not Fixed'),
        (93, 'Unknown Fixed Object'),
        (98, 'Harmful Event, Details Not Reported (Since 2019)'),
        (99, 'Reported as Unknown')
    ]
    first_harmful_event = models.PositiveSmallIntegerField(choices=first_harmful_event_options, default=98)
    #c20
    manner_of_collision_of_first_harmful_event_options = [
        (0,'First Harmful Event was Not a Collision with Motor Vehicle In-Transport'),
        (1,'Front-to-Rear'),
        (2,'Front-to-Front'),
        (6,'Angle'),
        (7,'Sideswipe - Same Direction'),
        (8,'Sideswipe - Opposite Direction'),
        (9,'Rear-to-Side'),
        (10,'Rear-to-Rear'),
        (11,'Other (End-Swipes and Others)'),
        (98,'Not Reported'),
        (99,'Reported as Unknown')
    ]
    manner_of_collision_of_first_harmful_event = models.PositiveSmallIntegerField(choices=manner_of_collision_of_first_harmful_event_options, default=98)
    #c21B RELJCT1
    at_intersection_options = [
        (0, "No"),
        (1, "Yes"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    
    at_intersection = models.PositiveSmallIntegerField(choices=at_intersection_options, default=8)
#      2010- 2018- 
    #c23
    relation_to_junction_options = [
        (1,'Non-Junction'),
        (2,'Intersection'),
        (3,'Intersection Related'),
        (4,'Driveway Access'),
        (5,'Entrance/Exit Ramp Related'),
        (6,'Railway Grade Crossing'),
        (7,'Crossover Related'),
        (8,'Driveway Access Related'),
        (16,'Shared-Use Path Crossing'),
        (17,'Acceleration/Deceleration Lane'),
        (18,'Through Roadway'),
        (19,'Other Location Within Interchange Area'),
        (20,'Entrance/Exit Ramp'),
        (98,'Not Reported'),
        (99,'Reported as Unknown')
    ]
    relation_to_junction = models.PositiveSmallIntegerField(choices=relation_to_junction_options, default=98)
    #c22
    type_of_intersection_options = [
        (1, "Not an Intersection"),
        (2, "Four-Way Intersection"),
        (3, "T-Intersection"),
        (4, "Y-Intersection"),
        (5, "Traffic Circle"),
        (6, "Roundabout"),
        (7, "Five-Point, or More"),
        (10, "L-Intersection"),
        (11, "Other Intersection Type"),
        (98, "Not Reported"),
        (99, "Reported as Unknown")
    ]
    type_of_intersection = models.PositiveSmallIntegerField(choices=type_of_intersection_options, default=98)
    #c23
    relation_to_road_options = [
        (1,'On Roadway'),
        (2,'On Shoulder'),
        (3,'On Median'),
        (4,'On Roadside'),
        (5,'Outside Trafficway'),
        (6,'Off Roadway - Location Unknown'),
        (7,'In Parking Lane/Zone'),
        (8,'Gore'),
        (10,'Separator'),
        (11,'Continuous Left-Turn Lane'),
        (12,'Pedestrian Refuge Island or Traffic Island'),
        (98,'Not Reported'),
        (99,'Reported as Unknown')
    ]
    relation_to_road = models.PositiveSmallIntegerField(choices=relation_to_road_options, default=98)
    #c24
    work_zone_options = [
        (0, "None"),
        (1, "Construction"),
        (2, "Maintenance")
        (3, "Utility"),
        (4, "Work Zone, Type Unknown")

    ]
    work_zone = models.PositiveSmallIntegerField(choices=work_zone_options, default=0)
    #c25
    light_condition_options = [
        (1,'Daylight'),
        (2,'Dark - Not Lighted'),
        (3,'Dark - Lighted'),
        (4,'Dawn'),
        (5,'Dusk'),
        (6,'Dark - Unknown Lighting'),
        (7,'Other'),
        (8,'Not Reported'),
        (9,'Reported as Unknown')
    ]
    light_condition = models.PositiveSmallIntegerField(choices=light_condition_options, default=8) 
    #c26
    atmospheric_condition_options = [
        (1,'Clear'),
        (2,'Rain'),
        (3,'Sleet, Hail'),
        (4,'Snow'),
        (5,'Fog, Smog, Smoke'),
        (6,'Severe Crosswinds'),
        (7,'Blowing Sand, Soil, Dirt'),
        (8,'Other'),
        (10,'Cloudy'),
        (11,'Blowing Snow'),
        (12,'Freezing Rain or Drizzle'),
        (98,'Not Reported'),
        (99,'Unknown/')
    ]
    atmospheric_condition = models.PositiveSmallIntegerField(choices=atmospheric_condition_options, default=98) 
    #c27
    school_bus_related = models.BooleanField(null=False, blank=False, default=0)
    #c28
    rail_grade_crossing_identifier = models.CharField(null=True, blank=True) #seven-char string
    #c29a
    ems_notified_hour = models.PositiveSmallIntegerField(null=True, blank=True)
    #c29b
    ems_notified_minute = models.PositiveSmallIntegerField(null=True, blank=True)
    #c30A
    ems_arrived_hour = models.PositiveSmallIntegerField(null=True, blank=True)
    #c30B
    ems_arrived_minute = models.PositiveSmallIntegerField(null=True, blank=True)
    #c31A
    arrived_at_hospital_hour = models.PositiveSmallIntegerField(null=True, blank=True)
    #c31B
    arrived_at_hospital_minute = models.PositiveSmallIntegerField(null=True, blank=True)
    #c101
    fatalities = models.PositiveSmallIntegerField(null=False, blank=False)

    # #discontinued 2008
    # hit_and_run
    # #discontinued 2015 DRUNK_DR
    # num_drunk_drivers 
    # # discontinued ALIGNMNT
    # roadway_alignment
    # #discontinued ROAD_FNC
    # roadway_function
    # # discontinued PROFILE
    # roadway_profile
    # # discontinued SUR_COND
    # roadway_surface_condition
    # # discontinued PAVE_TYP
    # pavement_type
    # # discontinued SP_LIMIT
    # speed_limit
    # # discontinued NO_LANES
    # num_lanes_in_roadway
    # # discontinued TRA_CONT
    # traffic_control_device # This one needs a huge table
    # # discontinued T_CONT_F
    # traffic_control_device_functioning

    

class Vehicle(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    accident = models.ForeignKey(Accident, on_delete=models.DO_NOTHING)
    vehicle_number = models.PositiveSmallIntegerField(null=False)
    #v4
    number_of_occupants = models.PositiveSmallIntegerField(null=True, blank=True)
    # v6
    hit_and_run_choices = [
        (0, "No Hit and Run"),
        (1, "Hit and Run"),
        (9, "Unknown")
    ]
    hit_and_run = models.PositiveSmallIntegerField(choices=hit_and_run_choices, default=0) 
    #v7 
    registration_state_choices = [
        (0, "Not Applicable"),
        (1, 'Alabama'),
        (2, 'Alaska'),
        (3, 'American Samoa'),
        (4, 'Arizona'),
        (5, 'Arkansas'),
        (6, 'California'),
        (8, 'Colorado'),
        (9, 'Connecticut'),
        (10, 'Delaware'),
        (11, 'District of Columbia'),
        (12, 'Florida'),
        (13, 'Georgia'),
        (14, 'Guam'),
        (15, 'Hawaii'),
        (16, 'Idaho'),
        (17, 'Illinois'),
        (18, 'Indiana'),
        (19, 'Iowa'),
        (20, 'Kansas'),
        (21, 'Kentucky'),
        (22, 'Louisiana'),
        (23, 'Maine'),
        (24, 'Maryland'),
        (25, 'Massachusetts'),
        (26, 'Michigan'),
        (27, 'Minnesota'),
        (28, 'Mississippi'),
        (29, 'Missouri'),
        (30, 'Montana'),
        (31, 'Nebraska'),
        (32, 'Nevada'),
        (33, 'New Hampshire'),
        (34, 'New Jersey'),
        (35, 'New Mexico'),
        (36, 'New York'),
        (37, 'North Carolina'),
        (38, 'North Dakota'),
        (39, 'Ohio '),
        (40, 'Oklahoma'),
        (41, 'Oregon'),
        (42, 'Pennsylvania'),
        (43, 'Puerto Rico'),
        (44, 'Rhode Island'),
        (45, 'South Carolina'),
        (46, 'South Dakota'),
        (47, 'Tennessee'),
        (48, 'Texas'),
        (49, 'Utah'),
        (50, 'Vermont'),
        (51, 'Virginia'),
        (52, 'Virgin Islands'),
        (53, 'Washington'),
        (54, 'West Virginia'),
        (55, 'Wisconsin'),
        (56, 'Wyoming'),
        (91, "Not Reported"),
        (92, "No Registration"),
        (93, "Multiple State Registrations"),
        (94, "US Government / Military"),
        (95, "Canada"),
        (96, "Mexico"),
        (97, "Other Foreign Country"),
        (98, "Other Registration"),
        (99, "Unknown")
    ]
    registration_state = models.PositiveSmallIntegerField(choices=registration_state_choices, default=99)
    #v8 registered vehicle owner
    registered_vehicle_owner_choices = [
        (0, 'Not Applicable, Vehicle Not Registered'),
        (1, 'Driver (in This Crash) Was Registered Owner'),
        (2, 'Driver (in This Crash) Not Registered Owner (Other Private Owner)'),
        (3, 'Vehicle Registered as Commercial/Business/Company/Government'),
        (4, 'Vehicle Registered as Rental Vehicle'),
        (5, 'Vehicle Was Stolen (Reported by Police)'),
        (6, 'Driverless/Motor Vehicle Parked/Stopped off Roadway'),
        (9, 'Unknown')
    ]
    registered_vehicle_owner = models.PositiveSmallIntegerField(choices=registered_vehicle_owner_choices, default=9)
    #v9
    vehicle_identification_number = models.CharField(max_length=32, null=True, blank=True)
    #v10 
    vehicle_model_year = models.PositiveSmallIntegerField(null=True, blank=True)
    # V11
    vpic_make = models.PositiveSmallIntegerField(null=True, blank=True)
    # V12
    vpic_model = models.PositiveIntegerField(null=True, blank=True)
    # V13
    vpic_body_class_choices = [
          
    ]
    vpic_body_class = models.PositiveSmallIntegerField()
    #v14
    ncsa_make 
    #v15
    ncsa_model 
    #v16
    body_type 
    #v19 
    vehicle_trailing  
    #v22 
    jackknife  


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
    special_vehicle_use  
    #v29
    emergency_vehicle_use  
    #v30
    travel_speed
    #v32 
    rollover  
    #V34A
    initial_contact_point   
    #v35
    extent_of_damage   
    #v36
    vehicle_towed 
    #v38
    most_harmful_event 
    #v39
    fire_occurence  
    #v40a
    automation_system_present  
    #v40b
    type_of_automation_system_present  
    #v40c
    type_of_automation_system_engaged  
    #v150
    fatalities
    #v151
    driver_drinking 
    #d4
    driver_presence 
    #d5
    driver_license_state 
    #d6 DRIMPAIR
    driver_zip_code
    #d7b
    non_cdl_license_status 
    #d8
    cdl_license_status 
    #d10
    license_compliance_with_class_of_vehicle 
    #d11
    compliance_with_license_restrictions 
    #d12 (inches)
    driver_height
    #d13 (lbs)
    driver_weight
    #d14
    previous_recorded_crashes 
    #d16
    previous_dwi_convictions 
    #d17
    previous_speeding_convictions 
    #d18
    previous_other_moving_violations 
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
    roadway_alignment 
    #pc9
    roadway_grade 
    #pc10
    roadway_surface_type 
    #pc11
    roadway_surface_condition 
    #pc12
    traffic_control_device 
    #pc13
    traffic_control_device_functioning 
    

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