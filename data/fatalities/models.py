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
        (1, 'Convertible/Cabriolet'),
        (2, 'Minivan'),
        (3, 'Coupe'),
        (4, 'Low Speed Vehicle (LSV)/Neighborhood Electric Vehicle (NEV)'),
        (5, 'Hatchback/Liftback/Notchback'),
        (6, 'Motorcycle - Standard'),
        (7, 'Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)'),
        (8, 'Crossover Utility Vehicle (CUV)'),
        (9, 'Van'),
        (10, 'Roadster'),
        (11, 'Truck'),
        (12, 'Motorcycle - Scooter'),
        (13, 'Sedan/Saloon'),
        (15, 'Wagon'),
        (16, 'Bus'),
        (60, 'Pickup'),
        (62, 'Incomplete - Cutaway*'),
        (63, 'Incomplete - Chassis Cab (Single Cab)*'),
        (64, 'Incomplete - Glider*'),
        (65, 'Incomplete*'),
        (66, 'Truck-Tractor'),
        (67, 'Incomplete - Stripped Chassis*'),
        (68, 'Streetcar/Trolley'),
        (69, 'Off-Road Vehicle - All Terrain Vehicle (ATV) (Motorcycle-Style)'),
        (70, 'Incomplete - Chassis Cab (Double Cab)*'),
        (71, 'Incomplete - School Bus Chassis*'),
        (72, 'Incomplete - Commercial Bus Chassis*'),
        (73, 'Bus - School Bus'),
        (74, 'Incomplete - Chassis Cab (Number of Cab Unknown)*'),
        (75, 'Incomplete - Transit Bus Chassis*'),
        (76, 'Incomplete - Motor Coach Chassis*'),
        (77, 'Incomplete - Shuttle Bus Chassis*'),
        (78, 'Incomplete - Motor Home Chassis*'),
        (80, 'Motorcycle - Sport'),
        (81, 'Motorcycle - Touring/Sport Touring'),
        (82, 'Motorcycle - Cruiser'),
        (83, 'Motorcycle - Trike'),
        (84, 'Off-Road Vehicle - Dirt Bike/Off-Road'),
        (85, 'Motorcycle - Dual Sport/Adventure/Supermoto/On/Off-Road'),
        (86, 'Off-Road Vehicle - Enduro (off-road long-distance racing)'),
        (87, 'Motorcycle - Small/Minibike'),
        (88, 'Off-Road Vehicle - Go Kart'),
        (90, 'Motorcycle - Side Car'),
        (94, 'Motorcycle - Custom'),
        (95, 'Cargo Van'),
        (97, 'Off-Road Vehicle - Snowmobile'),
        (98, 'Motorcycle - Street'),
        (100, 'Motorcycle - Enclosed Three Wheeled/Enclosed Autocycle'),
        (103, 'Motorcycle - Unenclosed Three Wheeled/Open Autocycle'),
        (104, 'Motorcycle - Moped'),
        (105, 'Off-Road Vehicle - Recreational Off-Road Vehicle (ROV)'),
        (107, 'Incomplete - Bus Chassis*'),
        (108, 'Motorhome'),
        (109, 'Motorcycle - Cross Country'),
        (110, 'Motorcycle - Underbone'),
        (111, 'Step Van/Walk-in Van'),
        (112, 'Incomplete - Commercial Chassis*'),
        (113, 'Off-Road Vehicle - Motocross (Off-Road Short-Distance, Closed-Track Racing)'),
        (114, 'Motorcycle - Competition'),
        (117, 'Limousine'),
        (119, 'Sport Utility Truck (SUT)'),
        (124, 'Off-Road Vehicle - Golf Cart'),
        (125, 'Motorcycle - Unknown Body Type'),
        (126, 'Off-Road Vehicle - Farm Equipment'),
        (127, 'Off-Road Vehicle - Construction Equipment'),
        (128, 'Ambulance'),
        (129, 'Street Sweeper'),
        (130, 'Fire Apparatus'),
        (996, 'Motorized Bicycle (discontinued in 2022)'),
        (997, 'Other'),
        (998, 'Not Reported'),
        (999, 'Unknown')
    ]
    vpic_body_class = models.PositiveSmallIntegerField(choices=vpic_body_class_choices, default=999)
    #v14
    ncsa_make_choices = [
        (1, 'American Motors'),
        (2, 'Jeep/Kaiser-Jeep/Willys Jeep'),
        (3, 'AM General'),
        (6, 'Chrysler'),
        (7, 'Dodge'),
        (8, 'Imperial'),
        (9, 'Plymouth'),
        (10, 'Eagle'),
        (12, 'Ford'),
        (13, 'Lincoln'),
        (14, 'Mercury'),
        (18, 'Buick/Opel'),
        (19, 'Cadillac'),
        (20, 'Chevrolet'),
        (21, 'Oldsmobile'),
        (22, 'Pontiac'),
        (23, 'GMC'),
        (24, 'Saturn'),
        (25, 'Grumman'),
        (26, 'Coda (Since 2013)'),
        (29, 'Other Domestic Manufacturers'),
        (30, 'Volkswagen'),
        (31, 'Alfa Romeo'),
        (32, 'Audi'),
        (33, 'Austin/Austin Healey'),
        (34, 'BMW'),
        (35, 'Datsun/Nissan'),
        (36, 'Fiat'),
        (37, 'Honda'),
        (38, 'Isuzu'),
        (39, 'Jaguar'),
        (40, 'Lancia'),
        (41, 'Mazda'),
        (42, 'Mercedes-Benz'),
        (43, 'MG'),
        (44, 'Peugeot'),
        (45, 'Porsche'),
        (46, 'Renault'),
        (47, 'Saab'),
        (48, 'Subaru'),
        (49, 'Toyota'),
        (50, 'Triumph'),
        (51, 'Volvo'),
        (52, 'Mitsubishi'),
        (53, 'Suzuki'),
        (54, 'Acura'),
        (55, 'Hyundai'),
        (56, 'Merkur'),
        (57, 'Yugo'),
        (58, 'Infiniti'),
        (59, 'Lexus'),
        (60, 'Daihatsu'),
        (61, 'Sterling'),
        (62, 'Land Rover'),
        (63, 'Kia'),
        (64, 'Daewoo'),
        (65, 'Smart (Since 2010)'),
        (66, 'Mahindra (2011-2013)'),
        (67, 'Scion (Since 2012)'),
        (69, 'Other Imports'),
        (70, 'BSA'),
        (71, 'Ducati'),
        (72, 'Harley-Davidson'),
        (73, 'Kawasaki'),
        (74, 'Moto Guzzi'),
        (75, 'Norton'),
        (76, 'Yamaha'),
        (77, 'Victory'),
        (78, 'Other Make Moped (Since 2010)'),
        (79, 'Other Make Motored Cycle (Since 2010)'),
        (80, 'Brockway'),
        (81, 'Diamond Reo/Reo'),
        (82, 'Freightliner'),
        (83, 'FWD'),
        (84, 'International Harvester/Navistar'),
        (85, 'Kenworth'),
        (86, 'Mack'),
        (87, 'Peterbilt'),
        (88, 'Iveco/Magirus'),
        (89, 'White/Autocar, White/GMC'),
        (90, 'Bluebird'),
        (91, 'Eagle Coach'),
        (92, 'Gillig'),
        (93, 'MCI'),
        (94, 'Thomas Built'),
        (97, 'Not Reported (Since 2010)'),
        (98, 'Other Make'),
        (99, 'Unknown Make')
    ]
    ncsa_make = models.PositiveSmallIntegerField(choices=ncsa_make_choices, default=99)
    #v15
    ncsa_model = models.IntegerField(null=True, blank=True)
    #v16
    body_type_choices = [
        (1, 'Convertible (Excludes Sunroof, T-Bar)'),
        (2, '2-Door Sedan/Hardtop/Coupe'),
        (3, '3-Door/2-Door Hatchback'),
        (4, '4-Door Sedan/Hardtop'),
        (5, '5-Door/4-Door Hatchback'),
        (6, 'Station Wagon (Excluding Van- and Truck-Based)'),
        (7, 'Hatchback, Number of Doors Unknown'),
        (8, 'Sedan/Hardtop, Number of Doors Unknown (Since 1994)'),
        (9, 'Other or Unknown Automobile Type (Since 1994)'),
        (10, 'Auto-Based Pickup'),
        (11, 'Auto-Based Panel (Cargo Station Wagon, AutoBased Ambulance or Hearse)'),
        (12, 'Large Limousine (More Than Four Side Doors or Stretch Chassis)'),
        (13, 'Three-Wheel Automobile or Automobile Derivative'),
        (14, 'Compact Utility (ANSI D-16 Utility Vehicle Categories “Small” and “Midsize”)'),
        (15, 'Large Utility (ANSI D-16 Utility Vehicle Categories “Full Size” and “Large”)'),
        (16, 'Utility Station Wagon'),
        (17, '3-Door Coupe'),
        (19, 'Utility Unknown Body'),
        (20, 'Minivan'),
        (21, 'Large Van - Includes Van-Based Buses'),
        (22, 'Step Van or Walk-in Van (GVWR ≤ 10,000 lbs)'),
        (28, 'Other Van Type (Hi-Cube Van)'),
        (29, 'Unknown Van Type'),
        (33, 'Convertible Pickup'),
        (34, 'Light Pickup'),
        (39, 'Unknown (Pickup Style) Light Conventional Truck Type'),
        (40, 'Cab Chassis-Based (Includes Light Stake, Light Dump, Light Tow, Rescue Vehicles)'),
        (41, 'Truck-Based Panel'),
        (42, 'Light Vehicle-Based Motorhome (Chassis Mounted)'),
        (45, 'Other Light Conventional Truck Type (Includes Stretched Suburban Limousine)'),
        (48, 'Unknown Light Truck Type (Since 2013)'),
        (49, 'Unknown Light-Vehicle Type (Automobile, Utility Vehicle, Van or Light Truck)'),
        (50, 'School Bus'),
        (51, 'Cross-Country/Intercity Bus (i.e., Greyhound)'),
        (52, 'Transit Bus (City Bus)'),
        (55, 'Van-Based Bus (GVWR > 10,000 lbs) (Since 2011)'),
        (58, 'Other Bus Type'),
        (59, 'Unknown Bus Type'),
        (60, 'Step Van (GVWR > 10,000 lbs)'),
        (61, 'Single-Unit Straight Truck or Cab-Chassis (GVWR range 10,001 to 19,500 lbs) (Since 2011)'),
        (62, 'Single-Unit Straight Truck or Cab-Chassis (GVWR range 19,501 to 26,000 lbs) (Since 2011)'),
        (63, 'Single-Unit Straight Truck or Cab-Chassis (GVWR > 26,000 lbs) (Since 2011)'),
        (64, 'Single Unit Straight Truck or Cab-Chassis (GVWR Unknown) (Since 2011)'),
        (65, 'Medium/Heavy Vehicle-Based Motorhome'),
        (66, 'Truck/Tractor (Cab Only, or With Any Number of Trailing Units: Any Weight)'),
        (67, 'Medium/Heavy Pickup (GVWR > 10,000 lbs) (Since 2001)'),
        (71, 'Unknown if Single-Unit or Combination-Unit Medium Truck (GVWR range 10,001 to 26,000 lbs)'),
        (72, 'Unknown if Single-Unit or Combination-Unit Heavy Truck (GVWR > 26,000 lbs)'),
        (73, 'Camper or Motorhome, Unknown GVWR'),
        (78, 'Unknown Medium/Heavy Truck Type'),
        (79, 'Unknown Truck Type'),
        (80, 'Two Wheel Motorcycle (excluding motor scooters)'),
        (81, 'Moped (Since 2022)'),
        (82, 'Three-Wheel Motorcycle (2 Rear Wheels)'),
        (83, 'Off-Road Motorcycle'),
        (84, 'Motor Scooter'),
        (85, 'Unenclosed Three-Wheel Motorcycle/Unenclosed Autocycle (1 Rear Wheel)'),
        (86, 'Enclosed Three-Wheel Motorcycle/Enclosed Autocycle (1 Rear Wheel)'),
        (87, 'Unknown Three-Wheel Motorcycle Type'),
        (88, 'Other Motored Cycle Type (Mini-Bikes, Pocket Motorcycles, Pocket Bikes)'),
        (89, 'Unknown Motored Cycle Type'),
        (90, 'ATV (All-Terrain Vehicle; Includes 3 or 4 Wheels)'),
        (91, 'Snowmobile'),
        (92, 'Farm Equipment Other Than Trucks'),
        (93, 'Construction Equipment Other Than Trucks (Includes Graders)'),
        (94, 'Low-Speed Vehicle (LSV)/Neighborhood Electric Vehicle (NEV) (Since 2011)'),
        (95, 'Golf Cart (Since 2012)'),
        (96, 'Recreational Off-Highway Vehicle'),
        (97, 'Other Vehicle Type (Includes Go-Cart, Fork-Lift, City Street Sweeper, Dune/Swamp Buggy)'),
        (98, 'Not Reported'),
        (99, 'Unknown Body Type')
    ]
    body_type = models.PositiveSmallIntegerField(choices=body_type_choices, default=99)

    #V17
    final_stage_body_class_choices = [
        (0, 'Not Applicable'),
        (2, 'Minivan'),
        (4, 'Low-Speed Vehicle (LSV)'),
        (7, 'Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)'),
        (8, 'Crossover Utility Vehicle (CUV)'),
        (9, 'Van'),
        (11, 'Truck'),
        (15, 'Wagon'),
        (16, 'Bus'),
        (60, 'Pickup'),
        (66, 'Truck-Tractor'),
        (68, 'Streetcar/Trolley'),
        (73, 'Bus-School Bus'),
        (95, 'Cargo Van'),
        (108, 'Motorhome'),
        (111, 'Step Van/Walk-in Van'),
        (117, 'Limousine'),
        (119, 'Sport Utility Truck'),
        (128, 'Ambulance'),
        (129, 'Street Sweeper'),
        (130, 'Fire Apparatus'),
        (997, 'Other'),
        (998, 'Not Reported'),
        (999, 'Unknown')
    ]
    final_stage_body_class = models.PositiveSmallIntegerField(choices=final_stage_body_class_choices, default=999)
    # V18
    weight_rating_choices = [
        (11, 'Class 1: 6,000 lbs or less (2,722 kg or less)'),
        (12, 'Class 2: 6,001 - 10,000 lbs (2,722 - 4,536 kg)'),
        (13, 'Class 3: 10,001 - 14,000 lbs (4,536 - 6,350 kg)'),
        (14, 'Class 4: 14,001 - 16,000 lbs (6,350 - 7,258 kg)'),
        (15, 'Class 5: 16,001 - 19,500 lbs (7,258 - 8,845 kg)'),
        (16, 'Class 6: 19,501 - 26,000 lbs (8,845 - 11,794 kg)'),
        (17, 'Class 7: 26,001 - 33,000 lbs (11,794 - 14,969 kg)'),
        (18, 'Class 8: 33,001 lbs and above (14,969 kg and above)'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown')
    ]
    gross_vehicle_weight_rating_lower = models.PositiveSmallIntegerField(choices = weight_rating_choices, default = 99)
    gross_vehicle_weight_rating_upper = models.PositiveSmallIntegerField(choices = weight_rating_choices, default = 99)
    #v19 
    vehicle_trailing_choices = [
        (0, 'No Trailers'),
        (1, 'One Trailer'),
        (2, 'Two Trailers'),
        (3, 'Three or More Trailers'),
        (4, 'Yes, Number of Trailers Unknown'),
        (5, 'Vehicle Towing Another Motor Vehicle - Fixed Linkage'),
        (6, 'Vehicle Towing Another Motor Vehicle - Non-Fixed Linkage'),
        (7, 'Trailing Unit Other than a Trailer or Another Motor Vehicle'),
        (9, 'Unknown')
    ]
    vehicle_trailing = models.PositiveSmallIntegerField(choices=vehicle_trailing_choices, default=0)
    #V20
    trailer_vin_1= models.CharField(max_length=32, null=True, blank=True)
    trailer_vin_2= models.CharField(max_length=32, null=True, blank=True)
    trailer_vin_3= models.CharField(max_length=32, null=True, blank=True)
    #V21
    trailer_weight_rating_choices = [
        (0, 'No Trailer GVWR Required'),
        (11, 'Class 1: 6,000 lbs or less (2,722 kg or less)'),
        (12, 'Class 2: 6,001 - 10,000 lbs (2,722 - 4,536 kg)'),
        (13, 'Class 3: 10,001 - 14,000 lbs (4,536 - 6,350 kg)'),
        (14, 'Class 4: 14,001 - 16,000 lbs (6,350 - 7,258 kg)'),
        (15, 'Class 5: 16,001 - 19,500 lbs (7,258 - 8,845 kg)'),
        (16, 'Class 6: 19,501 - 26,000 lbs (8,845 - 11,794 kg)'),
        (17, 'Class 7: 26,001 - 33,000 lbs (11,794 - 14,969 kg)'),
        (18, 'Class 8: 33,001 lbs and above (14,969 kg and above)'),
        (77, 'No Trailing Units'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown')
    ]
    trailer_weight_rating_1 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=0)
    trailer_weight_rating_2 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=0)
    trailer_weight_rating_3 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=0)
    #v22 
    jackknife_choices = [
        (0, "Not an Articulated Vehicle"),
        (1, "No")
        (2, "Yes, First Event")
        (3, "Yes, Subsequent Event")
    ]
    jackknife = models.PositiveSmallIntegerField(choices=jackknife_choices, default=0)
    #V23
    mcid_issuing_authority_choices = [
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
        (57, "U.S. DOT"),
        (58, "MC/MX (ICC)"),
        (77, "Not Reported"),
        (88, "None"),
        (95, "Canada"),
        (96, "Mexico"),
        (99, "Unknown")
    ] 
    motor_carrier_issuing_authority = models.PositiveSmallIntegerField(choices=mcid_issuing_authority_choices, default=0)
    motor_carrier_identification_number = models.CharField(max_length=32, null=True, blank=True)

    #v24
    vehicle_configuration_choices = [
        (0, 'Not Applicable'),
        (1, 'Single-Unit Truck (2 Axles and GVWR More Than 10,000 lbs)'),
        (2, 'Single-Unit Truck (3 or More Axles)'),
        (4, 'Truck Pulling Trailer(s)'),
        (5, 'Truck Tractor (Bobtail)'),
        (6, 'Truck Tractor/Semi-Trailer'),
        (7, 'Truck Tractor/Double'),
        (8, 'Truck Tractor/Triple'),
        (10, 'Vehicle 10,000 lbs. or Less Placarded for Hazardous Materials'),
        (19, 'Vehicle More Than 10,000 lbs., Other'),
        (20, 'Bus/Large Van (Seats for 9-15 Occupants, Including Driver)'),
        (21, 'Bus (Seats for More Than 15 Occupants, Including Driver, 2010-Later)'),
        (88, 'Qualifying Vehicle, Unknown Configuration'),
        (98, 'Not Reported (2010-2012)'),
        (99, 'Unknown (Reported as Unknown, 2018-2019)')
    ]
    vehicle_configuration = models.PositiveSmallIntegerField(choices=vehicle_configuration_choices, default=0)

    #v25
    cargo_body_type_choices = [
        (0, 'Not Applicable'),
        (1, 'Van/Enclosed Box'),
        (2, 'Cargo Tank'),
        (3, 'Flatbed'),
        (4, 'Dump'),
        (5, 'Concrete Mixer'),
        (6, 'Auto Transporter'),
        (7, 'Garbage/Refuse'),
        (8, 'Grain/Chips/Gravel'),
        (9, 'Pole-Trailer'),
        (10, 'Log (Since 2007)'),
        (11, 'Intermodal Container Chassis'),
        (12, 'Vehicle Towing Another Motor Vehicle (Since 2007)'),
        (22, 'Bus'),
        (28, 'Not Reported (2010-2012)'),
        (96, 'No Cargo Body Type'),
        (97, 'Other'),
        (98, 'Unknown Cargo Body Type'),
        (99, 'Unknown (Reported as Unknown, 2018-2019)')
    ]
    cargo_body_type = models.PositiveSmallIntegerField(choices=cargo_body_type_choices, default=0)
    #v26a HAZ_INV
    hazardous_material_involvement = models.BooleanField(default=False)
    #v26B HAZPLAC
    placard_choices = [
        (0, "Not Applicable"),
        (1, "No"),
        (2, "Yes"),
        (8, "Not Reported")
    ]
    hazardous_material_placard = models.PositiveSmallIntegerField(choices=placard_choices, default=0)
    # V26C - HAZ_ID
    hazardous_material_id = models.IntegerField(null=True, blank=True)
    # v26D HAZ_CNO
    hazardous_material_class_number_choices = [
        (0, "Not Applicable"),
        (1, "Explosives"),
        (2, "Gases"),
        (3, "Flammable/Combustible Liquid"),
        (4, "Flammable Solid, Spontaneously Combustible, and Dangerous When Wet"),
        (5, "Oxidizer and Organic Peroxide"),
        (6, "Poison and Poison Inhalation Hazard"),
        (7, "Radioactive"),
        (8, "Corrosive"),
        (9, "Miscellaneous"),
        (88, "Not Reported")
    ]
    hazardous_material_class_number = models.PositiveSmallIntegerField(choices=hazardous_material_class_number_choices, default=0)
    # v26E HAZ_REL
    release_of_hazardous_material = models.PositiveSmallIntegerField(choices=placard_choices, default=0)
    #v27 
    bus_use_choices = [
        (0, "Not a Bus"),
        (1, "School"),
        (4, "Intercity"),
        (5, "Charter/Tour"),
        (6, "Transit/Commuter"),
        (7, "Shuttle"),
        (8, "Modified for Personal/Private Use"),
        (97, "Bus, Unknown Use"),
        (98, "Not Reported"),
        (99, "Reported as Unknown")

    ]
    bus_use = models.PositiveSmallIntegerField(choices=bus_use_choices, default=0)
    #v28
    special_vehicle_use_choices = [
        (0, 'No Special Use Noted'),
        (1, 'Taxi'),
        (2, 'Vehicle Used as School Transport'),
        (3, 'Vehicle Used as Other Bus'),
        (4, 'Military'),
        (5, 'Police'),
        (6, 'Ambulance (Since 1980)'),
        (7, 'Fire Truck (Since 1982)'),
        (8, 'Non-Transport Emergency Services Vehicle'),
        (10, 'Safety Service Patrols - Incident Response'),
        (11, 'Other Incident Response'),
        (12, 'Towing - Incident Response'),
        (19, 'Motor Vehicle Used for Vehicle Sharing Mobility'),
        (20, 'Motor Vehicle Used for Electronic Ride-Hailing'),
        (21, 'Mail Carrier'),
        (22, 'Public Utility'),
        (23, 'Rental Truck Over 10,000 lbs'),
        (24, 'Truck Operating With Crash Attenuator Equipment'),
        (99, 'Reported as Unknown (since 2018)')
    ]
    special_vehicle_use = models.PositiveSmallIntegerField(choices=special_vehicle_use_choices, default=0)
    #v29
    emergency_vehicle_use_choices = [
        (0, 'Not Applicable'),
        (2, 'Non-Emergency, Non-Transport'),
        (3, 'Non-Emergency Transport'),
        (4, 'Emergency Operation, Emergency Warning Equipment Not in Use'),
        (5, 'Emergency Operation, Emergency Warning Equipment in Use'),
        (6, 'Emergency Operation, Emergency Warning Equipment in Use Unknown'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown')
    ]
    emergency_vehicle_use = models.PositiveSmallIntegerField(choices=emergency_vehicle_use_choices, default=0)
    #v30
    travel_speed = models.PositiveSmallIntegerField(null=True, blank=True)
    #v31
    underride_override_choices = [
        (0, "No Underride or Override"),
        (1, "Underride"),
        (2, "Override"),
        (7, "Not Applicable"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    underride_override = models.PositiveSmallIntegerField(choices=underride_override_choices, default=0)
    #v32 
    rollover_choices = [
        (0, "No Rollover"),
        (3, "Rollover"),
        (8, "Not Applicable")
    ]
    rollover = models.PositiveSmallIntegerField(choices=rollover_choices, default=0)
    #v33 
    rollover_location_choices = [
        (0, "No Rollover"),
        (1, "On Roadway"),
        (2, "On Shoulder"),
        (3, "On Median/Separator"),
        (4, "In Gore"),
        (5, "On Roadside"),
        (6, "Outside of Trafficway"),
        (7, "In Parking Lane/Zone"),
        (8, "Not Applicable"),
        (9, "Unknown")
    ]
    rollover_location = models.PositiveSmallIntegerField(choices=rollover_location_choices, default=0)
    #V34A
    initial_contact_point_choices = [
        (0, "Non-Collision"),
        (1, "1 O'Clock"),
        (2, "2 O'Clock"),
        (3, "3 O'Clock"),
        (4, "4 O'Clock"),
        (5, "5 O'Clock"),
        (6, "6 O'Clock"),
        (7, "7 O'Clock"),
        (8, "8 O'Clock"),
        (9, "9 O'Clock"),
        (10, "10 O'Clock"),
        (11, "11 O'Clock"),
        (12, "12 O'Clock"),
        (13, "Top"),
        (14, "Undercarriage"),
        (18, "Cargo/Vehicle Parts Set-in-Motion"),
        (19, "Other Objects or Person Set-in-Motion"),
        (20, "Object Set in Motion, Unknown if Cargo/Vehicle Parts or Other"),
        (61, "Left"),
        (62, "Left-Front Side"),
        (63, "Left-Back Side")
        (81, "Right"),
        (82, "Right-Front Side"),
        (83, "Right-Back Side"),
        (98, "Not Reported"),
        (99, "Unknown")
    ] 
    initial_contact_point = models.PositiveSmallIntegerField(choices=initial_contact_point_choices, default=98)
    #v35
    extent_of_damage_choices = [
        (0, "No Damage"),
        (2, "Minor Damage"),
        (4, "Functional Damage"),
        (6, "Disabling Damage"),
        (7, "Damage Reported, Extent Unknown"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ] 
    extent_of_damage = models.PositiveSmallIntegerField(choices=extent_of_damage_choices, default=8)
    #v36
    vehicle_towed_choices = [
        (5, "Not Towed"),
        (6, "Towed"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]

    vehicle_towed = models.PositiveSmallIntegerField(choices=vehicle_towed_choices, default=8)
    #v38

    most_harmful_event_choices = [
        (1, 'Rollover/Overturn'),
        (2, 'Fire/Explosion'),
        (3, 'Immersion (or Partial Immersion, Since 2012)'),
        (4, 'Gas Inhalation'),
        (5, 'Fell/Jumped From Vehicle'),
        (6, 'Injured in Vehicle (Non-Collision)'),
        (7, 'Other Non-Collision'),
        (8, 'Pedestrian'),
        (9, 'Pedalcyclist'),
        (10, 'Railway Vehicle'),
        (11, 'Live Animal'),
        (12, 'Motor Vehicle In-Transport'),
        (14, 'Parked Motor Vehicle'),
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
        (31, 'Post, Pole or Other Support'),
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
        (54, 'MotorMotor Vehicle In-Transport Strikes or Is Struck by Cargo, Persons or Objects Setin-Motion From/by Another Motor Vehicle In-Transport'),
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
        (99, 'Unknown / Reported as Unknown (Since 2018)')
    ]
    most_harmful_event = models.PositiveSmallIntegerField(choices=most_harmful_event_choices, default=98)
    #v39
    fire_occurence = models.BooleanField(default=False)
    #v40a
    automated_driving_system_present_choices = [
        (0, "No"),
        (1, "Yes"),
        (98, "Not Reported"),
        (99, "Reported as Unknown")
    ]
    automated_driving_system_present = models.PositiveSmallIntegerField(choices=automated_driving_system_present_choices, default=98)
    #v40b
    automated_driving_system_level_choices = [
        (0, "No Automation"),
        (1, "Level 1 - Driver Assistance Present"),
        (2, "Level 2 - Partial Automation Present"),
        (3, "Level 3 - Conditional Automation Present"),
        (4, "Level 4 - High Automation Present"),
        (5, "Level 5 - Full Automation Present"),
        (9, "Automation Present, Level Unknown"),
        (98, "Not Reported"),
        (99, "Reported as Unknown")
    ]
    automated_driving_system_level = models.PositiveSmallIntegerField(choices=automated_driving_system_level_choices, default=98)
    
    automated_driving_system_engaged_choices = [
        (0, "No Automation"),
        (1, "Level 1 - Driver Assistance Engaged"),
        (2, "Level 2 - Partial Automation Engaged"),
        (3, "Level 3 - Conditional Automation Engaged"),
        (4, "Level 4 - High Automation Engaged"),
        (5, "Level 5 - Full Automation Engaged"),
        (6, "Automation Systems Engaged, Level Unknown"),
        (9, "Automation Systems Present, Unknown if Any Engaged"),
        (90, "Automation Systems Present, Not Engaged"),
        (98, "Not Reported"),
        (99, "Reported as Unknown")

    ]
    automated_driving_system_engaged = models.PositiveSmallIntegerField(choices=automated_driving_system_engaged_choices, default=98)
    combined_make_model_id = models.IntegerField(null=True, blank=True)
    #v150
    fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #v151
    driver_drinking_choices = [
        (0, "No Drinking"),
        (1, "Drinking"),
        (9, "Unknown")
    ]
    driver_drinking = models.PositiveSmallIntegerField(choices=driver_drinking_choices, default=9)
    #d4
    driver_present_choices = [
        (0, "No Driver Present/Not Applicable")
        (1, "Driver Present"),
        (9, "Unknown")
    ]
    driver_present = models.PositiveSmallIntegerField(choices=driver_present_choices, default=9)
    #d5
    drivers_license_state_choices = [
        (0, "No Driver Present (Since 2010)"),
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
        (57, "Other U.S. Driver's License (Since 2018)"),
        (93, "Indian Nation (Since 2009)"),
        (94, "U.S. Government"),
        (95, "Canada"),
        (96, "Mexico"),
        (97, "Other Foreign Country"),
        (98, "Not Reported"),
        (99, "Reported as Unknown")
    ]
    drivers_license_state = models.PositiveSmallIntegerField(choices=drivers_license_state_choices, default=98)
    #d6 
    driver_zip_code = models.IntegerField(null=True, blank=True)

    #d7a
    non_cdl_license_type_choices = [
        (0, "Not Licensed"),
        (1, "Full Driver License"),
        (2, "Intermediate Driver License"),
        (6, "No Driver Present/Unknown if Driver Present"),
        (7, "Learner's Permit"),
        (8, "Temporary License"),
        (9, "Unknown License Type")
    ]
    non_cdl_license_type = models.PositiveSmallIntegerField(choices=non_cdl_license_type_choices, default=9)

    #d7b
    non_cdl_license_status_choices = [
        (0, 'Not Licensed'),
        (1, 'Suspended'),
        (2, 'Revoked'),
        (3, 'Expired'),
        (4, 'Cancelled or Denied'),
        (5, "Single-Class License")
        (6, 'Valid'),
        (7, 'No Driver Present/Unknown if Driver'),
        (9, 'Unknown License Status')
    ]
    non_cdl_license_status = models.PositiveSmallIntegerField(choices=non_cdl_license_status_choices, default=9)
    #d8
    cdl_license_status_choices = [
        (0, "No Commercial Driver's License (CDL)"),
        (1, 'Suspended'),
        (2, 'Revoked'),
        (3, 'Expired'),
        (4, 'Cancelled or Denied'),
        (5, 'Disqualified'),
        (6, 'Valid'),
        (7, "Commercial Learner's Permit (CLP)"),
        (8, 'Other - Not Valid'),
        (97, 'No Driver Present/Unknown if Driver Present'),
        (99, 'Unknown License Status')
    ]
    cdl_license_status = models.PositiveSmallIntegerField(choices=cdl_license_status_choices, default=99)
    #d9
    cdl_endorsements_choices = [
        (0, 'No Endorsements Required for This Vehicle'),
        (1, 'Endorsements Required, Complied With'),
        (2, 'Endorsements Required, Not Complied With'),
        (3, 'Endorsements Required, Compliance Unknown'),
        (7, 'No Driver Present/Unknown if Driver Present'),
        (9, 'Unknown, if Required')
    ]
    cdl_endorsements = models.PositiveSmallIntegerField(choices=cdl_endorsements_choices, default=0)
    #d10
    license_compliance_with_class_of_vehicle_choices = [
        (0, 'Not Licensed'),
        (1, 'No License Required for This Class Vehicle'),
        (2, 'No Valid License for This Class Vehicle'),
        (3, 'Valid License for This Class Vehicle'),
        (6, 'No Driver Present/Unknown if Driver Present'),
        (8, 'Unknown if CDL and/or CDL Endorsement Required for This Vehicle'),
        (9, 'Unknown')
    ]
    license_compliance_with_class_of_vehicle = models.PositiveSmallIntegerField(choices=license_compliance_with_class_of_vehicle_choices, default=9)
    #d11
    compliance_with_license_restrictions_choices = [
        (0, "No Restrictions or Not Applicable"),
        (1, "Restrictions Complied With"),
        (2, "Restrictions Not Complied With"),
        (3, "Restrictions, Compliance Unknown"),
        (7, "No Driver Present/Unknown if Driver Present"),
        (9, "Unknown")
    ]
    compliance_with_license_restrictions = models.PositiveSmallIntegerField(choices=compliance_with_license_restrictions_choices, default=9)
    


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


