from django.db import models
from django.contrib.gis.db import models as gismodels

import time

# Create your models here.

class State(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    short_name = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = "state"
        managed = True


class County(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    state = models.ForeignKey(State, null=False, blank=False, on_delete=models.DO_NOTHING)
    county_id = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=512, null=False)

    class Meta:
        unique_together = [["state", "county_id"]]
        db_table = "county"
        managed = True

class City(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    city_id = models.PositiveIntegerField(null=False, blank=False)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=512, null=False)

    class Meta:
        unique_together = [["state", "city_id"]]
        db_table = "city"
        managed = True

# in a just world, I would name this model "Crash" but we do not live in a just world and I'm striving for code quality here over personal vendettas
class Accident(models.Model):
    def accident(self):
        return self
    def coordinates(self):
        if not self.longitude or not self.latitude:
            return [-999.9999,99.9999]
        return [self.longitude, self.latitude]
    def link(self):
        return f"<a href='/accidents/{self.id}'>Details Here</a>"
    def map_link(self):
        return f"<a href='https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}'>Google Maps</a>"
    
    id = models.PositiveBigIntegerField(primary_key = True)
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    st_case = models.PositiveIntegerField(null=False)
    #c3
    number_of_persons_not_in_motor_vehicles = models.PositiveSmallIntegerField(default=0)
    #c3a
    number_of_persons_not_in_motor_vehicles_in_transport = models.PositiveSmallIntegerField(default=0)
    #c4
    number_of_vehicles = models.PositiveSmallIntegerField(default=0)
    #c4a
    number_of_vehicles_in_transport = models.PositiveSmallIntegerField(default=0)
    #c4b
    number_of_parked_vehicles = models.PositiveSmallIntegerField(default=0)
    #c5
    number_of_persons_in_motor_vehicles = models.PositiveSmallIntegerField(default=0)
    #c5a
    number_of_persons_in_motor_vehicles_in_transport = models.PositiveSmallIntegerField(default=0)

    @property
    def number_of_persons_in_parked_vehicles(self):
        return self.number_of_persons_in_motor_vehicles - self.number_of_persons_in_motor_vehicles_in_transport
    
    state = models.ForeignKey(State, null=True, blank=True, on_delete = models.DO_NOTHING)
    # C6 County COUNTY 40
    county = models.ForeignKey(County, null=True, blank=True, on_delete = models.DO_NOTHING)
    # C7 City CITY 41
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.DO_NOTHING)
    # C8A Month of Crash MONTH 42
    month_choices = [
        (1, "January"), 
        (2, "February"), 
        (3, "March"), 
        (4, "April"), 
        (5, "May"), 
        (6, "June"), 
        (7, "July"), 
        (8, "August"), 
        (9, "September"), 
        (10, "October"), 
        (11, "November"), 
        (12, "December"), 
        (99, "Unknown")
    ]
    month = models.PositiveSmallIntegerField(choices=month_choices, default=99)
    # C8B Day of Crash DAY 42
    day = models.PositiveSmallIntegerField(null=True, blank=True)
    # C8C Day of Week DAY_WEEK 43
    day_of_the_week_choices = [
        (1, "Sunday"), 
        (2, "Monday"), 
        (3, "Tuesday"), 
        (4, "Wednesday"), 
        (5, "Thursday"), 
        (6, "Friday"), 
        (7, "Saturday"), 
        (99, "Unknown")
    ]
    day_of_the_week = models.PositiveSmallIntegerField(choices=day_of_the_week_choices, default=99)
    # C8D Year of Crash YEAR 43
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    # C9A Hour of Crash HOUR 44
    hour = models.PositiveSmallIntegerField(null=True, blank=True)
    # C9B Minute of Crash MINUTE 44
    minute = models.PositiveSmallIntegerField(null=True, blank=True)

    datetime = models.DateTimeField(null=True, blank=True)
    datetime_is_estimated = models.BooleanField(default=True)

    #C10
    trafficway_identifier_1 = models.CharField(max_length=256, null=True, blank=True)
    trafficway_identifier_2 = models.CharField(max_length=256, null=True, blank=True)
    #c11
    route_signing_choices = [
        (0, "Not Signed"),
        (1, "Interstate"),
        (2, "U.S. Highway"),
        (3, "State Highway"),
        (4, "County"),
        (5, "Township"),
        (6, "Municipal"),
        (7, "Local Street - Frontage Road"),
        (8, "Other"),
        # (9, "Unknown"),
        (10, "Parkway Marker or Forest Route Marker"),
        (11, "Off-Interstate Business Marker"),
        (12, "Secondary Route"), 
        (13, "Bureau of Indian Affairs"),
        (95, "Other"),
        (96, "Trafficway Not in State Inventory"),
        (99, "Unknown/Not Reported")
    ]
    route_signing = models.PositiveSmallIntegerField(choices=route_signing_choices, default=9)
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
        (2, "Other Freeways and Expressways"),
        (3, "Other Principal Arterial"),
        (4, "Minor Arterial"),
        (5, "Major Collector"), 
        (6, "Minor Collector"),
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
        (26, 'Private (Other Than Railroad)'),
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
        (95, 'Other'),
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
    location = gismodels.PointField(null=True, blank=True, geography=True)
    location_is_estimated = models.BooleanField(default=True)
    
    #c19
    first_harmful_event_choices = [
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
        (54, 'Motor Vehicle In-Transport Strikes or Is Struck by Cargo, Persons or Objects Setin-Motion From/by Another Motor Vehicle In-Transport'),
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
    first_harmful_event = models.PositiveSmallIntegerField(choices=first_harmful_event_choices, default=99)
    #c20
    manner_of_collision_of_first_harmful_event_choices = [
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
    manner_of_collision_of_first_harmful_event = models.PositiveSmallIntegerField(choices=manner_of_collision_of_first_harmful_event_choices, default=98)
    #c21B RELJCT1
    within_interchange_area_choices = [
        (0, "No"),
        (1, "Yes"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    
    within_interchange_area = models.PositiveSmallIntegerField(choices=within_interchange_area_choices, default=8)
#      2010- 2018- 
    #c23
    relation_to_junction_choices = [
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
    relation_to_junction = models.PositiveSmallIntegerField(choices=relation_to_junction_choices, default=98)
    #c22
    type_of_intersection_choices = [
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
    type_of_intersection = models.PositiveSmallIntegerField(choices=type_of_intersection_choices, default=98)
    #c23
    relation_to_road_choices = [
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
    relation_to_road = models.PositiveSmallIntegerField(choices=relation_to_road_choices, default=98)
    #c24
    work_zone_choices = [
        (0, "None"),
        (1, "Construction"),
        (2, "Maintenance"),
        (3, "Utility"),
        (4, "Work Zone, Type Unknown")

    ]
    work_zone = models.PositiveSmallIntegerField(choices=work_zone_choices, default=0)
    #c25
    light_condition_choices = [
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
    light_condition = models.PositiveSmallIntegerField(choices=light_condition_choices, default=8) 
    #c26
    atmospheric_condition_choices = [
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
    atmospheric_condition = models.PositiveSmallIntegerField(choices=atmospheric_condition_choices, default=98) 
    #c27
    school_bus_related = models.BooleanField(null=False, blank=False, default=0)
    #c28
    rail_grade_crossing_identifier = models.CharField(null=True, blank=True, max_length = 64) #seven-char string
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

    def nonmotorist_set(self):
        return self.person_set.filter(vehicle__vehicle_number__isnull=True, parked_vehicle__vehicle_number__isnull=True)

    @property
    def data(self):
        return f"/accidents/{self.id}"
    
    class Meta:
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["datetime"]),
        ]
        unique_together = [["year", "st_case"]]
        db_table = "accident"
        managed = True

class Vehicle(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    accident = models.ForeignKey(Accident, on_delete=models.CASCADE)
    vehicle_number = models.PositiveSmallIntegerField(null=False)
    #v4
    number_of_occupants = models.PositiveSmallIntegerField(null=True, blank=True)
    # v6
    hit_and_run_choices = [
        (0, "No Hit and Run"),
        (1, "Hit and Run"),
        (9, "Unknown")
    ]
    hit_and_run = models.PositiveSmallIntegerField(choices=hit_and_run_choices, default=9) 
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
    vpic_make = models.PositiveIntegerField(null=True, blank=True)
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
        (62, 'Incomplete - Cutaway'),
        (63, 'Incomplete - Chassis Cab (Single Cab)'),
        (64, 'Incomplete - Glider'),
        (65, 'Incomplete'),
        (66, 'Truck-Tractor'),
        (67, 'Incomplete - Stripped Chassis'),
        (68, 'Streetcar/Trolley'),
        (69, 'Off-Road Vehicle - All Terrain Vehicle (ATV) (Motorcycle-Style)'),
        (70, 'Incomplete - Chassis Cab (Double Cab)'),
        (71, 'Incomplete - School Bus Chassis'),
        (72, 'Incomplete - Commercial Bus Chassis'),
        (73, 'Bus - School Bus'),
        (74, 'Incomplete - Chassis Cab (Number of Cab Unknown)'),
        (75, 'Incomplete - Transit Bus Chassis'),
        (76, 'Incomplete - Motor Coach Chassis'),
        (77, 'Incomplete - Shuttle Bus Chassis'),
        (78, 'Incomplete - Motor Home Chassis'),
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
        (107, 'Incomplete - Bus Chassis'),
        (108, 'Motorhome'),
        (109, 'Motorcycle - Cross Country'),
        (110, 'Motorcycle - Underbone'),
        (111, 'Step Van/Walk-in Van'),
        (112, 'Incomplete - Commercial Chassis'),
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
        (95, "Other Truck/Bus"),
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
    gross_vehicle_weight_rating_lower = models.PositiveSmallIntegerField(choices = weight_rating_choices, default = 98)
    gross_vehicle_weight_rating_upper = models.PositiveSmallIntegerField(choices = weight_rating_choices, default = 98)
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
    vehicle_trailing = models.PositiveSmallIntegerField(choices=vehicle_trailing_choices, default=9)
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
    trailer_weight_rating_1 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=98)
    trailer_weight_rating_2 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=98)
    trailer_weight_rating_3 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=98)
    #v22 
    jackknife_choices = [
        (0, "Not an Articulated Vehicle"),
        (1, "No"),
        (2, "Yes, First Event"),
        (3, "Yes, Subsequent Event")
    ]
    jackknife = models.PositiveSmallIntegerField(choices=jackknife_choices, default=0)
    
    #V23
    motor_carrier_identification_number = models.CharField(max_length=32, null=True, blank=True)

    #v24
    vehicle_configuration_choices = [
        (0, 'Not Applicable'),
        (1, 'Single-Unit Truck (2 Axles and GVWR More Than 10,000 lbs)'),
        (2, 'Single-Unit Truck (3 or More Axles)'),
        (3, "Single-Unit Truck (Unknown Number of Axles, Tires)"),
        (4, 'Truck Pulling Trailer(s)'),
        (5, 'Truck Tractor (Bobtail)'),
        (6, 'Truck Tractor/Semi-Trailer'),
        (7, 'Truck Tractor/Double'),
        (8, 'Truck Tractor/Triple'),
        (10, 'Vehicle 10,000 lbs. or Less Placarded for Hazardous Materials'),
        (19, 'Vehicle More Than 10,000 lbs., Other'),
        (20, 'Bus/Large Van (Seats for 9-15 Occupants, Including Driver)'),
        (21, 'Bus (Seats for More Than 15 Occupants, Including Driver, 2010-Later)'),
        (70, "Light Truck (Van, Mini-Van, Panel, Pickup, Sport Utility Vehicle Displaying a Hazardous Materials Placard)"),
        (80, "Passenger Car (Only When Displaying a Hazardous Materials Placard)"),
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
    hazardous_material_placard = models.PositiveSmallIntegerField(choices=placard_choices, default=8)
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
    hazardous_material_class_number = models.PositiveSmallIntegerField(choices=hazardous_material_class_number_choices, default=88)
    # v26E HAZ_REL
    release_of_hazardous_material_choices = [
        (0, "Not Applicable"),
        (1, "No"),
        (2, "Yes"),
        (8, "Not Reported")
    ]
    release_of_hazardous_material = models.PositiveSmallIntegerField(choices=release_of_hazardous_material_choices, default=8)
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
    bus_use = models.PositiveSmallIntegerField(choices=bus_use_choices, default=98)
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
        (98, "Not Reported"),
        (99, 'Reported as Unknown (since 2018)')
    ]
    special_vehicle_use = models.PositiveSmallIntegerField(choices=special_vehicle_use_choices, default=0)
    #v29
    emergency_vehicle_use_choices = [
        (0, 'Not Applicable'),
        (1, "Yes"),
        (2, 'Non-Emergency, Non-Transport'),
        (3, 'Non-Emergency Transport'),
        (4, 'Emergency Operation, Emergency Warning Equipment Not in Use'),
        (5, 'Emergency Operation, Emergency Warning Equipment in Use'),
        (6, 'Emergency Operation, Emergency Warning Equipment in Use Unknown'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown')
    ]
    emergency_vehicle_use = models.PositiveSmallIntegerField(choices=emergency_vehicle_use_choices, default=8)
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
    underride_override = models.PositiveSmallIntegerField(choices=underride_override_choices, default=8)
    #v32 
    rollover_choices = [
        (0, "No Rollover"),
        (3, "Rollover"),
        (8, "Not Applicable")
    ]
    rollover = models.PositiveSmallIntegerField(choices=rollover_choices, default=8)
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
    rollover_location = models.PositiveSmallIntegerField(choices=rollover_location_choices, default=9)
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
        (15, "Underride"),
        (16, "Override"),
        (18, "Cargo/Vehicle Parts Set-in-Motion"),
        (19, "Other Objects or Person Set-in-Motion"),
        (20, "Object Set in Motion, Unknown if Cargo/Vehicle Parts or Other"),
        (61, "Left"),
        (62, "Left-Front Side"),
        (63, "Left-Back Side"),
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
    most_harmful_event = models.PositiveSmallIntegerField(choices=most_harmful_event_choices, default=99)
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
        (0, "No Driver Present/Not Applicable"),
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
    drivers_license_state = models.PositiveSmallIntegerField(choices=drivers_license_state_choices, default=98, null=True, blank=True)
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
    non_cdl_license_type = models.PositiveSmallIntegerField(choices=non_cdl_license_type_choices, default=9, null=True, blank=True)

    #d7b
    non_cdl_license_status_choices = [
        (0, 'Not Licensed'),
        (1, 'Suspended'),
        (2, 'Revoked'),
        (3, 'Expired'),
        (4, 'Cancelled or Denied'),
        (5, "Single-Class License"),
        (6, 'Valid'),
        (7, 'No Driver Present/Unknown if Driver'),
        (9, 'Unknown License Status')
    ]
    non_cdl_license_status = models.PositiveSmallIntegerField(choices=non_cdl_license_status_choices, default=9, null=True, blank=True)
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
        (98, "Not Reported"),
        (99, 'Unknown License Status')
    ]
    cdl_license_status = models.PositiveSmallIntegerField(choices=cdl_license_status_choices, default=99, null=True, blank=True)
    #d9
    cdl_endorsements_choices = [
        (0, 'No Endorsements Required for This Vehicle'),
        (1, 'Endorsements Required, Complied With'),
        (2, 'Endorsements Required, Not Complied With'),
        (3, 'Endorsements Required, Compliance Unknown'),
        (7, 'No Driver Present/Unknown if Driver Present'),
        (8, "Not Reported "),
        (9, 'Unknown, if Required')
    ]
    cdl_endorsements = models.PositiveSmallIntegerField(choices=cdl_endorsements_choices, default=0, null=True, blank=True)
    #d10
    license_compliance_with_class_of_vehicle_choices = [
        (0, 'Not Licensed'),
        (1, 'No License Required for This Class Vehicle'),
        (2, 'No Valid License for This Class Vehicle'),
        (3, 'Valid License for This Class Vehicle'),
        (6, 'No Driver Present/Unknown if Driver Present'),
        (7, 'Not Reported '),
        (8, 'Unknown if CDL and/or CDL Endorsement Required for This Vehicle'),
        (9, 'Unknown')
    ]
    license_compliance_with_class_of_vehicle = models.PositiveSmallIntegerField(choices=license_compliance_with_class_of_vehicle_choices, default=9, null=True, blank=True)
    #d11
    compliance_with_license_restrictions_choices = [
        (0, "No Restrictions or Not Applicable"),
        (1, "Restrictions Complied With"),
        (2, "Restrictions Not Complied With"),
        (3, "Restrictions, Compliance Unknown"),
        (7, "No Driver Present/Unknown if Driver Present"),
        (8, "Not Reported"),
        (9, "Unknown")
    ]
    compliance_with_license_restrictions = models.PositiveSmallIntegerField(choices=compliance_with_license_restrictions_choices, default=9, null=True, blank=True)
    


    #d12 (inches)
    driver_height = models.PositiveSmallIntegerField(null=True, blank=True)
    #d13 (lbs)
    driver_weight = models.PositiveSmallIntegerField(null=True, blank=True)
    #d14
    previous_recorded_crashes = models.PositiveSmallIntegerField(null=True, blank=True)
    #d15
    previous_bac_suspensions_underage = models.PositiveSmallIntegerField(null=True, blank=True)
    previous_bac_suspensions = models.PositiveSmallIntegerField(null=True, blank=True)
    previous_other_suspensions = models.PositiveSmallIntegerField(null=True, blank=True)
    #d16
    previous_dwi_convictions = models.PositiveSmallIntegerField(null=True, blank=True)
    #d17
    previous_speeding_convictions = models.PositiveSmallIntegerField(null=True, blank=True)
    #d18
    previous_other_moving_violations = models.PositiveSmallIntegerField(null=True, blank=True)
    #d19a

    month_of_oldest_violation_choices = [
        (0, "No Record"),
        (1, "January"), 
        (2, "February"), 
        (3, "March"), 
        (4, "April"), 
        (5, "May"), 
        (6, "June"), 
        (7, "July"), 
        (8, "August"), 
        (9, "September"), 
        (10, "October"), 
        (11, "November"), 
        (12, "December"),
        (98, "No Driver Present/Unknown if Driver Present"),
        (99, "Unknown")
    ]
    month_of_oldest_violation = models.PositiveSmallIntegerField(choices=month_of_oldest_violation_choices, default=99, null=True, blank=True)
    #d19b
    year_of_oldest_violation = models.PositiveIntegerField(null=True, blank=True)
    #d20a
    month_of_newest_violation = models.PositiveSmallIntegerField(choices=month_of_oldest_violation_choices, default=99, null=True, blank=True)
    #d20b
    year_of_newest_violation = models.PositiveIntegerField(null=True, blank=True)
    #d22
    speeding_related_choices = [
        (0, "No"),
        (1, "Yes"),
        (2, "Yes, Racing"),
        (3, "Yes, Exceeded Speed Limit"),
        (4, "Yes, Too Fast for Conditions"),
        (5, "Yes, Specifics Unknown"),
        (8, "No Driver Present/Unknown if Driver Present"),
        (9, "Reported as Unknown")
    ]
    speeding_related = models.PositiveSmallIntegerField(choices=speeding_related_choices, default=9, null=True, blank=True)

    #pc5
    trafficway_description_choices = [
        (0, 'Non-Trafficway or Driveway Access'),
        (1, 'Two-Way, Not Divided'),
        (2, 'Two-Way, Divided, Unprotected Median'),
        (3, 'Two-Way, Divided, Positive Median Barrier'),
        (4, 'One-Way Trafficway'),
        (5, 'Two-Way, Not Divided With a Continuous Left Turn Lane'),
        (6, 'Entrance/Exit Ramp'),
        (7, 'Two-Way Divided, Unknown if Unprotected Median or Positive Median Barrier'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown'),
    ]
    trafficway_description = models.PositiveSmallIntegerField(choices=trafficway_description_choices, default=9)
    # pc6
    total_lanes_in_roadway_choices = [
        (0, 'Non-Trafficway or Driveway Access'),
        (1, 'One Lane'),
        (2, 'Two Lanes'),
        (3, 'Three Lanes'),
        (4, 'Four Lanes'),
        (5, 'Five Lanes'),
        (6, 'Six Lanes'),
        (7, 'Seven or More Lanes'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown'),
    ] 
    total_lanes_in_roadway = models.PositiveSmallIntegerField(choices=total_lanes_in_roadway_choices, default=9)
    #pc7
    speed_limit = models.PositiveSmallIntegerField(null=True, blank=True)
    #pc8
    roadway_alignment_choices = [
        (0, 'Non-Trafficway or Driveway Access'),
        (1, 'Straight'),
        (2, 'Curve Right'),
        (3, 'Curve Left'),
        (4, 'Curve - Unknown Direction'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown'),
    ]
    roadway_alignment = models.PositiveSmallIntegerField(choices=roadway_alignment_choices, default=9)
    #pc9
    roadway_grade_choices = [
        (0, 'Non-Trafficway or Driveway Access'),
        (1, 'Level'),
        (2, 'Grade, Unknown Slope'),
        (3, 'Hillcrest'),
        (4, 'Sag (Bottom)'),
        (5, 'Uphill'),
        (6, 'Downhill'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown')
    ]
    roadway_grade = models.PositiveSmallIntegerField(choices=roadway_grade_choices, default=9)
    #pc10
    roadway_surface_type_choices = [
        (0, 'Non-Trafficway or Driveway Access'),
        (1, 'Concrete'),
        (2, 'Blacktop, Bituminous, or Asphalt'),
        (3, 'Brick or Block'),
        (4, 'Slag, Gravel, or Stone'),
        (5, 'Dirt'),
        (7, 'Other'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown')
    ]
    roadway_surface_type = models.PositiveSmallIntegerField(choices=roadway_surface_type_choices, default=9)
    #pc11
    roadway_surface_condition_choices = [
        (0, 'Non-Trafficway Area or Driveway Access'),
        (1, 'Dry'),
        (2, 'Wet'),
        (3, 'Snow'),
        (4, 'Ice/Frost'),
        (5, 'Sand'),
        (6, 'Water (Standing or Moving)'),
        (7, 'Oil'),
        (8, 'Other'),
        (10, 'Slush'),
        (11, 'Mud, Dirt, Gravel'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown'),
    ]
    roadway_surface_condition = models.PositiveSmallIntegerField(choices=roadway_surface_condition_choices, default=98)
    #pc12
    traffic_control_device_choices = [
        (0, 'No Controls'),
        (1, 'Traffic Control Signal (on Colors) Without Pedestrian Signal'),
        (2, 'Traffic Control Signal (on Colors) With Pedestrian Signal'),
        (3, 'Traffic Control Signal (on Colors) Not Known if Pedestrian Signal'),
        (4, 'Flashing Traffic Control Signal'),
        (7, 'Lane Use Control Signal'),
        (8, 'Other Highway Traffic Signal'),
        (9, 'Unknown Highway Traffic Signal'),
        (20, 'Stop Sign'),
        (21, 'Yield Sign'),
        (28, 'Other Regulatory Sign'),
        (29, 'Unknown Regulatory Sign'),
        (23, 'School Zone Sign/Device'),
        (40, 'Warning Sign'),
        (50, 'Person'),
        (65, 'Railway Crossing Device'),
        (98, 'Other'),
        (97, 'Not Reported'),
        (99, 'Reported as Unknown'),
    ]
    traffic_control_device = models.PositiveSmallIntegerField(choices=traffic_control_device_choices, default=97)
    #pc13
    traffic_control_device_functioning_choices = [
        (0, 'No Controls'),
        (1, 'Device Not Functioning'),
        (2, 'Device Functioning - Functioning Improperly'),
        (3, 'Device Functioning Properly'),
        (4, 'Device Not Functioning or Device Functioning Improperly, Specifics Unknown'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown'),
    ]
    traffic_control_device_functioning = models.PositiveSmallIntegerField(choices=traffic_control_device_functioning_choices, default=8)
    # PC17
    pre_event_movement_choices = [
        (0, 'No Driver Present/Unknown if Driver Present'),	
        (1, 'Going Straight'),	
        (2, 'Decelerating in Road'),
        (3, 'Accelerating in Road'),	
        (4, 'Starting in Road'),
        (5, 'Stopped in Roadway'),
        (6, 'Passing or Overtaking Another Vehicle'),
        (7, 'Disabled or "Parked" in Travel Lane'),
        (8, 'Leaving a Parking Position'),
        (9, 'Entering a Parking Position'),
        (10, 'Turning Right'),
        (11, 'Turning Left'),
        (12, 'Making a U-Turn'),
        (13, 'Backing up (Other Than for Parking Position)'),
        (14, 'Negotiating a Curve'),	
        (15, 'Changing Lanes'),	
        (16, 'Merging'),	
        (17, 'Successful Avoidance Maneuver to a Previous Critical Event'),	
        (98, 'Other'),	
        (99, 'Unknown')
    ]
    pre_event_movement = models.PositiveSmallIntegerField(choices=pre_event_movement_choices, default=99)
    # PC19
    critical_precrash_event_choices = [
        (1, 'THIS VEHICLE LOSS OF CONTROL DUE TO: Blow Out/Flat Tire'),
        (2, 'THIS VEHICLE LOSS OF CONTROL DUE TO: Stalled Engine'),
        (3, 'THIS VEHICLE LOSS OF CONTROL DUE TO: Disabling Vehicle Failure (e.g., Wheel Fell off)'),
        (4, 'THIS VEHICLE LOSS OF CONTROL DUE TO: Non-Disabling Vehicle Problem (e.g., Hood Flew up)'),
        (5, 'THIS VEHICLE LOSS OF CONTROL DUE TO: Poor Road Conditions (Puddle, Pothole, Ice, etc.)'),
        (6, 'THIS VEHICLE LOSS OF CONTROL DUE TO: Traveling Too Fast for Conditions'),
        (8, 'THIS VEHICLE LOSS OF CONTROL DUE TO: Other Cause of Control Loss'),
        (9, 'THIS VEHICLE LOSS OF CONTROL DUE TO: Unknown Cause of Control Loss'),
        (10, 'THIS VEHICLE TRAVELING Over the Lane Line on Left Side of Travel Lane'),
        (11, 'THIS VEHICLE TRAVELING Over the Lane Line on Right Side of Travel Lane'),
        (12, 'THIS VEHICLE TRAVELING Off the Edge of the Road on the Left Side'),
        (13, 'THIS VEHICLE TRAVELING Off the Edge of the Road on the Right Side'),
        (14, 'THIS VEHICLE TRAVELING End Departure'),
        (15, 'THIS VEHICLE TRAVELING Turning Left'),
        (16, 'THIS VEHICLE TRAVELING Turning Right'),
        (17, 'THIS VEHICLE TRAVELING Crossing Over (Passing Through) Intersection'),
        (18, 'THIS VEHICLE TRAVELING This Vehicle Decelerating'),
        (19, 'THIS VEHICLE TRAVELING Unknown Travel Direction'),
        (20, 'THIS VEHICLE TRAVELING Backing'),
        (21, 'THIS VEHICLE TRAVELING Making a U-Turn'),
        (50, 'OTHER MOTOR VEHICLE IN LANE Other Vehicle Stopped'),
        (51, 'OTHER MOTOR VEHICLE IN LANE Traveling in Same Direction With Lower Steady Speed'),
        (52, 'OTHER MOTOR VEHICLE IN LANE Traveling in Same Direction While Decelerating'),
        (53, 'OTHER MOTOR VEHICLE IN LANE Traveling in Same Direction With Higher Speed'),
        (54, 'OTHER MOTOR VEHICLE IN LANE Traveling in Opposite Direction'),
        (55, 'OTHER MOTOR VEHICLE IN LANE In Crossover'),
        (56, 'OTHER MOTOR VEHICLE IN LANE Backing'),
        (59, 'OTHER MOTOR VEHICLE IN LANE Unknown Travel Direction of the Other Motor Vehicle in Lane'),
        (60, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Adjacent Lane (Same Direction) Over Left Lane Line'),
        (61, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Adjacent Lane (Same Direction) Over Right Lane Line'),
        (62, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Opposite Direction Over Left Lane Line'),
        (63, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Opposite Direction Over Right Lane Line'),
        (64, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Parking Lane/Shoulder, Median/Crossover, Roadside'),
        (65, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Crossing Street, Turning Into Same Direction'),
        (66, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Crossing Street, Across Path'),
        (67, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Crossing Street, Turning Into Opposite Direction'),
        (68, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Crossing Street, Intended Path Not Known'),
        (70, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Driveway, Turning Into Same Direction'),
        (71, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Driveway, Across Path'),
        (72, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Driveway, Turning Into Opposite Direction'),
        (73, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Driveway, Intended Path Not Known'),
        (74, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE From Entrance to Limited Access Highway'),
        (78, 'OTHER MOTOR VEHICLE ENCROACHING INTO LANE Encroachment by Other Vehicle - Details Unknown'),
        (80, 'PEDESTRIAN OR PEDALCYCLIST OR OTHER NON-MOTORIST Pedestrian in Road'),
        (81, 'PEDESTRIAN OR PEDALCYCLIST OR OTHER NON-MOTORIST Pedestrian Approaching Road'),
        (82, 'PEDESTRIAN OR PEDALCYCLIST OR OTHER NON-MOTORIST Pedestrian Unknown Location'),
        (83, 'PEDESTRIAN OR PEDALCYCLIST OR OTHER NON-MOTORIST Pedalcyclist/Other Non-Motorist in Road'),
        (84, 'PEDESTRIAN OR PEDALCYCLIST OR OTHER NON-MOTORIST Pedalcyclist/Other Non-Motorist Approaching Road'),
        (85, 'PEDESTRIAN OR PEDALCYCLIST OR OTHER NON-MOTORIST Pedalcyclist/Other Non-Motorist Unknown Location'),
        (87, 'OBJECT OR ANIMAL Animal in Road'),
        (88, 'OBJECT OR ANIMAL Animal Approaching Road'),
        (89, 'OBJECT OR ANIMAL Animal - Unknown Location'),
        (90, 'OBJECT OR ANIMAL Object in Road'),
        (91, 'OBJECT OR ANIMAL Object Approaching Road'),
        (92, 'OBJECT OR ANIMAL Object Unknown Location'),
        (98, 'OTHER Other Critical Precrash Event'),
        (99, 'OTHER Unknown'),
    ]
    critical_precrash_event = models.PositiveSmallIntegerField(choices=critical_precrash_event_choices, default=99)
    #pc20
    attempted_avoidance_maneuver_choices = [
        (0, 'No Driver Present/Unknown if Driver Present'),
        (1, 'No Avoidance Maneuver'),
        (5, 'Releasing Brakes'),
        (6, 'Steering Left'),
        (7, 'Steering Right'),
        (8, 'Braking and Steering Left'),
        (9, 'Braking and Steering Right'),
        (10, 'Accelerating'),
        (11, 'Accelerating and Steering Left'),
        (12, 'Accelerating and Steering Right'),
        (15, 'Braking and Unknown Steering Direction'),
        (16, 'Braking'),
        (98, 'Other Actions'),
        (99, 'Unknown/Not Reported'),
    ]
    attempted_avoidance_maneuver = models.PositiveSmallIntegerField(choices=attempted_avoidance_maneuver_choices, default=99 )
    #pc21
    precrash_stability_choices = [
        (0, 'No Driver Present/Unknown if Driver Present'),
        (1, 'Tracking'),
        (2, 'Skidding Longitudinally - Rotation Less Than 30 Degrees'),
        (3, 'Skidding Laterally - Clockwise Rotation'),
        (4, 'Skidding Laterally - Counterclockwise Rotation'),
        (5, 'Skidding Laterally - Rotation Direction Unknown'),
        (7, 'Other Vehicle Loss-of-Control'),
        (9, 'Precrash Stability Unknown'),
    ]
    precrash_stability = models.PositiveSmallIntegerField(choices=precrash_stability_choices, default=9)
    #pc22
    preimpact_location_choices = [
        (0, 'No Driver Present/Unknown if Driver Present'),
        (1, 'Stayed in Original Travel Lane'),
        (2, 'Stayed on Roadway, but Left Original Travel Lane'),
        (3, 'Stayed on Roadway, Not Known if Left Original Travel Lane'),
        (4, 'Departed Roadway'),
        (5, 'Remained off Roadway'),
        (6, 'Returned to Roadway'),
        (7, 'Entered Roadway'),
        (9, 'Unknown'),
    ]
    preimpact_location = models.PositiveSmallIntegerField(choices=preimpact_location_choices, default=9)
    #pc23
    crash_type_choices = [
        (0, 'No Impact'),
        (1, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION A: RIGHT ROADSIDE DEPARTURE - Drive off Road'),
        (2, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION A: RIGHT ROADSIDE DEPARTURE - Control/Traction Loss'),
        (3, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION A: RIGHT ROADSIDE DEPARTURE - Avoid Collision With Vehicle, Pedestrian, Animal'),
        (4, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION A: RIGHT ROADSIDE DEPARTURE - Specifics Other'),
        (5, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION A: RIGHT ROADSIDE DEPARTURE - Specifics Unknown'),
        (6, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION B: LEFT ROADSIDE DEPARTURE - Drive off Road'),
        (7, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION B: LEFT ROADSIDE DEPARTURE - Control/Traction Loss'),
        (8, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION B: LEFT ROADSIDE DEPARTURE - Avoid Collision With Vehicle, Pedestrian, Animal'),
        (9, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION B: LEFT ROADSIDE DEPARTURE - Specifics Other'),
        (10, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION B: LEFT ROADSIDE DEPARTURE - Specifics Unknown'),
        (11, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION C: FORWARD IMPACT - Parked Vehicle'),
        (12, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION C: FORWARD IMPACT - Stationary Object'),
        (13, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION C: FORWARD IMPACT - Pedestrian/Animal'),
        (14, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION C: FORWARD IMPACT - End Departure'),
        (15, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION C: FORWARD IMPACT - Specifics Other'),
        (16, 'CATEGORY I: SINGLE DRIVER - CONFIGURATION C: FORWARD IMPACT - Specifics Unknown'),
        (20, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Stopped'),
        (21, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Stopped, Straight'),
        (22, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Stopped, Left'),
        (23, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Stopped, Right'),
        (24, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Slower'),
        (25, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Slower, Going Straight'),
        (26, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Slower, Going Left'),
        (27, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Slower, Going Right'),
        (28, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Decelerating (Slowing)'),
        (29, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Decelerating (Slowing), Going Straight'),
        (30, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Decelerating (Slowing), Going Left'),
        (31, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Decelerating (Slowing), Going Right'),
        (32, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Specifics Other'),
        (33, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION D: REAR END - Specifics Unknown'),
        (34, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Control/Traction Loss, Avoiding Non-Contact Vehicle- Vehicle’s Frontal Area Impacts Another Vehicle'),
        (35, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Control/Traction Loss, Avoiding Non-Contact Vehicle- Vehicle Is Impacted by Frontal Area of Another Vehicle'),
        (36, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Control/Traction Loss, Avoiding Non-Fixed Object- Vehicle’s Frontal Area Impacts Another Vehicle'),
        (37, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Control/Traction Loss, Avoiding Non-Fixed Object- Vehicle Is Impacted by Frontal Area of Another Vehicle'),
        (38, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Avoiding Non-Contact Vehicle- Vehicle’s Frontal Area Impacts Another Vehicle'),
        (39, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Avoiding Non-Contact Vehicle- Vehicle Is Impacted by Frontal Area of Another Vehicle'),
        (40, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Avoiding Non-Fixed Object- Vehicle’s Frontal Area Impacts Another Vehicle'),
        (41, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Avoiding Non-Fixed Object- Vehicle Is Impacted by Frontal Area of Another Vehicle'),
        (42, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Specifics Other'),
        (43, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION E: FORWARD IMPACT - Specifics Unknown'),
        (44, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION F: SIDESWIPE/ANGLE - Straight Ahead on Left'),
        (45, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION F: SIDESWIPE/ANGLE - Straight Ahead on Left/Right'),
        (46, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION F: SIDESWIPE/ANGLE - Changing Lanes to the Right'),
        (47, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION F: SIDESWIPE/ANGLE - Changing Lanes to the Left'),
        (48, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION F: SIDESWIPE/ANGLE - Specifics Other'),
        (49, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - CONFIGURATION F: SIDESWIPE/ANGLE - Specifics Unknown'),
        # (50, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION G: HEAD-ON - Lateral Move (Left/Right)'),
        # (51, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION G: HEAD-ON - Lateral Move (Going Straight)'),
        (52, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION G: HEAD-ON - Specifics Other'),
        (53, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION G: HEAD-ON - Specifics Unknown'),
        (54, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Control/Traction Loss, Avoiding Non-Contact Vehicle- Vehicle’s Frontal Area Impacts Another Vehicle'),
        (55, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Control/Traction Loss, Avoiding Non-Contact Vehicle- Vehicle Is Impacted by Frontal Area of Another Vehicle'),
        (56, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Control/Traction Loss, Avoiding Non-Fixed Object- Vehicle’s Frontal Area Impacts Another Vehicle'),
        (57, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Control/Traction Loss, Avoiding Non-Fixed Object- Vehicle Is Impacted by Frontal Area of Another Vehicle'),
        (58, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Avoiding Non-Contact Vehicle- Vehicle’s Frontal Area Impacts Another Vehicle'),
        (59, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Avoiding Non-Contact Vehicle- Vehicle Is Impacted by Frontal Area of Another Vehicle'),
        (60, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Avoiding Non-Fixed Object- Vehicle’s Frontal Area Impacts Another Vehicle'),
        (61, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Avoiding Non-Fixed Object- Vehicle Is Impacted by Frontal Area of Another Vehicle'),
        (62, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Specifics Other'),
        (63, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION H: FORWARD IMPACT - Specifics Unknown'),
        (64, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION I: SIDESWIPE/ANGLE - Lateral Move (Left/Right)'),
        (65, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION I: SIDESWIPE/ANGLE - Lateral Move (Going Straight)'),
        (66, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION I: SIDESWIPE/ANGLE - Specifics Other'),
        (67, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - CONFIGURATION I: SIDESWIPE/ANGLE - Specifics Unknown'),
        # (68, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION J: TURN ACROSS PATH - Initial Opposite Directions (Left/Right)'),
        # (69, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION J: TURN ACROSS PATH - Initial Opposite Directions (Going Straight)'),
        # (70, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION J: TURN ACROSS PATH - Initial Same Directions (Turning Right)'),
        # (71, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION J: TURN ACROSS PATH - Initial Same Directions (Going Straight)'),
        # (72, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION J: TURN ACROSS PATH - Initial Same Directions (Turning Left)'),
        # (73, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION J: TURN ACROSS PATH - Initial Same Directions (Going Straight)'),
        (74, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION J: TURN ACROSS PATH - Specifics Other'),
        (75, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION J: TURN ACROSS PATH - Specifics Unknown'),
        # (76, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Turn Into Same Direction (Turning Left)'),
        # (77, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Turn Into Same Direction (Going Straight)'),
        # (78, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Turn Into Same Direction (Turning Right)'),
        # (79, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Turn Into Same Direction (Going Straight)'),
        # (80, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Turn Into Opposite Directions (Turning Right)'),
        # (81, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Turn Into Opposite Directions (Going Straight)'),
        # (82, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Turn Into Opposite Directions (Turning Left)'),
        # (83, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Turn Into Opposite Directions (Going Straight)'),
        (84, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Specifics Other'),
        (85, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - CONFIGURATION K: TURN INTO PATH - Specifics Unknown'),
        # (86, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - CONFIGURATION L: STRAIGHT PATHS - Striking From the Right'),
        # (87, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - CONFIGURATION L: STRAIGHT PATHS - Struck on the Right'),
        # (88, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - CONFIGURATION L: STRAIGHT PATHS - Striking From the Left'),
        # (89, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - CONFIGURATION L: STRAIGHT PATHS - Struck on the Left'),
        (90, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - CONFIGURATION L: STRAIGHT PATHS - Specifics Other'),
        (91, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - CONFIGURATION L: STRAIGHT PATHS - Specifics Unknown'),
        # (92, 'CATEGORY VI: MISCELLANEOUS - CONFIGURATION M: BACKING, ETC. - Backing Vehicle'),
        # (93, 'CATEGORY VI: MISCELLANEOUS - CONFIGURATION M: BACKING, ETC. - Other Vehicle or Object (2010-2012)'),
        # (93, 'CATEGORY VI: MISCELLANEOUS - CONFIGURATION M: BACKING, ETC. - Other Vehicle (2013-Later)'),
        # (98, 'CATEGORY VI: MISCELLANEOUS - CONFIGURATION M: BACKING, ETC. - Other Crash Type'),
        # (99, 'CATEGORY VI: MISCELLANEOUS - CONFIGURATION M: BACKING, ETC. - Unknown Crash Type'),
        (101, 'CATEGORY I: SINGLE DRIVER - Right Roadside Departure'),
        (102, 'CATEGORY I: SINGLE DRIVER - Left Roadside Departure'),
        (103, 'CATEGORY I: SINGLE DRIVER - Struck Object While Moving Forward'),
        (201, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - Rear End, Leading Vehicle'),
        (202, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - Rear End, Trailing Vehicle'),
        (203, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - Rear End, Other or Unknown'),
        (204, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - Forward Impact, Frontal Impact After Maneuver'),
        (205, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - Forward Impact, Rear End Impact After Maneuver'),
        (206, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - Forward Impact, Other or Unknown'),
        (207, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - Sideswipe Angle, Vehicle on Left'),
        (208, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - Sideswipe Angle, Vehicle on Right'),
        (209, 'CATEGORY II: SAME TRAFFICWAY, SAME DIRECTION - (Sideswipe Angle, Other or Unknown'),
        (301, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - Lateral Move [Left/Right], Head-On, Sideswipe, or Angle'),
        (302, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - Lateral Move [Going Straight], Head-On, Sideswipe, or Angle'),
        (303, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - Lateral Move, Other or Unknown'),
        (304, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - Frontal Impact After Maneuver, Departed Lane'),
        (305, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - Frontal Impact After Maneuver, Remained in Lane'),
        (306, 'CATEGORY III: SAME TRAFFICWAY, OPPOSITE DIRECTION - Frontal Impact After Maneuver, Other or Unknown'),
        (401, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Across Path, Initial Opposite Directions [Left/Right]'),
        (402, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Across Path, Initial Opposite Directions [Going Straight]'),
        (403, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Across Path, Initial Same Directions [Turning Right]'),
        (404, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Across Path, Initial Same Directions [Going Straight]'),
        (405, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Across Path, Initial Same Directions [Turning Left]'),
        (406, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Across Path, Initial Same Directions [Going Straight]'),
        (407, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Across Path, Other or Unknown'),
        (408, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Turn into Same Direction [Turning Left]'),
        (409, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Turn into Same Direction [Going Straight]'),
        (410, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Turn into Same Direction [Turning Right]'),
        (411, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Turn into Same Direction [Going Straight]'),
        (412, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Turn into Opposite Directions [Turning Right]'),
        (413, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Turn into Opposite Directions [Going Straight]'),
        (414, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Turn into Opposite Directions [Turning Left]'),
        (415, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Turn into Opposite Directions [Going Straight]'),
        (416, 'CATEGORY IV: CHANGING TRAFFICWAY, VEHICLE TURNING - Turn Into Path, Other or Unknown'),
        (501, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - Straight Paths, Striking from the Right'),
        (502, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - Straight Paths, Struck on the Right'),
        (503, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - Straight Paths, Striking from the Left'),
        (504, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - Straight Paths, Struck on the Left'),
        (505, 'CATEGORY V: INTERSECTING PATHS (VEHICLE DAMAGE) - Straight Paths, Other or Unknown'),
        (992, 'CATEGORY VI: MISCELLANEOUS - Backing Vehicle'),
        (993, 'CATEGORY VI: MISCELLANEOUS - Other Vehicle'),
        (998, 'CATEGORY VI: MISCELLANEOUS - Other Crash Type'),
        (999, 'CATEGORY VI: MISCELLANEOUS - Unknown Crash Type'),

    ]
    crash_type = models.PositiveSmallIntegerField(choices = crash_type_choices, default=99)

    class Meta:
        unique_together = [["accident", "vehicle_number"]]
        db_table = "vehicle"
        managed = True

# A class for parked cars involved with a given fatal crash
    
class ParkedVehicle(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    accident = models.ForeignKey(Accident, on_delete=models.CASCADE)
    vehicle_number = models.PositiveSmallIntegerField(null=False)
    #c4a #PVE_FORMS
    # number_of_vehicles_in_transit = models.PositiveSmallIntegerField(default=0)
    #c19 PHARM_EV
    first_harmful_event_choices = [
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
    first_harmful_event = models.PositiveSmallIntegerField(choices=first_harmful_event_choices, default=99)
    # c20 PMAN_COLL
    manner_of_collision_of_first_harmful_event_choices = [
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
    manner_of_collision_of_first_harmful_event = models.PositiveSmallIntegerField(choices=manner_of_collision_of_first_harmful_event_choices, default=99)
    #v4 PNUMOCCS
    number_of_occupants = models.PositiveSmallIntegerField(null=True, blank=True)
    #v5 PTYPE
    unit_type_choices = [
        (2, "Motor Vehicle Not In-Transport Within the Trafficway"),
        (3, "Motor Vehicle Not In-Transport Outside the Trafficway"),
        (4, "Working Motor Vehicle (Highway Construction, Maintenance, Utility Only)")
    ]
    unit_type = models.PositiveSmallIntegerField(choices=unit_type_choices, default=3)
    # v6 PHIT_RUN
    hit_and_run_choices = [
        (0, "No Hit and Run"),
        (1, "Hit and Run"),
        (9, "Unknown")
    ]
    hit_and_run = models.PositiveSmallIntegerField(choices=hit_and_run_choices, default=9) 
    
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
    vpic_make = models.PositiveIntegerField(null=True, blank=True)
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
        (62, 'Incomplete - Cutaway'),
        (63, 'Incomplete - Chassis Cab (Single Cab)'),
        (64, 'Incomplete - Glider'),
        (65, 'Incomplete'),
        (66, 'Truck-Tractor'),
        (67, 'Incomplete - Stripped Chassis'),
        (68, 'Streetcar/Trolley'),
        (69, 'Off-Road Vehicle - All Terrain Vehicle (ATV) (Motorcycle-Style)'),
        (70, 'Incomplete - Chassis Cab (Double Cab)'),
        (71, 'Incomplete - School Bus Chassis'),
        (72, 'Incomplete - Commercial Bus Chassis'),
        (73, 'Bus - School Bus'),
        (74, 'Incomplete - Chassis Cab (Number of Cab Unknown)'),
        (75, 'Incomplete - Transit Bus Chassis'),
        (76, 'Incomplete - Motor Coach Chassis'),
        (77, 'Incomplete - Shuttle Bus Chassis'),
        (78, 'Incomplete - Motor Home Chassis'),
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
        (107, 'Incomplete - Bus Chassis'),
        (108, 'Motorhome'),
        (109, 'Motorcycle - Cross Country'),
        (110, 'Motorcycle - Underbone'),
        (111, 'Step Van/Walk-in Van'),
        (112, 'Incomplete - Commercial Chassis'),
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
    gross_vehicle_weight_rating_lower = models.PositiveSmallIntegerField(choices = weight_rating_choices, default = 98)
    gross_vehicle_weight_rating_upper = models.PositiveSmallIntegerField(choices = weight_rating_choices, default = 98)
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
    vehicle_trailing = models.PositiveSmallIntegerField(choices=vehicle_trailing_choices, default=9)
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
    trailer_weight_rating_1 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=98)
    trailer_weight_rating_2 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=98)
    trailer_weight_rating_3 = models.PositiveSmallIntegerField(choices=trailer_weight_rating_choices, default=98)
    
    #V23
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
    hazardous_material_placard = models.PositiveSmallIntegerField(choices=placard_choices, default=8)
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
    hazardous_material_class_number = models.PositiveSmallIntegerField(choices=hazardous_material_class_number_choices, default=88)
    # v26E HAZ_REL
    release_of_hazardous_material_choices = [
        (0, "Not Applicable"),
        (1, "No"),
        (2, "Yes"),
        (8, "Not Reported")
    ]
    release_of_hazardous_material = models.PositiveSmallIntegerField(choices=release_of_hazardous_material_choices, default=8)
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
    bus_use = models.PositiveSmallIntegerField(choices=bus_use_choices, default=98)
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
    special_vehicle_use = models.PositiveSmallIntegerField(choices=special_vehicle_use_choices, default=99)
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
    emergency_vehicle_use = models.PositiveSmallIntegerField(choices=emergency_vehicle_use_choices, default=8)
    #v31
    underride_override_choices = [
        (0, "No Underride or Override"),
        (1, "Underride"),
        (2, "Override"),
        (7, "Not Applicable"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    underride_override = models.PositiveSmallIntegerField(choices=underride_override_choices, default=8)
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
        (15, "Underride"),
        (16, "Override"),
        (18, "Cargo/Vehicle Parts Set-in-Motion"),
        (19, "Other Objects or Person Set-in-Motion"),
        (20, "Object Set in Motion, Unknown if Cargo/Vehicle Parts or Other"),
        (61, "Left"),
        (62, "Left-Front Side"),
        (63, "Left-Back Side"),
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
    #v150
    fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    # V100
    combined_make_model_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = [["accident", "vehicle_number"]]
        db_table = "parked_vehicle"
        managed = True



class Person(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    def __nonmotorists__(self):
        return self.filter(vehicle__vehicle_number__isnull=True)
    
    accident = models.ForeignKey(Accident, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.CASCADE)
    parked_vehicle = models.ForeignKey(ParkedVehicle, null=True, blank=True, on_delete=models.CASCADE)
    person_number = models.PositiveSmallIntegerField(null=False)
    # id = models.PositiveBigIntegerField(primary_key = True)
    
    #p5
    age = models.PositiveSmallIntegerField(null = True)
    #p6 
    sex_choices = [
        (1, "Male"),
        (2, "Female"),
        (3, "Other"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    sex = models.PositiveSmallIntegerField(choices=sex_choices, default=8)
    #p7 PER_TYP
    person_type_choices = [
        (1, 'Driver of a Motor Vehicle In-Transport'),
        (2, 'Passenger of a Motor Vehicle In-Transport'),
        (3, 'Occupant of a Motor Vehicle Not In-Transport'),
        (4, 'Occupant of a Non-Motor Vehicle Transport Device'),
        (5, 'Pedestrian'),
        (6, 'Bicyclist'),
        (7, 'Other Pedalcyclist'),
        (8, 'Person on Personal Conveyance'),
        (9, 'Unknown Occupant Type in a Motor Vehicle In Transport'),
        (10, 'Person In/On a Building'),
        (19, 'Unknown Type of Non-Motorist'),
    ]
    person_type = models.PositiveSmallIntegerField(choices=person_type_choices, default=9)
    #p8 injury_severity
    injury_severity_choices = [
        (0, 'No Apparent Injury (O)'),
        (1, 'Possible Injury (C)'),
        (2, 'Suspected Minor Injury (B)'),
        (3, 'Suspected Serious Injury (A)'),
        (4, 'Fatal Injury (K)'),
        (5, 'Injured, Severity Unknown (U) (Since 1978)'),
        (6, 'Died Prior to Crash'),
        (9, 'Unknown/Not Reported')
    ]
    injury_severity = models.PositiveSmallIntegerField(choices=injury_severity_choices, default=9)

    #p9 seating position
    seating_position_choices = [
        (0, 'Not a Motor Vehicle Occupant (2005-Later)'),
        (11, "Front Seat, Left Side (Driver's Side)"),
        (12, 'Front Seat, Middle'),
        (13, 'Front Seat, Right Side'),
        (18, 'Front Seat, Other'),
        (19, 'Front Seat, Unknown'),
        (21, 'Second Seat, Left Side'),
        (22, 'Second Seat, Middle'),
        (23, 'Second Seat, Right Side'),
        (28, 'Second Seat, Other'),
        (29, 'Second Seat, Unknown'),
        (31, 'Third Seat, Left Side'),
        (32, 'Third Seat, Middle'),
        (33, 'Third Seat, Right Side'),
        (38, 'Third Seat, Other'),
        (39, 'Third Seat, Unknown'),
        (41, 'Fourth Seat, Left Side'),
        (42, 'Fourth Seat, Middle'),
        (43, 'Fourth Seat, Right Side'),
        (48, 'Fourth Seat, Other'),
        (49, 'Fourth Seat, Unknown'),
        (50, 'Sleeper Section of Cab (Truck)'),
        (51, 'Other Passenger in Enclosed Passenger or Cargo Area (Since 2009)'),
        (52, 'Other Passenger in Unenclosed Passenger or Cargo Area'),
        (53, 'Other Passenger in Passenger or Cargo Area, Unknown Whether or Not Enclosed'),
        (54, 'Trailing Unit'),
        (55, 'Riding on Vehicle Exterior'),
        (56, 'Appended to a Motor Vehicle for Motion'),
        (98, 'Not Reported'),
        (99, 'Unknown/Reported as Unknown (Since 2018)'),
    ]
    seating_position = models.PositiveSmallIntegerField(choices=seating_position_choices, default=98)
    #P10A restraint system use
    restraint_system_use_choices = [
        (0, 'None Used/Not Applicable'),
        (1, 'Shoulder Belt Only Used'),
        (2, 'Lap Belt Only Used'),
        (3, 'Shoulder and Lap Belt Used'),
        (4, 'Child Restraint - Type Unknown'),
        (6, 'Racing-Style Harness Used'),
        (8, 'Restraint Used - Type Unknown'),
        (10, 'Child Restraint System - Forward Facing (Since 2008)'),
        (11, 'Child Restraint System - Rear Facing (Since 2008)'),
        (12, 'Booster Seat'),
        (20, 'None Used/Not Applicable'),
        (96, 'Not a Motor Vehicle Occupant'),
        (97, 'Other'),
        (98, 'Not Reported'),
        (99, 'Unknown/Reported as Unknown (Since 2018)'),
    ]
    restraint_system_use = models.PositiveSmallIntegerField(choices=restraint_system_use_choices, default=98)
    #P10B restraint system misuse
    restraint_system_misuse_choices = [
        (0, "No Indication of Misuse"),
        (1, "Yes, Indication of Misuse"),
        (7, "None Used/Not Applicable"),
        (8, "Not a Motor Vehicle Occupant")
    ]
    restraint_system_misuse = models.PositiveSmallIntegerField(choices=restraint_system_misuse_choices, default=7)
    
    # P11A Helmet Use 
    helmet_use_choices = [
        (5, 'DOT-Compliant Motorcycle Helmet'),
        (16, 'Helmet, Other than DOT-Compliant Motorcycle Helmet'),
        (17, 'No Helmet'),
        (19, 'Helmet, Unknown if DOT-Compliant'),
        (20, 'Not Applicable'),
        (96, 'Not a Motor Vehicle Occupant'),
        (98, 'Not Reported'),
        (99, 'Unknown/Reported as Unknown if Helmet Worn'),
    ]
    helmet_use = models.PositiveSmallIntegerField(choices=helmet_use_choices, default=98)
    #p11b
    helmet_misuse = models.PositiveSmallIntegerField(choices=restraint_system_misuse_choices, default=7)

    # p12
    airbag_deployed_choices = [
        (0, "Nonmotorist"),
        (1, 'Deployed - Front'),
        (2, 'Deployed - Side (Door, Seat Back)'),
        (3, 'Deployed - Curtain (Roof)'),
        (7, 'Deployed - Other (Knee, Air Belt, etc.)'),
        (8, 'Deployed - Combination'),
        (9, 'Deployment - Unknown Location'),
        (20, 'Not Deployed'),
        (97, 'Not a Motor Vehicle Occupant'),
        (98, 'Not Reported'),
        (99, 'Reported as Deployment Unknown'),
    ]
    airbag_deployed = models.PositiveSmallIntegerField(choices=airbag_deployed_choices, default=98)
    # p13
    ejection_choices = [
        (0, "Not Ejected"),
        (1, "Totally Ejected"),
        (2, "Partially Ejected"),
        (3, "Ejected - Unknown Degree (Since 2008)"),
        (7, "Not Reported"),
        (8, "Not Applicable"),
        (9, "Reported as Unknown if Ejected")
    ]
    ejection = models.PositiveSmallIntegerField(choices=ejection_choices, default=8)
    # p14 ejectionpath
    ejection_path_choices = [
        (0, 'Ejection Path Not Applicable'),
        (1, 'Through Side Door Opening'),
        (2, 'Through Side Window'),
        (3, 'Through Windshield'),
        (4, 'Through Back Window'),
        (5, 'Through Back Door/Tailgate Opening'),
        (6, 'Through Roof Opening (Sun Roof, Convertible Top Down)'),
        (7, 'Through Roof (Convertible Top Up)'),
        (8, 'Other Path (e.g., Back of Pickup Truck)'),
        (9, 'Ejection Path Unknown'),
    ]
    ejection_path = models.PositiveSmallIntegerField(choices=ejection_path_choices, default=0)
    #p15
    extrication_choices = [
        (0, "Not Extricated/Not Applicable"),
        (1, "Extricated"),
        (9, "Unknown")
    ]
    extrication = models.PositiveSmallIntegerField(choices=extrication_choices, default=9)
    #p16
    police_reported_alcohol_involvement_choices = [
        (0, "No (Alcohol Not Involved)"),
        (1, "Yes (Alcohol Involved)"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    police_reported_alcohol_involvement = models.PositiveSmallIntegerField(choices=police_reported_alcohol_involvement_choices, default=8)
    
    #p17A
    alcohol_test_given_choices = [
        (0, "Test Not Given"),
        (2, "Test Given"),
        (8, "Not Reported"),
        (9, "Reported as Unknown if Tested ")
    ]
    alcohol_test_given = models.PositiveSmallIntegerField(choices=alcohol_test_given_choices, default=8)
    #p17B
    alcohol_test_type_choices = [
        (0, 'Not Tested for Alcohol'),
        (1, 'Blood Test'),
        (2, 'Breath Test (AC)'),
        (3, 'Urine'),
        (4, 'Vitreous'),
        (5, 'Blood Plasma/Serum'),
        (6, 'Blood Clot'),
        (7, 'Liver'),
        (8, 'Other Test Type'),
        (10, 'Preliminary Breath Test (PBT)'),
        (11, 'Breath Test, Unknown Type'),
        (95, 'Not Reported'),
        (98, 'Unknown Test Type (Since 2009)'),
        (99, 'Reported as Unknown if Tested')
    ]
    alcohol_test_type = models.PositiveSmallIntegerField(choices=alcohol_test_type_choices, default=95)
    #p17C
    alcohol_test_result = models.PositiveSmallIntegerField(null=True, blank=True)

    def interpret_alcohol_test_result(self):
        result = self.alcohol_test_result
        if result <= 940:
            return result / 1000
        else:
            if result in {995}:
                return "Not Reported"
            if result in {996}:
                return "None Given"
            if result in {997}:
                return "AC Test Performed, Results Unknown"
            if result in {998}:
                return "Positive Reading With No Actual Value"
            if result in {999}:
                return "Reported as Unknown if Tested"

            
                
    #p18
    police_reported_drug_involvement_choices = [
        (0, "No (Drugs Not Involved)"),
        (1, "Yes (Drugs Involved)"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    police_reported_drug_involvement = models.PositiveSmallIntegerField(choices=police_reported_drug_involvement_choices, default=8)
    #p19A
    drug_tested_choices = [
        (0, "Test Not Given"),
        (2, "Test Given"),
        (8, "Not Reported"),
        (9, "Reported as Unknown if Tested")
    ]
    drug_tested = models.PositiveSmallIntegerField(choices=drug_tested_choices, default=8)
    
    #p20
    transported_to_medical_facility_by_choices = [
        (0, 'Not Transported for Treatment'),
        (1, 'EMS Air'),
        (2, 'Law Enforcement'),
        (3, 'EMS Unknown Mode'),
        (4, 'Transported Unknown Source'),
        (5, 'EMS Ground'),
        (6, 'Other'),
        (8, 'Not Reported'),
        (9, 'Reported as Unknown')
    ]
    transported_to_medical_facility_by = models.PositiveSmallIntegerField(choices=transported_to_medical_facility_by_choices, default=8)
    #p21
    died_en_route_choices = [
        (0, "Not Applicable"),
        (7, "Died at Scene"),
        (8, "Died En Route"),
        (9, "Unknown")
    ]
    died_en_route = models.PositiveSmallIntegerField(choices=died_en_route_choices, default=0)
    #p22a
    month_of_death_choices = [
        (1, "January"), 
        (2, "February"), 
        (3, "March"), 
        (4, "April"), 
        (5, "May"), 
        (6, "June"), 
        (7, "July"), 
        (8, "August"), 
        (9, "September"), 
        (10, "October"), 
        (11, "November"), 
        (12, "December"), 
        (88, "Not Applicable (Non-Fatal)"),
        (97, "Redacted"),
        (99, "Unknown")
    ]
    month_of_death = models.PositiveSmallIntegerField(choices=month_of_death_choices)
    #p22b
    day_of_death = models.PositiveSmallIntegerField(null=True, blank=True)
    #p22c
    year_of_death = models.PositiveSmallIntegerField(null=True, blank=True)
    #p23A
    hour_of_death = models.IntegerField(null=True, blank=True)
    #p23B
    minute_of_death = models.IntegerField(null=True, blank=True)
    #p100a
    lag_hours = models.PositiveSmallIntegerField(null=True, blank=True)
    #p100b
    lag_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    #NM4
    vehicle_which_struck_non_motorist = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="vehicle_which_struck_nonmotorist")
    #nm8
    parked_vehicle_which_struck_non_motorist = models.ForeignKey(ParkedVehicle, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="parked_vehicle_which_struck_nonmotorist")
    #nm8
    non_motorist_device_type_choices = [
        (0, 'Not Applicable'),
        (1, 'Ridden Animal, Animal Drawn Conveyance, or Trailer'),
        (2, 'Railway Vehicle or Road Vehicle on Rails'),
        (3, 'Bicycle'),
        (4, 'Other Pedalcycle'),
        (5, 'Mobility Aid Device'),
        (6, 'Skates'),
        (7, 'Non-Self-Balancing Board (Skateboard)'),
        (8, 'Self-Balancing Board'),
        (9, 'Standing or Seated Scooter'),
        (97, 'Personal Conveyance, Other'),
        (98, 'Personal Conveyance, Unknown Type'),
        (99, 'Unknown Type of Non-Motorist'),
    ]
    non_motorist_device_type = models.PositiveSmallIntegerField(choices=non_motorist_device_type_choices, default=0)
    #nm9
    non_motorist_device_motorization_choices = [
        (0, "Not Applicable"),
        (1, "Not Motorized"),
        (2, "Motorized"),
        (3, "Unknown/Not Reported if Motorized"),
        (9, "Unknown Type of Non-Motorist")
    ]
    non_motorist_device_motorization = models.PositiveSmallIntegerField(choices=non_motorist_device_motorization_choices, default=0)
    #nm10
    non_motorist_location_choices = [
        (0, 'Occupant of a Motor Vehicle (Includes Railway Train Occupants Since 2006)'),
        (1, 'At Intersection-In Marked Crosswalk'),
        (2, 'At Intersection-Unmarked/Unknown if Marked Crosswalk'),
        (3, 'At Intersection-Not in Crosswalk'),
        (9, 'At Intersection-Unknown Location'),
        (10, 'Not at Intersection-In Marked Crosswalk'),
        (11, 'Non at Intersection-On Roadway, Not in Marked Crosswalk'),
        (13, 'Not at Intersection-On Roadway, Crosswalk Availability Unknown'),
        (14, 'Parking Lane/Zone'),
        (16, 'Bicycle Lane'),
        (20, 'Shoulder/Roadside'),
        (21, 'Sidewalk'),
        (22, 'Median/Crossing Island'),
        (23, 'Driveway Access'),
        (24, 'Shared-Use Path'),
        (25, 'Non-Trafficway Area'),
        (28, 'Other'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown Location'),
    ]
    non_motorist_location = models.PositiveSmallIntegerField(choices=non_motorist_location_choices, default=0)
    #sp2 
    at_work_choices = [
        (0, "No"),
        (1, "Yes"),
        (7, "Redacted"),
        (8, "Not Aplicable"),
        (9, "Unknown")
    ]
    at_work = models.PositiveSmallIntegerField(choices=at_work_choices, default=9)
    hispanic_choices = [
        (0, 'Not a Fatality (Not Applicable)'),
        (1, 'Mexican'),
        (2, 'Puerto Rican'),
        (3, 'Cuban'),
        (4, 'Central or South American'),
        (5, 'European Spanish (Since 2000)'),
        (6, 'Hispanic, Origin Not Specified or Other Origin'),
        (7, 'Non-Hispanic'),
        (97, "Redacted"),
        (99, 'Unknown')
    ]
    hispanic = models.PositiveSmallIntegerField(choices=hispanic_choices, default=99)

    def vehicle_or_parked_vehicle_id(self):
        if self.vehicle:
            return self.vehicle.id
        if self.parked_vehicle:
            return self.parked_vehicle.id
        return None

    def vehicle_or_parked_vehicle_number(self):
        if self.vehicle:
            return self.vehicle.vehicle_number
        if self.parked_vehicle:
            return self.parked_vehicle.vehicle_number
        return None

    class Meta:
        unique_together = [["accident", "vehicle", "person_number"]]
        db_table = "person"
        managed = True



class PedestrianType(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    person = models.OneToOneField(Person, on_delete = models.CASCADE)
    #p5
    age = models.PositiveSmallIntegerField(null = True)
    #p6 
    sex_choices = [
        (1, "Male"),
        (2, "Female"),
        (3, "Other"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    sex = models.PositiveSmallIntegerField(choices=sex_choices, default=8)
    #p7 PBPTYPE
    person_type_choices = [
        (5, "Pedestrian"),
        (6, "Bicyclist"),
        (7, "Other Pedalcyclist"),
        (8, "Person on a Personal Conveyance")
    ]
    person_type = models.PositiveSmallIntegerField(choices=person_type_choices, default=5)
    # NM11-PB27 PBCWALK
    marked_crosswalk_present_choices = [
        (0, "None Noted"),
        (1, "Yes"),
        (9, "Unknown")
    ]
    marked_crosswalk_present = models.PositiveSmallIntegerField(choices=marked_crosswalk_present_choices, default=9)
    # NM11-PB28 PBSWALK
    sidewalk_present_choices = [
        (0, "None Noted"),
        (1, "Yes"),
        (9, "Unknown")
    ]
    sidewalk_present = models.PositiveSmallIntegerField(choices=sidewalk_present_choices, default=9)
    # NM11-PB29 PBSZONE
    in_school_zone_choices = [
        (0, "None Noted"),
        (1, "Yes"),
        (9, "Unknown")
    ]
    in_school_zone = models.PositiveSmallIntegerField(choices=in_school_zone_choices, default=9)
    # NM11-PB30 PEDCTYPE
    pedestrian_crash_type_choices = [
        (0, 'Not a Pedestrian'),
        (120, 'Dispute-Related'),
        (130, 'Pedestrian on Vehicle'),
        (140, 'Vehicle Into Vehicle or Vehicle Into Object'),
        (150, 'Motor Vehicle Loss of Control'),
        (160, 'Pedestrian Loss of Control'),
        (190, 'Other Unusual Circumstances'),
        (211, 'Backing Vehicle - Non-Trafficway - Driveway'),
        (212, 'Backing Vehicle - Driveway Access'),
        (213, 'Backing Vehicle - Trafficway'),
        (214, 'Backing Vehicle - Non-Trafficway - Parking Lot'),
        (219, 'Backing Vehicle - Other/Unknown'),
        (220, 'Driverless Vehicle'),
        (230, 'Disabled Vehicle-Related'),
        (240, 'Emergency Vehicle-Related'),
        (250, 'Play Vehicle-Related'),
        (311, 'Working in Roadway'),
        (312, 'Playing in Roadway'),
        (313, 'Lying in Roadway'),
        (320, 'Entering/Exiting Parked or Stopped Vehicle'),
        (330, 'Mailbox-Related'),
        (341, 'Transit Bus Stop-Related'),
        (342, 'School Bus Stop-Related'),
        (360, 'Ice Cream/Vendor Truck-Related'),
        (410, 'Walking/Running Along Roadway With Traffic - From Behind'),
        (420, 'Walking/Running Along Roadway With Traffic - From Front'),
        (430, 'Walking/Running Along Roadway Against Traffic - From Behind'),
        (440, 'Walking/Running Along Roadway Against Traffic - From Front'),
        (459, 'Walking/Running Along Roadway - Direction/Position Unknown'),
        (461, 'Motorist Entering Driveway'),
        (465, 'Motorist Exiting Driveway'),
        (469, 'Driveway Access - Other/Unknown'),
        (510, 'Waiting to Cross - Vehicle Turning'),
        (520, 'Waiting to Cross - Vehicle Not Turning'),
        (590, 'Waiting to Cross - Vehicle Action Unknown'),
        (610, 'Standing in Roadway'),
        (620, 'Walking in Roadway'),
        (680, 'Not at Intersection - Other/Unknown'),
        (690, 'At Intersection - Other/Unknown'),
        (710, 'Multiple Threat'),
        (730, 'Trapped'),
        (741, 'Dash - Run, No Visial Obstruction Noted'),
        (742, 'Dart-out - Visual Obstruction Noted'),
        (760, 'Pedestrian Failed to Yield'),
        (770, 'Motorist Failed to Yield'),
        (781, 'Motorist Left Turn - Parallel Paths'),
        (782, 'Motorist Left Turn - Perpendicular Paths'),
        (791, 'Motorist Right Turn - Parallel Paths'),
        (792, 'Motorist Right Turn on Red - Parallel Paths'),
        (794, 'Motorist Right Turn on Red - Perpendicular Paths'),
        (795, 'Motorist Right Turn - Perpendicular Paths'),
        (799, 'Motorist Turn/Merge - Other/Unknown'),
        (830, 'Non-Trafficway - Parking Lot'),
        (890, 'Non-Trafficway - Other/Unknown'),
        (900, 'Other - Unknown Location'),
        (910, 'Crossing an Expressway'),
    ]
    pedestrian_crash_type = models.PositiveSmallIntegerField(choices=pedestrian_crash_type_choices, default=0)
    # NM11-PB30B BIKECTYPE
    bicycle_crash_type_choices = [
        (0, 'Not a Cyclist'),
        (111, 'Motorist Turning Error - Left Turn'),
        (112, 'Motorist Turning Error - Right Turn'),
        (113, 'Motorist Turning Error - Other'),
        (114, 'Bicyclist Turning Error - Left Turn'),
        (115, 'Bicyclist Turning Error - Right Turn'),
        (116, 'Bicyclist Turning Error - Other'),
        (121, 'Bicyclist Lost Control - Mechanical Problems'),
        (122, 'Bicyclist Lost Control - Oversteering, Improper Braking, Speed'),
        (123, 'Bicyclist Lost Control - Alcohol/Drug Impairment'),
        (124, 'Bicyclist Lost Control - Surface Conditions'),
        (129, 'Bicyclist Lost Control - Other/Unknown'),
        (131, 'Motorist Lost Control - Mechanical Problems'),
        (132, 'Motorist Lost Control - Oversteering, Improper Braking, Speed'),
        (133, 'Motorist Lost Control - Alcohol/Drug Impairment'),
        (134, 'Motorist Lost Control - Surface Conditions'),
        (139, 'Motorist Lost Control - Other/Unknown'),
        (141, 'Motorist Drive-out - Sign-Controlled Intersection'),
        (142, 'Bicyclist Ride-out - Sign-Controlled Intersection'),
        (143, 'Motorist Drive-Through - Sign-Controlled Intersection'),
        (144, 'Bicyclist Ride-Through - Sign-Controlled Intersection'),
        (147, 'Multiple Threat - Sign-Controlled Intersection'),
        (148, 'Sign-Controlled Intersection - Other/Unknown'),
        (151, 'Motorist Drive-out - Right Turn on Red'),
        (152, 'Motorist Drive-out - Signalized Intersection'),
        (153, 'Bicyclist - Ride-out - Signalized Intersection'),
        (154, 'Motorist Drive-Through - Signalized Intersection'),
        (155, 'Bicyclist Ride-Through - Signalized Intersection'),
        (156, 'Bicyclist Failed to Clear - Trapped'),
        (157, 'Bicyclist Failed to Clear - Multiple Threat'),
        (158, 'Signalized Intersection - Other/Unknown'),
        (159, 'Bicyclist Failed to Clear - Unknown'),
        (160, 'Crossing Paths - Uncontrolled Intersection'),
        (180, 'Crossing Paths - Intersection - Other/Unknown'),
        (211, 'Motorist Left Turn - Same Direction'),
        (212, 'Motorist Left Turn - Opposite Direction'),
        (213, 'Motorist Right Turn - Same Direction'),
        (214, 'Motorist Right Turn - Opposite Direction'),
        (215, 'Motorist Drive-in/out - Parking'),
        (216, 'Bus/Delivery Vehicle Pullover'),
        (217, 'Motorist Right Turn on Red - Same Direction'),
        (218, 'Motorist Right Turn on Red - Opposite Direction'),
        (219, 'Motorist Turn/Merge - Other/Unknown'),
        (221, 'Bicyclist Left Turn - Same Direction'),
        (222, 'Bicyclist Left Turn - Opposite Direction'),
        (223, 'Bicyclist Right Turn - Same Direction'),
        (224, 'Bicyclist Right Turn - Opposite Direction'),
        (225, 'Bicyclist Ride-out - Parallel Path'),
        (231, 'Motorist Overtaking - Undetected Bicyclist'),
        (232, 'Motorist Overtaking - Misjudged Space'),
        (235, 'Motorist Overtaking - Bicyclist Swerved'),
        (239, 'Motorist Overtaking - Other/Unknown'),
        (241, 'Bicyclist Overtaking - Passing on Right'),
        (242, 'Bicyclist Overtaking - Passing on Left'),
        (243, 'Bicyclist Overtaking - Parked Vehicle'),
        (244, 'Bicyclist Overtaking - Extended Door'),
        (249, 'Bicyclist Overtaking - Other/Unknown'),
        (250, 'Wrong-Way/Wrong-Side - Bicyclist'),
        (255, 'Wrong-Way/Wrong-Side - Motorist'),
        (259, 'Wrong-Way/Wrong-Side - Unknown'),
        (280, 'Parallel Paths - Other/Unknown'),
        (311, 'Bicyclist Ride-out - Residential Driveway'),
        (312, 'Bicyclist Ride-out - Commercial Driveway'),
        (313, 'Bicyclist Ride-out - Driveway, Unknown Type'),
        (318, 'Bicyclist Ride-out - Other Midblock'),
        (319, 'Bicyclist Ride-out - Unknown'),
        (321, 'Motorist Drive-out - Residential Driveway'),
        (322, 'Motorist Drive-out - Commercial Driveway'),
        (323, 'Motorist Drive-out - Driveway, Unknown Type'),
        (328, 'Motorist Drive-out - Other Midblock'),
        (329, 'Motorist Drive-out - Midblock - Unknown'),
        (357, 'Multiple Threat - Midblock'),
        (380, 'Crossing Paths - Midblock - Other/Unknown'),
        (610, 'Backing Vehicle'),
        (700, 'Play Vehicle-Related'),
        (800, 'Unusual Circumstances'),
        (910, 'Non-Trafficway'),
        (970, 'Unknown Approach Paths'),
        (980, 'Unknown Location'),
    ]
    bicycle_crash_type = models.PositiveSmallIntegerField(choices=bicycle_crash_type_choices, default=0)

    # NM11-PB31 PEDLOC
    pedestrian_location_choices = [
        (1, 'At Intersection'),
        (2, 'Intersection-Related'),
        (3, 'Not at Intersection'),
        (4, 'Non-Trafficway Location'),
        (7, 'Not a Pedestrian'),
        (9, 'Unknown/Insufficient Information'),
    ]
    pedestrian_location = models.PositiveSmallIntegerField(choices=pedestrian_location_choices, default=7)
    # NM11-PB31B BIKELOC
    bicycle_location_choices = [
        (1, 'At Intersection'),
        (2, 'Intersection-Related'),
        (3, 'Not at Intersection'),
        (4, 'Non-Trafficway Location'),
        (7, 'Not a Cyclist'),
        (9, 'Unknown/Insufficient Information'),
    ]
    bicycle_location = models.PositiveSmallIntegerField(choices=bicycle_location_choices, default=7)

    # NM11-PB32 PEDPOS
    pedestrian_position_choices = [
        (1, 'Intersection Area'),
        (2, 'Crosswalk Area'),
        (3, 'Travel Lane'),
        (4, 'Paved Shoulder/Bicycle Lane/Parking Lane'),
        (5, 'Sidewalk/Shared-Use Path/Driveway Access'),
        (6, 'Unpaved Right-of-Way'),
        (7, 'Non-Trafficway - Driveway'),
        (8, 'Non-Trafficway - Parking Lot/Other'),
        (9, 'Other/Unknown'),
        (77, 'Not a Pedestrian'),
    ]
    pedestrian_position = models.PositiveSmallIntegerField(choices=pedestrian_position_choices, default=77)
    # NM11-PB32B BIKEPOS
    bicycle_position_choices = [
        (1, 'Travel Lane'),
        (2, 'Bicycle Lane/Paved Shoulder/Parking Lane'),
        (3, 'Sidewalk/Crosswalk/Driveway Access'),
        (4, 'Shared-Use Path'),
        (5, 'Non-Trafficway - Driveway'),
        (6, 'Non-Trafficway - Parking Lot/Other'),
        (7, 'Not a Cyclist'),
        (8, 'Other'),
        (9, 'Unknown'),
    ]
    bicycle_position = models.PositiveSmallIntegerField(choices=bicycle_position_choices, default=7)

    # NM11-PB33 PEDDIR
    pedestrian_direction_choices = [
        (1, 'Northbound'),
        (2, 'Eastbound'),
        (3, 'Southbound'),
        (4, 'Westbound'),
        (7, 'Not a Pedestrian'),
        (8, 'Not Applicable'),
        (9, 'Not Derived/Unknown Initial Direction of Travel'),
    ]
    pedestrian_direction = models.PositiveSmallIntegerField(choices=pedestrian_direction_choices, default=7)
    # NM11-PB33B BIKEDIR
    bicycle_direction_choices = [
        (1, "With Traffic"),
        (2, "Facing Traffic"),
        (3, "Not Applicable"),
        (7, "Not a Cyclist"),
        (9, "Unknown")
    ]
    bicycle_direction = models.PositiveSmallIntegerField(choices=bicycle_direction_choices, default=7)

    # NM11-PB34 MOTDIR
    motorist_direction_choices = [
        (1, 'Northbound'),
        (2, 'Eastbound'),
        (3, 'Southbound'),
        (4, 'Westbound'),
        (7, 'Not a Pedestrian'),
        (8, 'Not Applicable'),
        (9, 'Unknown Initial Direction of Travel'),
    ]
    motorist_direction = models.PositiveSmallIntegerField(choices=motorist_direction_choices, default=9)
    # NM11-PB35  MOTMAN
    motorist_maneuver_choices = [
        (1, 'Left Turn'),
        (2, 'Right Turn'),
        (3, 'Straight Through'),
        (7, 'Not a Pedestrian'),
        (8, 'Not Applicable'),
        (9, 'Unknown Motorist Maneuver'),
    ]
    motorist_maneuver = models.PositiveSmallIntegerField(choices=motorist_maneuver_choices, default=9)

    # NM11-PB36 PEDLEG
    intersection_leg_choices = [
        (1, "Nearside"),
        (2, "Farside"),
        (7, "Not a Pedestrian"),
        (8, "Not Applicable"),
        (9, "Unknown/None of the Above")

    ]
    intersection_leg = models.PositiveSmallIntegerField(choices=intersection_leg_choices, default=9)
    # NM11-PB37 PEDSNR
    pedestrian_scenario_choices = [
        ('1a', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Traveled From Motorist’s Left.'),
        ('1b', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Traveled From Motorist’s Right.'),
        ('1c', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Unknown.'),
        ('1d', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Other (Since 2017)'),
        ('2a', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Traveled From Motorist’s Left.'),
        ('2b', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Traveled From Motorist’s Right.'),
        ('2c', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Unknown.'),
        ('2d', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Other (Since 2017)'),
        ('3a', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Traveled From Motorist’s Left.'),
        ('3b', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Traveled From Motorist’s Right.'),
        ('3c', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Unknown.'),
        ('3d', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Other (Since 2017)'),
        ('4a', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Traveled From Motorist’s Left.'),
        ('4b', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Traveled From Motorist’s Right.'),
        ('4c', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Unknown.'),
        ('4d', 'MOTORIST TRAVELING STRAIGHT THROUGH - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Other (Since 2017)'),
        ('5a', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Traveled From Motorist’s Left.'),
        ('5b', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Traveled From Motorist’s Right.'),
        ('5c', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Unknown.'),
        ('5d', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Other (Since 2017)'),
        ('6a', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Traveled From Motorist’s Left.'),
        ('6b', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Traveled From Motorist’s Right.'),
        ('6c', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Unknown.'),
        ('6d', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Other (Since 2017)'),
        ('7a', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Same as Motorist’s.'),
        ('7b', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Opposite Motorist’s.'),
        ('7c', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Unknown.'),
        ('7d', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Other (Since 2017)'),
        ('8a', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Same as Motorist’s.'),
        ('8b', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Opposite Motorist’s.'),
        ('8c', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Unknown.'),
        ('8d', 'MOTORIST TURNING RIGHT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Other (Since 2017)'),
        ('9a', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Traveled From Motorist’s Left.'),
        ('9b', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Traveled From Motorist’s Right.'),
        ('9c', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Unknown.'),
        ('9d', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Other (Since 2017)'),
        ('10a', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Traveled From Motorist’s Left.'),
        ('10b', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Traveled From Motorist’s Right.'),
        ('10c', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Unknown.'),
        ('10d', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON NEAR (APPROACH) SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Other (Since 2017)'),
        ('11a', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Same as Motorist’s.'),
        ('11b', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Opposite Motorist’s.'),
        ('11c', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Approach Direction Unknown.'),
        ('11d', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Within Crosswalk Area, Other (Since 2017)'),
        ('12a', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Same as Motorist’s.'),
        ('12b', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Opposite Motorist’s.'),
        ('12c', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Approach Direction Unknown.'),
        ('12d', 'MOTORIST TURNING LEFT - CRASH OCCURRED ON FAR SIDE OF INTERSECTION - Pedestrian Outside Crosswalk Area, Other (Since 2017)'),
        ('7', 'Not a Pedestrian'),
        ('8', 'Not Applicable'),
        ('99', 'Unknown/Insufficient Information (Since 2017)'),
    ]
    pedestrian_scenario = models.CharField(choices=pedestrian_scenario_choices, default="99", max_length=16)

    # NM11-PB38 PEDCGP
    pedestrian_crash_group_choices = [
        (0, 'Not a Pedestrian'),
        (100, 'Unusual Circumstances'),
        (200, 'Backing Vehicle'),
        (310, 'Working or Playing in Roadway'),
        (340, 'Bus Stop-Related'),
        (350, 'Unique Midblock'),
        (400, 'Walking/Running Along Roadway'),
        (460, 'Driveway Access/Driveway Access-Related'),
        (500, 'Waiting to Cross'),
        (600, 'Pedestrian in Roadway - Circumstances Unknown'),
        (720, 'Multiple Threat/Trapped'),
        (740, 'Dash - Run, No Visual Obstruction Noted/ Dart-out - Visual Obstruction Noted'),
        (750, 'Crossing Roadway - Vehicle Not Turning'),
        (790, 'Crossing Roadway - Vehicle Turning'),
        (800, 'Non-Trafficway'),
        (910, 'Crossing Expressway'),
        (990, 'Other/Unknown - Insufficient Details'),
    ]
    pedestrian_crash_group = models.PositiveSmallIntegerField(choices=pedestrian_crash_group_choices, default=0)
    # NM11-PB38B BIKECGP
    bike_crash_group_choices = [
        (0, 'Not a Cyclist'),
        (110, 'Loss of Control/Turning Error'),
        (140, 'Motorist Failed to Yield - Sign-Controlled Intersection'),
        (145, 'Bicyclist Failed to Yield - Sign-Controlled Intersection'),
        (150, 'Motorist Failed to Yield - Signalized Intersection'),
        (158, 'Bicyclist Failed to Yield - Signalized Intersection'),
        (190, 'Crossing Paths - Other Circumstances'),
        (210, 'Motorist Left Turn/Merge'),
        (215, 'Motorist Right Turn/Merge'),
        (219, 'Parking/Bus-Related'),
        (220, 'Bicyclist Left Turn/Merge'),
        (225, 'Bicyclist Right Turn/Merge'),
        (230, 'Motorist Overtaking Bicyclist'),
        (240, 'Bicyclist Overtaking Motorist'),
        (258, 'Wrong-Way/Wrong-Side'),
        (290, 'Parallel Paths - Other Circumstances'),
        (310, 'Bicyclist Failed to Yield - Midblock'),
        (320, 'Motorist Failed to Yield - Midblock'),
        (600, 'Backing Vehicle'),
        (850, 'Other/Unusual Circumstances'),
        (910, 'Non-Trafficway'),
        (990, 'Other/Unknown - Insufficient Details'),
    ]
    bike_crash_group = models.PositiveSmallIntegerField(choices=bike_crash_group_choices, default=0)

    class Meta:
        db_table = "pedestrian_type"
        managed = True


class CrashEvent(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    accident = models.ForeignKey(Accident, null=False, on_delete=models.CASCADE)
    crash_event_number = models.PositiveSmallIntegerField(null=False)
    # VNUMBER1 c18a
    vehicle_1 = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.CASCADE, related_name="crash_event_vehicle_1")
    vehicle_2 = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.CASCADE, related_name="crash_event_vehicle_2")
    parked_vehicle_1 = models.ForeignKey(ParkedVehicle, null=True, blank=True, on_delete=models.CASCADE, related_name="crash_event_parked_vehicle_1")
    parked_vehicle_2 = models.ForeignKey(ParkedVehicle, null=True, blank=True, on_delete=models.CASCADE, related_name="crash_event_parked_vehicle_2")

    @property
    def vehicle_id_1(self):
        if self.vehicle_1.id:
            return self.vehicle_1.id
        if self.parked_vehicle_1.id:
            return self.parked_vehicle_1.id
        return None
    
    @property
    def vehicle_number_1(self):
        if self.vehicle_1.vehicle_number:
            return self.vehicle_1.vehicle_number
        if self.parked_vehicle_1.vehicle_number:
            return self.parked_vehicle_1.vehicle_number
        return None
    
    @property
    def vehicle_number_2(self):
        if self.vehicle_2:
            return self.vehicle_2.vehicle_number
        if self.parked_vehicle_2:
            return self.parked_vehicle_2.vehicle_number
        return None
    
    @property
    def vehicle_id_2(self):
        if self.vehicle_2.id:
            return self.vehicle_2.id
        if self.parked_vehicle_2.id:
            return self.parked_vehicle_2.id
        return None
    
    # C18B AOI1 
    area_of_impact_choices = [
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
        (13,'Top'),
        (14,'Undercarriage'),
        (15, "Underride"),
        (16, "Override"),
        (18,'Cargo/Vehicle Parts Set-in-Motion'),
        (19,'Other Objects or Person Set-in-Motion'),
        (20,'Object Set in Motion, Unknown if Cargo/Vehicle Parts or Other'),
        (55,'Non-Harmful Event'),
        (61,'Left'),
        (62,'Left-Front Side'),
        (63,'Left-Back Side'),
        (77,'Not a Motor Vehicle'),
        (81,'Right'),
        (82,'Right-Front Side'),
        (83,'Right-Back Side'),
        (98,'Not Reported'),
        (99,'Reported as Unknown'),
    ]
    area_of_impact_1 = models.PositiveSmallIntegerField(choices=area_of_impact_choices, default=98)
    area_of_impact_2 = models.PositiveSmallIntegerField(choices=area_of_impact_choices, default=98)
    # V37 SOE
    sequence_of_events_choices = [
        (1,'Rollover/Overturn'),
        (2,'Fire/Explosion'),
        (3,'Immersion or Partial Immersion'),
        (4,'Gas Inhalation'),
        (5,'Fell/Jumped From Vehicle'),
        (6,'Injured in Vehicle (Non-Collision)'),
        (7,'Other Non-Collision'),
        (8,'Pedestrian'),
        (9,'Pedalcyclist'),
        (10,'Railway Vehicle'),
        (11,'Live Animal'),
        (12,'Motor Vehicle In-Transport'),
        (14,'Parked Motor Vehicle'),
        (15,'Non-Motorist on Personal Conveyance'),
        (16,'Thrown or Falling Object'),
        (17,'Boulder'),
        (18,'Other Object (Not Fixed)'),
        (19,'Building'),
        (20,'Impact Attenuator/Crash Cushion'),
        (21,'Bridge Pier or Support'),
        (23,'Bridge Rail (Includes Parapet)'),
        (24,'Guardrail Face'),
        (25,'Concrete Traffic Barrier'),
        (26,'Other Traffic Barrier'),
        (30,'Utility Pole/Light Support'),
        (31,'Post, Pole or Other Support'),
        (32,'Culvert'),
        (33,'Curb'),
        (34,'Ditch'),
        (35,'Embankment'),
        (38,'Fence'),
        (39,'Wall'),
        (40,'Fire Hydrant'),
        (41,'Shrubbery'),
        (42,'Tree (Standing Only)'),
        (43,'Other Fixed Object'),
        (44,'Pavement Surface Irregularity(Ruts, Potholes, Grates, etc.)'),
        (45,'Working Motor Vehicle'),
        (46,'Traffic Signal Support'),
        (47, "Vehicle Occupant Struck or Run Over by Own Vehicle"),
        (48,'Snow Bank'),
        (49,'Ridden Animal or Animal-Drawn Conveyance'),
        (50,'Bridge Overhead Structure'),
        (51,'Jackknife (Harmful to This Vehicle)'),
        (52,'Guardrail End'),
        (53,'Mail Box'),
        (54,'Motor Vehicle In-Transport Strikes or Is Struck by Cargo, Persons or Objects Set-in-Motion From/by Another Motor Vehicle In-Transport'),
        (55,'Motor Vehicle in Motion Outside the Trafficway'),
        (57,'Cable Barrier'),
        (58,'Ground'),
        (59,'Traffic Sign Support'),
        (60,'Cargo/Equipment Loss or Shift (Non-Harmful)'),
        (61,'Equipment Failure (Blown Tire, Brake Failure, etc.)'),
        (62,'Separation of Units'),
        (63,'Ran off Road - Right'),
        (64,'Ran off Road - Left'),
        (65,'Cross Median'),
        (66,'Downhill Runaway'),
        (67,'Vehicle Went Airborne'),
        (68,'Cross Centerline'),
        (69,'Re-Entering Highway'),
        (70,'Jackknife (Non-Harmful)'),
        (71,'End Departure'),
        (72,'Cargo/Equipment Loss, Shift, or Damage (Harmful)'),
        (73,'Object That Had Fallen From Motor Vehicle In-Transport'),
        (74,'Road Vehicle on Rails'),
        (79,'Ran off Roadway - Direction Unknown'),
        (91,'Unknown Object Not Fixed'),
        (93,'Unknown Fixed Object'),
        (98,'Harmful Event, Details Not Reported (Since 2019)'),
        (99,'Unknown/Reported as Unknown (Since 2018)'),
    ]
    sequence_of_events = models.PositiveSmallIntegerField(choices=sequence_of_events_choices, default=98)
    
    class Meta:
        unique_together = [["accident", "crash_event_number"]]
        db_table = "crash_event"
        managed = True

class VehicleEvent(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=True, blank = True, on_delete=models.CASCADE)
    crash_event = models.ForeignKey(CrashEvent, null=False, blank=False, on_delete=models.CASCADE)
    vehicle_event_number = models.PositiveSmallIntegerField(null=False)

    # VNUMBER1 C18A
    vehicle_1 = models.ForeignKey(Vehicle, null=True, blank = True, on_delete=models.DO_NOTHING, related_name="vehicle_event_vehicle_1")
    vehicle_2 = models.ForeignKey(Vehicle, null=True, blank = True, on_delete=models.DO_NOTHING, related_name="vehicle_event_vehicle_2")
    parked_vehicle_1 = models.ForeignKey(ParkedVehicle, null=True, blank = True, on_delete=models.DO_NOTHING, related_name="parked_vehicle_event_vehicle_1")
    parked_vehicle_2 = models.ForeignKey(ParkedVehicle, null=True, blank = True, on_delete=models.DO_NOTHING, related_name="parked_vehicle_event_vehicle_2")
    # C18B AOI1 
    area_of_impact_choices = [
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
        (13,'Top'),
        (14,'Undercarriage'),
        (15, "Underride"),
        (16, "Override"),
        (18,'Cargo/Vehicle Parts Set-in-Motion'),
        (19,'Other Objects or Person Set-in-Motion'),
        (20,'Object Set in Motion, Unknown if Cargo/Vehicle Parts or Other'),
        (55,'Non-Harmful Event'),
        (61,'Left'),
        (62,'Left-Front Side'),
        (63,'Left-Back Side'),
        (77,'Not a Motor Vehicle'),
        (81,'Right'),
        (82,'Right-Front Side'),
        (83,'Right-Back Side'),
        (98,'Not Reported'),
        (99,'Reported as Unknown'),
    ]
    area_of_impact_1 = models.PositiveSmallIntegerField(choices=area_of_impact_choices, default=98)
    area_of_impact_2 = models.PositiveSmallIntegerField(choices=area_of_impact_choices, default=98)
    # V37 SOE

    sequence_of_events_choices = [
        (1,'Rollover/Overturn'),
        (2,'Fire/Explosion'),
        (3,'Immersion or Partial Immersion'),
        (4,'Gas Inhalation'),
        (5,'Fell/Jumped From Vehicle'),
        (6,'Injured in Vehicle (Non-Collision)'),
        (7,'Other Non-Collision'),
        (8,'Pedestrian'),
        (9,'Pedalcyclist'),
        (10,'Railway Vehicle'),
        (11,'Live Animal'),
        (12,'Motor Vehicle In-Transport'),
        (14,'Parked Motor Vehicle'),
        (15,'Non-Motorist on Personal Conveyance'),
        (16,'Thrown or Falling Object'),
        (17,'Boulder'),
        (18,'Other Object (Not Fixed)'),
        (19,'Building'),
        (20,'Impact Attenuator/Crash Cushion'),
        (21,'Bridge Pier or Support'),
        (23,'Bridge Rail (Includes Parapet)'),
        (24,'Guardrail Face'),
        (25,'Concrete Traffic Barrier'),
        (26,'Other Traffic Barrier'),
        (30,'Utility Pole/Light Support'),
        (31,'Post, Pole or Other Support'),
        (32,'Culvert'),
        (33,'Curb'),
        (34,'Ditch'),
        (35,'Embankment'),
        (38,'Fence'),
        (39,'Wall'),
        (40,'Fire Hydrant'),
        (41,'Shrubbery'),
        (42,'Tree (Standing Only)'),
        (43,'Other Fixed Object'),
        (44,'Pavement Surface Irregularity(Ruts, Potholes, Grates, etc.)'),
        (45,'Working Motor Vehicle'),
        (46,'Traffic Signal Support'),
        (47, "Vehicle Occupant Struck or Run Over by Own Vehicle"),
        (48,'Snow Bank'),
        (49,'Ridden Animal or Animal-Drawn Conveyance'),
        (50,'Bridge Overhead Structure'),
        (51,'Jackknife (Harmful to This Vehicle)'),
        (52,'Guardrail End'),
        (53,'Mail Box'),
        (54,'Motor Vehicle In-Transport Strikes or Is Struck by Cargo, Persons or Objects Set-in-Motion From/by Another Motor Vehicle In-Transport'),
        (55,'Motor Vehicle in Motion Outside the Trafficway'),
        (57,'Cable Barrier'),
        (58,'Ground'),
        (59,'Traffic Sign Support'),
        (60,'Cargo/Equipment Loss or Shift (Non-Harmful)'),
        (61,'Equipment Failure (Blown Tire, Brake Failure, etc.)'),
        (62,'Separation of Units'),
        (63,'Ran off Road - Right'),
        (64,'Ran off Road - Left'),
        (65,'Cross Median'),
        (66,'Downhill Runaway'),
        (67,'Vehicle Went Airborne'),
        (68,'Cross Centerline'),
        (69,'Re-Entering Highway'),
        (70,'Jackknife (Non-Harmful)'),
        (71,'End Departure'),
        (72,'Cargo/Equipment Loss, Shift, or Damage (Harmful)'),
        (73,'Object That Had Fallen From Motor Vehicle In-Transport'),
        (74,'Road Vehicle on Rails'),
        (79,'Ran off Roadway - Direction Unknown'),
        (91,'Unknown Object Not Fixed'),
        (93,'Unknown Fixed Object'),
        (98,'Harmful Event, Details Not Reported (Since 2019)'),
        (99,'Unknown/Reported as Unknown (Since 2018)'),
    ]
    sequence_of_events = models.PositiveSmallIntegerField(choices=sequence_of_events_choices, default=98)
    
    class Meta:
        unique_together = [["vehicle", "vehicle_event_number"]]
        db_table = "vehicle_event"
        managed = True


class VehicleSequenceOfEvents(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete = models.CASCADE)
    parked_vehicle = models.ForeignKey(ParkedVehicle, null=True, blank=True, on_delete = models.CASCADE)
    vehicle_event_number = models.PositiveSmallIntegerField(null=False)
    # C18E AOI
    area_of_impact_choices = [
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
        (13,'Top'),
        (14,'Undercarriage'),
        (15, "Underride"),
        (16, "Override"),
        (18,'Cargo/Vehicle Parts Set-in-Motion'),
        (19,'Other Objects or Person Set-in-Motion'),
        (20,'Object Set in Motion, Unknown if Cargo/Vehicle Parts or Other'),
        (55,'Non-Harmful Event'),
        (61,'Left'),
        (62,'Left-Front Side'),
        (63,'Left-Back Side'),
        (77,'Not a Motor Vehicle'),
        (81,'Right'),
        (82,'Right-Front Side'),
        (83,'Right-Back Side'),
        (98,'Not Reported'),
        (99,'Reported as Unknown'),
    ]
    area_of_impact = models.PositiveSmallIntegerField(choices=area_of_impact_choices, default=98)
    # V37 SOE
    sequence_of_events_choices = [
        (1,'Rollover/Overturn'),
        (2,'Fire/Explosion'),
        (3,'Immersion or Partial Immersion'),
        (4,'Gas Inhalation'),
        (5,'Fell/Jumped From Vehicle'),
        (6,'Injured in Vehicle (Non-Collision)'),
        (7,'Other Non-Collision'),
        (8,'Pedestrian'),
        (9,'Pedalcyclist'),
        (10,'Railway Vehicle'),
        (11,'Live Animal'),
        (12,'Motor Vehicle In-Transport'),
        (14,'Parked Motor Vehicle'),
        (15,'Non-Motorist on Personal Conveyance'),
        (16,'Thrown or Falling Object'),
        (17,'Boulder'),
        (18,'Other Object (Not Fixed)'),
        (19,'Building'),
        (20,'Impact Attenuator/Crash Cushion'),
        (21,'Bridge Pier or Support'),
        (23,'Bridge Rail (Includes Parapet)'),
        (24,'Guardrail Face'),
        (25,'Concrete Traffic Barrier'),
        (26,'Other Traffic Barrier'),
        (30,'Utility Pole/Light Support'),
        (31,'Post, Pole or Other Support'),
        (32,'Culvert'),
        (33,'Curb'),
        (34,'Ditch'),
        (35,'Embankment'),
        (38,'Fence'),
        (39,'Wall'),
        (40,'Fire Hydrant'),
        (41,'Shrubbery'),
        (42,'Tree (Standing Only)'),
        (43,'Other Fixed Object'),
        (44,'Pavement Surface Irregularity(Ruts, Potholes, Grates, etc.)'),
        (45,'Working Motor Vehicle'),
        (46,'Traffic Signal Support'),
        (47, "Vehicle Occupant Struck or Run Over by Own Vehicle"),
        (48,'Snow Bank'),
        (49,'Ridden Animal or Animal-Drawn Conveyance'),
        (50,'Bridge Overhead Structure'),
        (51,'Jackknife (Harmful to This Vehicle)'),
        (52,'Guardrail End'),
        (53,'Mail Box'),
        (54,'Motor Vehicle In-Transport Strikes or Is Struck by Cargo, Persons or Objects Set-in-Motion From/by Another Motor Vehicle In-Transport'),
        (55,'Motor Vehicle in Motion Outside the Trafficway'),
        (57,'Cable Barrier'),
        (58,'Ground'),
        (59,'Traffic Sign Support'),
        (60,'Cargo/Equipment Loss or Shift (Non-Harmful)'),
        (61,'Equipment Failure (Blown Tire, Brake Failure, etc.)'),
        (62,'Separation of Units'),
        (63,'Ran off Road - Right'),
        (64,'Ran off Road - Left'),
        (65,'Cross Median'),
        (66,'Downhill Runaway'),
        (67,'Vehicle Went Airborne'),
        (68,'Cross Centerline'),
        (69,'Re-Entering Highway'),
        (70,'Jackknife (Non-Harmful)'),
        (71,'End Departure'),
        (72,'Cargo/Equipment Loss, Shift, or Damage (Harmful)'),
        (73,'Object That Had Fallen From Motor Vehicle In-Transport'),
        (74,'Road Vehicle on Rails'),
        (79,'Ran off Roadway - Direction Unknown'),
        (91,'Unknown Object Not Fixed'),
        (93,'Unknown Fixed Object'),
        (98,'Harmful Event, Details Not Reported (Since 2019)'),
        (99,'Unknown/Reported as Unknown (Since 2018)'),
    ]
    sequence_of_events = models.PositiveSmallIntegerField(choices=sequence_of_events_choices, default=98)

    class Meta:
        unique_together = [["vehicle", "vehicle_event_number"]]
        db_table = "vehicle_sequence_of_events"
        managed = True


class CrashRelatedFactors(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.CASCADE)
    # CRASHRF C32
    crash_related_factor_choices = [
        (0, 'None Noted'),
        (1, 'Inadequate Warning of Exits, Lanes Narrowing, Traffic Controls, etc.'),
        (2, 'Shoulder Design or Condition'),
        (3, 'Other Maintenance or Construction-Created Condition'),
        (4, 'No or Obscured Pavement Marking'),
        (5, 'Surface Under Water'),
        (6, 'Inadequate Construction or Poor Design of Roadway, Bridge, etc.'),
        (7, 'Surface Washed out (Caved in, Road Slippage)'),
        (10, 'Emergency Vehicle Related'),
        (12, 'Distracted Driver of a Non-Contact Vehicle'),
        # 13 is deprecated in lieu of 102,103
        (13, 'Aggressive Driving/Road Rage by Non-Contact Vehicle Driver'),
        (14, 'Motor Vehicle Struck by Falling Cargo or Something That Came Loose From or Something That Was Set in Motion by a Vehicle'),
        (15, 'Non-Occupant Struck by Falling Cargo, or Something Came Loose From or Something That Was Set in Motion by a Vehicle'),
        (16, 'Non-Occupant Struck Vehicle'),
        (17, 'Stopped Vehicle Set in Motion by Non-Driver'),
        (18, 'Date of Crash and Date of EMS Notification Were Not Same Day'),
        (19, 'Recent Previous Crash Scene Nearby'),
        (20, 'Police-Pursuit-Involved'),
        (21, 'Within Designated School Zone'),
        (22, 'Speed Limit Is a Statutory Limit as Recorded or Was Determined as This State’s “Basic Rule”'),
        (23, 'Indication of a Stalled/Disabled Vehicle'),
        (24, 'Unstabilized Situation Began and All Harmful Events Occurred off of the Roadway'),
        (25, 'Toll Booth/Plaza Related'),
        (26, 'Prior Non-Recurring Incident'),
        (27, 'Backup Due to Prior Crash'),
        (28, 'Regular Congestion'),
        (30, 'Obstructed Crosswalks'),
        (31, 'Related to a Bus Stop'),
        (42, "Uncontrolled Intersection or Railroad Crossing"),
        (102, "Aggressive Driving by Non-Contact Vehicle Driver"),
        (103, "Road Rage by Non-Contact Vehicle Driver"),
        (999, "Unknown")
    ]
    crash_related_factor = models.PositiveSmallIntegerField(choices=crash_related_factor_choices, default=0)
    
    class Meta:
        db_table = "crash_related_factor"
        managed = True

class Weather(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    accident = models.ForeignKey(Accident, null=False, blank=False, on_delete = models.CASCADE)
    #c26 weather
    atmospheric_condition_choices = [
        (1, "Clear"),
        (2, "Rain"),
        (3, "Sleet or Hail"),
        (4, "Snow"),
        (5, "Fog, Smog, Smoke"),
        (6, "Severe Crosswinds"),
        (7, "Blowing Sand, Soil, Dirt"),
        (8, "Other"),
        (10, "Cloudy"),
        (11, "Blowing Snow"),
        (12, "Freezing Rain or Drizzle"),
        (98, "Not Reported"),
        (99, "Reported as Unknown"),
    ]
    atmospheric_condition = models.PositiveSmallIntegerField(choices=atmospheric_condition_choices, default=98)

    class Meta:
        db_table = "weather"
        managed = True

class VehicleRelatedFactor(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete = models.CASCADE)
    # v41 VEHICLESF
    vehicle_related_factor_choices = [
        (0, 'None Noted'),
        (29, 'Default Code Used for Vehicle Numbering'),
        (30, 'Multi-Wheeled Motorcycle Conversion'),
        (31, "Hit-and-Run Vehicle (1982-2008)"),
        (32, 'Vehicle Registration for a Person with a Disability'),
        (33, 'Vehicle Being Pushed by Non-Motorist'),
        (34, "Vehicle Impact Point-the Result of Something Set in Motion (1998-2003)"),
        (35, 'Reconstructed/Altered Vehicle'),
        (36, "Electric/Alternative Fuel Vehicle (Since 1999)"),
        (37, 'Transporting Children to/From Head Start/Day Care'),
        (38, "Vehicle Went Airborne During Crash (2001-2003)"),
        (39, 'Highway Construction, Maintenance or Utility Vehicle, In-Transport (Inside or Outside Work Zone)'),
        (40, "Highway Incident Response Vehicle(Since 2002)"),
        (41, 'Police Fire or EMS Vehicle Working at the Scene of an Emergency or Performing Other Traffic Control Activities'),
        (42, 'Other Working Vehicle (Not Construction, Maintenance, Utility, Police, Fire, or EMS Vehicle)'),
        (43, "Hazardous Materials/Cargo Released From This Vehicle (2005-2006)"),
        (44, 'Adaptive Equipment'),
        (45, 'Slide-in Camper'),
        (999, "Reported as Unknown")
    ]
    vehicle_related_factor = models.PositiveSmallIntegerField(choices=vehicle_related_factor_choices, default=0)

    class Meta:
        db_table = "vehicle_related_factor"
        managed = True

class ParkedVehicleRelatedFactor(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    parked_vehicle = models.ForeignKey(ParkedVehicle, null=False, blank = False, on_delete = models.CASCADE)
    # v41 VEHICLESF
    parked_vehicle_related_factor_choices = [
        (0, 'None Noted'),
        (29, 'Default Code Used for Vehicle Numbering'),
        (30, 'Multi-Wheeled Motorcycle Conversion'),
        (32, 'Vehicle Registration for a Person with a Disability'),
        (33, 'Vehicle Being Pushed by Non-Motorist'),
        (35, 'Reconstructed/Altered Vehicle'),
        (37, 'Transporting Children to/From Head Start/Day Care'),
        (39, 'Highway Construction, Maintenance or Utility Vehicle, In-Transport (Inside or Outside Work Zone)'),
        (41, 'Police Fire or EMS Vehicle Working at the Scene of an Emergency or Performing Other Traffic Control Activities'),
        (42, 'Other Working Vehicle (Not Construction, Maintenance, Utility, Police, Fire, or EMS Vehicle)'),
        (44, 'Adaptive Equipment'),
        (45, 'Slide-in Camper'),
        (999, "Reported as Unknown")
    ]
    parked_vehicle_related_factor  = models.PositiveSmallIntegerField(choices=parked_vehicle_related_factor_choices, default=0)

    class Meta:
        db_table = "parked_vehicle_related_factor"
        managed = True

class DriverRelatedFactor(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=False, blank = False, on_delete = models.CASCADE)
    # DRIVERRF D24
    driver_related_factor_choices = [
        (0, 'None Noted'),
        (1, "Drowsy, Sleepy, Asleep, Fatigued"),
        (2, "Ill, Passed out/Blackout"),
        (3, "Emotional (e.g., Depression, Angry, Disturbed)"),
        (4, 'Reaction to or Failure to Take Drugs/Medication'),
        (5, "Under the Influence of Alcohol, Drugs, or Medication (2003-2009)"),
        (6, 'Careless Driving, Inattentive Operation, Improper Driving, Driving Without Due Care'),
        (7, "Restricted to Wheelchair"),
        # 8 deprecated for 102,103
        (8, 'Road Rage/Aggressive Driving'),
        (10, 'Looked but Did Not See'),
        (12, 'Mother of Dead Fetus/Mother of Infant Born Post Crash'),
        (13, 'Person with an Intellectual, Cognitive, or Developmental Disability'),
        (14, "Failure to Take Drugs/Medication (1995-2004)"),
        (15, 'Seat Back Not in Normal Position, Seat Back Reclined'),
        (16, 'Police or Law Enforcement Officer'),
        (17, "Running off Road (2000-2003)"),
        (18, 'Traveling on Prohibited Trafficways'),
        (19, 'Legally Driving on Suspended or Revoked License'),
        (20, 'Leaving Vehicle Unattended With Engine Running; Leaving Vehicle Unattended in Roadway'),
        (21, 'Overloading or Improper Loading of Vehicle With Passenger or Cargo'),
        (22, 'Towing or Pushing Vehicle Improperly'),
        (23, 'Failing to Dim Lights or to Have Lights on When Required'),
        (24, 'Operating Without Required Equipment'),
        (26, 'Following Improperly'),
        (27, 'Improper or Erratic Lane Changing'),
        (28, 'Improper Lane Usage'),
        (29, 'Intentional Illegal Driving off the Roadway'),
        (30, 'Making Improper Entry to or Exit From Trafficway'),
        (31, 'Starting or Backing Improperly'),
        (32, 'Opening Vehicle Closure Into Moving Traffic or Vehicle Is in Motion'),
        (33, 'Passing Where Prohibited by Posted Signs, Pavement Markings, or School Bus Displaying Warning Not to Pass'),
        (34, 'Improper Passing Location'),
        (35, 'Passing With Insufficient Distance or Inadequate Visibility or Failing to Yield to Overtaking Vehicle'),
        (36, 'Operating the Vehicle in an Erratic, Reckless, Careless or Negligent Manner'),
        #37 deprecated in favor of 104/105
        (37, 'Police Pursuing This Driver or Police Officer in Pursuit (See Police Pursuits in Appendix C: Additional Data Element Information)'),
        (38, 'Failure to Yield Right-of-Way'),
        (39, 'Failure to Obey Actual Traffic Signs, Traffic Control Devices or Traffic Officers, Failure to Observe Safety Zone Traffic Laws'),
        (40, 'Passing Through or Around Barrier'),
        (41, 'Failure to Observe Warnings or Instructions on Vehicle Displaying Them'),
        (42, 'Failure to Signal Intentions'),
        (44, "Driving too Fast for Conditions or in Excess of Posted Speed Limit (1982-2008)"),
        (45, 'Driving Less Than Posted Maximum'),
        (46, "Racing"),
        (47, 'Making Right Turn From Left-Turn Lane or Making Left Turn From Right-Turn Lane'),
        (48, 'Making Improper Turn'),
        (49, "Failure to Comply With Physical Restrictions of License (1982-2004)"),
        (50, 'Driving Wrong Way on One-Way Trafficway'),
        (51, 'Driving on Wrong Side of Two-way Trafficway (Intentionally or Unintentionally)'),
        (52, 'Operator Inexperience'),
        (53, 'Unfamiliar With Roadway'),
        (54, 'Stopping in Roadway (Vehicle Not Abandoned)'),
        (55, 'Improper Management of Vehicle Controls'),
        (56, 'Object Interference With Vehicle Controls'),
        (57, 'Driving With Tire-Related Problems'),
        (58, 'Over Correcting'),
        (59, 'Getting off/out of a Vehicle'),
        (60, 'Alcohol and/or Drug Test Refused'),
        (61, "Rain, Snow, Fog, Smoke, Sand, Dust (1982-2008)"),
        (62, "Reflected Glare, Bright Sunlight, Headlights (1982-2008)"),
        (63, "Curve, Hill, or Other Design Features (Including Traffic Signs, Embankment 1982-2008)"),
        (64, "Building, Billboard, etc. (1982-2008)"),
        (65, "Trees, Crops, Vegetation (1982-2008)"),
        (66, "Motor Vehicle (Including Load 1982-2008)"),
        (67, "Parked Vehicle (1982-2008)"),
        (68, "Splash or Spray of Passing Vehicle (1982-2008)"),
        (69, "Inadequate Defrost or Defog System (1982-2008)"),
        (70, "Inadequate Vehicle Lighting System (1982-2008)"),
        (71, "Obstructing Angles on Vehicle (1982-2008)"),
        (72, "Mirrors - Rear View (1982-2008)"),
        (73, 'Driver Has Not Complied With Learners Permit or Intermediate Driver License Restrictions (GDL Restrictions)'),
        (74, 'Driver Has Not Complied With Physical or Other Imposed Restrictions'),
        (75, "Broken or Improperly Cleaned Windshield (1982-2008)"),
        (76, "Other Obstruction (1982-2008)"),
        (77, 'Severe Crosswind'),
        (78, 'Wind From Passing Truck'),
        (79, 'Slippery or Loose Surface'),
        (80, 'Tire Blow-Out or Flat'),
        (81, 'Debris or Objects in Road'),
        (82, 'Ruts, Holes, Bumps in Road'),
        (83, 'Live Animals in Road'),
        (84, 'Vehicle in Road'),
        (85, 'Phantom Vehicle'),
        (86, 'Pedestrian, Pedalcyclist, or Other Non-Motorist in Road'),
        (87, 'Ice, Water, Snow, Slush, Sand, Dirt, Oil, Wet Leaves on Road'),
        (88, 'Trailer Fishtailing or Swaying'),
        (89, 'Driver has a Driving Record or Driver’s License From More Than One State'),
        (90, "Hit-and-Run Vehicle Driver"),
        (91, "Non-Traffic Violation Charged (Manslaughter, Homicide, or Other Assault Offense Committed Without Malice, Since 1986)"),
        (92, "Other Non-Moving Traffic Violation (1986-2011)"),
        (93, "Cellular Telephone / Other Electronic Device"),
        (94, 'Emergency Medical Service Personnel'),
        (95, 'Fire Personnel'),
        (96, 'Tow Operator'),
        (97, 'Transportation (i.e., Maintenance Workers, Safety Service Patrol Operators, etc.)'),
        (99, "Reported as Unknown"),
        (100, "Using a Belt-Positioning Device or Other"),
        (101, "Carrying Hazardous Cargo Improperly (1994-2009)"),
        (102, "Aggressive Driving"),
        (103, "Road Rage"),
        (104, "Police Pursuing This Driver"),
        (105, "Police Officer in Pursuit"),
        (999, "Reported as Unknown")
    ]
    driver_related_factor = models.PositiveSmallIntegerField(choices=driver_related_factor_choices, default=0)

    class Meta:
        db_table = "driver_related_factor"
        managed = True

class Damage(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=True, blank= True, on_delete = models.CASCADE)
    # MDAREAS DAMAGE  V34B
    area_of_impact_choices = [
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
        (15, "No Damage"),
        (16, "Override"),
        (17, "Underride"),
        (18, "Cargo/Vehicle Parts Set-in-Motion"),
        (19, "Other Objects or Person Set-in-Motion"),
        (20, "Object Set in Motion, Unknown if Cargo/Vehicle Parts or Other"),
        (61, "Left"),
        (62, "Left-Front Side"),
        (63, "Left-Back Side"),
        (81, "Right"),
        (82, "Right-Front Side"),
        (83, "Right-Back Side"),
        (98, "Not Reported"),
        (99, "Damage Areas Unknown")
    ]

    area_of_impact = models.PositiveSmallIntegerField(choices=area_of_impact_choices, default=99)

    class Meta:
        db_table = "damage"
        managed = True


class DriverDistracted(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=False, blank = False, on_delete = models.CASCADE)
    # MDRDSTRD DRDISTRACT PC16
    distracted_by_choices = [
        (0, 'Not Distracted'),
        (1, 'Looked but Did Not See'),
        (3, 'By Other Occupant(s)'),
        (4, 'By a Moving Object in Vehicle'),
        (5, 'While Talking or Listening to Mobile Phone'),
        (6, 'While Manipulating Mobile Phone'),
        (7, 'While Adjusting Audio or Climate Controls'),
        (9, 'While Using Other Component/Controls Integral to Vehicle'),
        (10, 'While Using or Reaching for Device/Object Brought Into Vehicle'),
        (12, 'Distracted by Outside Person, Object or Event'),
        (13, 'Eating or Drinking'),
        (14, 'Smoking Related'),
        (15, 'Other Mobile Phone Related'),
        (16, 'No Driver Present/Unknown if Driver Present'),
        (17, 'Distraction/Inattention'),
        (18, 'Distraction/Careless'),
        (19, 'Careless/Inattentive'),
        (92, 'Distraction (Distracted), Details Unknown'),
        (93, 'Inattention (Inattentive), Details Unknown'),
        (96, 'Not Reported'),
        (97, 'Lost in Thought/Daydreaming'),
        (98, 'Other Distraction'),
        (99, 'Reported as Unknown if Distracted'),
    ]
    distracted_by = models.PositiveSmallIntegerField(choices=distracted_by_choices, default=99)

    class Meta:
        db_table = "driver_distracted"
        managed = True

class DriverImpaired(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=False, blank = False, on_delete = models.CASCADE)
    # DRIMPAIR D23
    driver_impaired_choices = [
        (0, 'None/Apparently Normal'),
        (1, 'Ill, Blackout'),
        (2, 'Asleep or Fatigued'),
        (3, 'Walking With a Cane or Crutches, etc.'),
        (4, 'Paraplegic or in a Wheelchair'),
        (5, 'Impaired Due to Previous Injury'),
        (6, 'Deaf/Hard of Hearing'),
        (7, 'Blind/Low Vision'),
        (8, 'Emotional (Depressed, Angry, Disturbed,'),
        (9, 'Under the Influence of Alcohol, Drugs, or'),
        (10, 'Physical Impairment - No Details'),
        (95, 'No Driver Present/Unknown if Driver'),
        (96, 'Other Physical Impairment'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown if Impaired'),
    ]
    driver_impaired = models.PositiveSmallIntegerField(choices=driver_impaired_choices, default=99)

    class Meta:
        db_table = "driver_impaired"
        managed = True


class VehicleFactor(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=False, blank = False, on_delete = models.CASCADE)
    # PC4 MFACTOR VEHICLECC
    contributing_cause_choices = [
        (0, 'None Noted'),
        (1, 'Tires'),
        (2, 'Brake System'),
        (3, 'Steering'),
        (4, 'Suspension'),
        (5, 'Power Train'),
        (6, 'Exhaust System'),
        (7, 'Head Lights'),
        (8, 'Signal Lights'),
        (9, 'Other Lights'),
        (10, 'Wipers'),
        (11, 'Wheels'),
        (12, 'Mirrors'),
        (13, 'Windows/Windshield'),
        (14, 'Body, Doors'),
        (15, 'Truck Coupling/Trailer Hitch/Safety Chains'),
        (16, 'Safety Systems'),
        (17, 'Vehicle Contributing Factors - No Details'),
        (18, "Horn"),
        (19, "Driver Seating and Control"),
        (97, 'Other'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown'),
    ]
    contributing_cause = models.PositiveSmallIntegerField(choices=contributing_cause_choices, default=99)

    class Meta:
        db_table = "vehicle_factor"
        managed = True


class Maneuver(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=False, blank = False, on_delete = models.CASCADE)
    # MDRMANAV MANEUVER PC15
    driver_maneuvered_to_avoid_choices = [
        (0, 'Driver Did Not Maneuver to Avoid'),
        (1, 'Object'),
        (2, 'Poor Road Conditions (Puddle, Ice, Pothole, etc.)'),
        (3, 'Live Animal'),
        (4, 'Contact Motor Vehicle (in This Crash)'),
        (5, 'Pedestrian, Pedalcyclist or Other Non-Motorist'),
        (92, 'Phantom/Non-Contact Motor Vehicle'),
        (95, 'No Driver Present/Unknown if Driver Present'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown'),
    ]
    driver_maneuvered_to_avoid = models.PositiveSmallIntegerField(choices=driver_maneuvered_to_avoid_choices, default=98)

    class Meta:
        db_table = "maneuver"
        managed = True


class Violation(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=False, blank = False, on_delete = models.CASCADE)
    # MVIOLATN VIOLATION D21
    moving_violation_choices = [
        (0, 'None'),
        (1, 'Manslaughter or Homicide'),
        (2, 'Willful Reckless Driving; Driving to Endanger; Negligent Driving'),
        (3, 'Unsafe Reckless (Not Willful, Wanton Reckless) Driving'),
        (4, 'Inattentive, Careless, Improper Driving, Driving Without Due Care'),
        (5, 'Fleeing or Eluding Police'),
        (6, 'Fail to Obey Police, Fireman, Authorized Person Directing Traffic'),
        (7, 'Hit-And-Run, Fail to Stop After Crash'),
        (8, 'Fail to Give Aid, Information, Wait for Police After Crash'),
        (9, 'Serious Violation Resulting in Death'),
        (10, 'Use of Telecommunications Device (Since 2015)'),
        (11, 'Driving While Intoxicated (Alcohol or Drugs) or BAC Above Limit (Any Detectable BAC for CDLs)'),
        (12, 'Driving While Impaired'),
        (13, 'Driving Under Influence of Substance Not Intended to Intoxicate'),
        (14, 'Drinking While Operating'),
        (15, 'Illegal Possession of Alcohol or Drugs'),
        (16, 'Driving With Detectable Alcohol'),
        (18, 'Refusal to Submit to Chemical Test'),
        (19, 'Alcohol, Drug or Impairment Violations Generally'),
        (21, 'Racing'),
        (22, 'Speeding (Above the Speed Limit)'),
        (23, 'Speed Greater Than Reasonable and Prudent (Not Necessarily Over the Limit)'),
        (24, 'Exceeding Special Speed Limit (for Trucks, Buses, Cycles, or on Bridge, in School Zone, etc.)'),
        (25, 'Energy Speed (Exceeding 55 mph, Non-Pointable)'),
        (26, 'Driving Too Slowly'),
        (29, 'Speed-Related Violations Generally'),
        (31, 'Fail to Stop for Red Signal'),
        (32, 'Fail to Stop for Flashing Red'),
        (33, 'Violation of Turn on Red (Fail to Stop and Yield, Yield to Pedestrians Before Turning)'),
        (34, 'Fail to Obey Flashing Signal (Yellow or Red)'),
        (35, 'Fail to Obey Signal Generally'),
        (36, 'Violate RR Grade Crossing Device/Regulations'),
        (37, 'Fail to Obey Stop Sign'),
        (38, 'Fail to Obey Yield Sign'),
        (39, 'Fail to Obey Traffic Control Device Generally'),
        (41, 'Turn in Violation of Traffic Control (Disobey Signs, Turn Arrow or Pavement Markings; This Is Not a Right-on-Red violation)'),
        (42, 'Improper Method and Position of Turn (Too Wide, Wrong Lane)'),
        (43, 'Fail to Signal for Turn or Stop'),
        (45, 'Fail to Yield to Emergency Vehicle'),
        (46, 'Fail to Yield Generally'),
        (48, 'Enter Intersection When Space Insufficient'),
        (49, 'Turn, Yield, Signaling Violations Generally'),
        (51, 'Driving Wrong Way on One-Way Road'),
        (52, 'Driving on Left, Wrong Side of Road Generally'),
        (53, 'Improper, Unsafe Passing'),
        (54, 'Pass on Right (Drive off Pavement to Pass)'),
        (55, 'Pass Stopped School Bus'),
        (56, 'Fail to Give Way When Overtaken'),
        (58, 'Following Too Closely'),
        (59, 'Wrong Side, Passing, Following Violations Generally'),
        (61, 'Unsafe or Prohibited Lane Change'),
        (62, 'Improper Use of Lane (Enter of 3-Lane Road, HOV Designated Lane)'),
        (63, 'Certain Traffic to Use Right Lane (Trucks, Slow Moving, etc.)'),
        (66, 'Motorcycle Lane Violations (More Than Two per Lane, Riding Between Lanes, etc.)'),
        (67, 'Motorcyclist Attached to Another Vehicle'),
        (69, 'Lane Violations Generally'),
        (71, 'Driving While License Withdrawn (Since 2014)'),
        (72, 'Other Driver License Violations'),
        (73, 'Commercial Driver Violations (Log Book, Hours, Permits Carried)'),
        (74, 'Vehicle Registration Violations'),
        (75, 'Fail to Carry Insurance Card'),
        (76, 'Driving Uninsured Vehicle'),
        (79, 'Non-Moving Violations Generally'),
        (81, 'Lamp Violations'),
        (82, 'Brake Violations'),
        (83, 'Failure to Require Restraint Use (by Self or Passenger)'),
        (84, 'Motorcycle Equipment Violations (Helmet, Special Equipment)'),
        (85, 'Violation of Hazardous Cargo Regulations'),
        (86, 'Size, Weight, Load Violations'),
        (89, 'Equipment Violations Generally'),
        (91, 'Parking'),
        (92, 'Theft, Unauthorized Use of Motor Vehicle'),
        (93, 'Driving Where Prohibited (Sidewalk, Limited Access, off Truck Route)'),
        (95, 'No Driver Present/Unknown if Driver Present'),
        (97, 'Not Reported'),
        (98, 'Other Moving Violation'),
        (99, 'Unknown Violations'),
    ]
    moving_violation = models.PositiveSmallIntegerField(choices=moving_violation_choices, default=0)

    class Meta:
        db_table = "violation"
        managed = True


class Vision(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, null=False, blank = False, on_delete = models.CASCADE)

    # MVISOBSC VISION PC14
    visibility_choices = [
        (0, 'No Obstruction Noted'),
        (1, 'Rain, Snow, Fog, Smoke, Sand, Dust'),
        (2, 'Reflected Glare, Bright Sunlight, Headlights'),
        (3, 'Curve, Hill, or Other Roadway Design Features'),
        (4, 'Building, Billboard, or Other Structure'),
        (5, 'Trees, Crops, Vegetation'),
        (6, 'In-Transport Motor Vehicle (Including Load)'),
        (7, 'Not In-Transport Motor Vehicle (Parked, Working)'),
        (8, 'Splash or Spray of Passing Vehicle'),
        (9, 'Inadequate Defrost or Defog System'),
        (10, 'Inadequate Vehicle Lighting System'),
        (11, 'Obstructing Interior to the Vehicle'),
        (12, 'External Mirrors'),
        (13, 'Broken or Improperly Cleaned Windshield'),
        (14, 'Obstructing Angles on Vehicle'),
        (95, 'No Driver Present/Unknown if Driver Present'),
        (97, 'Vision Obscured - No Details'),
        (98, 'Other Visual Obstruction'),
        (99, 'Reported as Unknown'),
    ]
    visibility = models.PositiveSmallIntegerField(choices=visibility_choices, default=99)

    class Meta:
        db_table = "vision"
        managed = True

# Person-related factors for all drivers are coded 00. Person-related factors for non-drivers can
# have non-zero values as listed below.
# For 1975 to 1981 values 02 to 06 correspond to 01 to 05 for the 1982 to 2009 data. Values of 20
# and higher correspond directly the same values for 1982 to 2009. 
    
class PersonRelatedFactor(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    person = models.ForeignKey(Person, null=False, blank=False, on_delete = models.CASCADE)

    # PERSONRF P24/NM26 
    person_related_factor_choices = [
        (0, 'None Noted'),
        (1, "Not Visible"),
        (2, "Darting, Running, or Stumbling Into Roadway (1995-2009)"),
        (3, "Improper Crossing or Roadway or Intersection"),
        (4, "Walking/Riding With or Against Traffic, Playing, Working, Sitting, Lying, Standing, etc., in Roadway"),
        (5, 'Interfering With Driver'),
        (6, "Ill, Passed out/Blackout (1995-2009)"),
        (7, "Emotional (e.g., Depression, Angry, Disputed)"),
        (8, 'Person with an Intellectual, Cognitive, or Developmental Disability'),
        (9, 'Construction/Maintenance/Utility Worker'),
        (10, 'Alcohol and/or Drug Test Refused'),
        (11, "Walking With Cane or Crutches"),
        (12, "Restricted to Wheelchair"),
        (13, 'Motorized Wheelchair Rider'),
        (14, "Impaired Due to Previous Injury"),
        (15, "Deaf 1982-1994"),
        (16, "Blind"),
        (17, "Other Physical Impairment"),
        (18, 'Mother of Dead Fetus/Mother of Infant Born Post-Crash'),
        (19, "Pedestrian"),
        (20, "Leaving Vehicle Unattended in Roadway (1975-1994)"),
        (21, 'Overloading or Improper Loading of Vehicle With Passengers or Cargo'),
        (22, "Towing or Pushing Vehicle Improperly (1982-2003)"),
        (23, "Failing to [Dim Lights or, Since 1995] Have Lights on When Required"),
        (24, "Operating Without Required Equipment"),
        (25, "Creating Unlawful Noise or Using Equipment Prohibited by Law (1982-2002)"),
        (26, 'Following Improperly'),
        (27, "Improper or Erratic Lane Changing"),
        (28, 'Improper Lane Usage'),
        (29, 'Intentional Illegal Driving on Road Shoulder, in Ditch, on Sidewalk, on Median'),
        (30, "Making Improper Entry to or Exit From Trafficway"),
        (31, 'Default Code Used for Vehicle Numbering'),
        (32, 'Opening Vehicle Closure Into Moving Traffic or While Vehicle Is in Motion'),
        (33, 'Passing Where Prohibited by Posted Signs, Pavement Markings, or School Bus Displaying Warning Not to Pass'),
        (34, "Passing on Wrong Side"),
        (35, "Passing With Insufficient Distance or Inadequate Visibility or Failing to Yield to Overtaking Vehicle"),
        (36, "Operating the Vehicle in Other Erratic, Reckless, Careless , or Negligent Manner (or Operating at Erratic or Suddenly Changing Speeds, 1995-2009)"),
        (37, 'Traveling on Prohibited Trafficway'),
        (38, "Failure to Yield Right-of-Way"),
        (39, "Failure to Obey Actual Traffic Signs, Traffic Control Devices or Traffic Officers; Failure to Obey Safety Zone Traffic Laws"),
        (40, 'Passing Through or Around Barrier Positioned to Prohibit or Channel Traffic'),
        (41, 'Failure to Observe Warnings or Instructions on Vehicles Displaying Them'),
        (42, 'Failure to Signal Intentions'),
        (43, "Giving Wrong Signal (1982-1996)"),
        (44, 'Driving Too Fast for Conditions or in Excess of Posted Maximum'),
        (45, 'Driving Less Than Posted Maximum'),
        (46, "Operating at Erratic or Suddenly Changing Speeds (1982-1996)"),
        (47, 'Making Right Turn From Left-Turn Lane, Left Turn From RightTurn Lane'),
        (48, "Making Other Improper Turn"),
        (49, "Driving Wrong Way on One-Way Trafficway"),
        (50, "Driving on Wrong Side of Road (Intentional or Unintentional, 1995-2009)"),
        (51, 'Operator Inexperience'),
        (52, 'Unfamiliar With Roadway'),
        (53, 'Non-Motorist Previously Used a Motor Vehicle for Motion'),
        (54, 'Non-Motorist Attempting to Use a Motor Vehicle for Motion'),
        (55, 'Non-Motorist Attempting to Use or Previously Used a Motor Vehicle for Motion, Details Not Reported'),
        (56, 'Non-Operator Flees Scene'),
        (57, 'Improper Tire Pressure'),
        (59, 'Overcorrecting'),
        (60, 'Rain, Snow, Fog, Smoke, Sand, Dust'),
        (61, 'Reflected Glare, Bright Sunlight, Headlights'),
        (62, 'Curve, Hill, or Other Design Features (Including Traffic Signs, Embankment)'),
        (63, 'Building, Billboard, Other Structures'),
        (64, 'Trees, Crops, Vegetation'),
        (65, 'Motor Vehicle (Including Load)'),
        (66, 'Parked Vehicle'),
        (67, 'Splash or Spray or Passing Vehicle'),
        (68, 'Inadequate Lighting System'),
        (69, 'Obstructing Angles on Vehicle'),
        (70, 'Mirrors'),
        (72, 'Other Visual Obstruction'),
        (73, 'Severe Crosswind'),
        (74, 'Wind From Passing Truck'),
        (75, 'Slippery or Loose Surface'),
        (76, 'Tire Blow-Out or Flat'),
        (77, 'Debris or Objects in Road'),
        (78, 'Ruts, Holes, Bumps in Road'),
        (79, "Live Animals in Road"),
        (80, 'Vehicle in Road'),
        (81, 'Phantom Vehicle'),
        (82, 'Pedestrian, Pedalcyclist, or Other Non-Motorist'),
        (83, 'Ice, Snow, Slush, Water, Sand, Dirt, Oil, Wet Leaves on Road'),
        (84, "Jaywalk (1982-1994)"),
        (85, "Jog (1982-1994)"),
        (87, 'Police or Law Enforcement Officer'),
        (88, 'Seat Back Not in Normal Upright Position, Seat Back Reclined'),
        (89, 'Parked Motor Vehicle With Equipment Extending Into the Travel Lane'),
        (90, 'Non-Motorist Pushing a Vehicle'),
        (91, 'Portable Electronic Devices'),
        (92, 'Person in Ambulance Treatment Compartment'),
        (93, 'Non-Motorist Wearing Motorcycle Helmet'),
        (94, 'Emergency Medical Services Personnel'),
        (95, 'Fire Personnel'),
        (96, 'Tow Operator'),
        (97, 'Transportation (Maintenance Workers, Safety Service Patrol Operators, etc.)'),
        (100, 'Using a Shared Micromobility Device'),
        (101, 'Obstructed Sidewalk (for this Person)'),
        (102, 'Motor Vehicle Occupant in Prior Crash'),
        (103, 'Road Rage'),
        (104, 'Using a Belt-Positioning Device or Other'),
        (105, 'Paraplegic or in a Wheelchair'),
        (999, "Reported as Unknown")
    ]
    person_related_factor = models.PositiveSmallIntegerField(choices=person_related_factor_choices, default=0)

    class Meta:
        db_table = "person_related_factor"
        managed = True


class Drugs(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

    person = models.ForeignKey(Person, null=False, blank=False, on_delete = models.CASCADE)

    # P19/NM21 DRUGSPEC
    drug_test_type_choices = [
        (0, 'Test Not Given'),
        (1, 'Whole Blood'),
        (2, 'Urine'),
        (3, 'Both Blood and Urine Tests'),
        (11, 'Blood Plasma/Serum'),
        (12, 'Blood Clot'),
        (13, 'Oral Fluids'),
        (14, 'Vitreous'),
        (15, 'Liver'),
        (96, 'Not Reported'),
        (97, 'Unknown Specimen'),
        (98, 'Other Specimen'),
        (99, 'Reported as Unknown if Tested'),
    ]
    drug_test_type = models.PositiveSmallIntegerField(choices=drug_test_type_choices, default=0)
    # P19C/NM21C  DRUGRES
    drug_test_results = models.PositiveIntegerField(null=False, blank=False)

    drug_test_method_choices = [
        (0, 'Test Not Given'),
        (1, 'Enzyme-Linked Immunosorbent Assay [ELISA]'),
        (2, 'Enzyme-Multiplied Immunoassay Technique [EMIT]'),
        (3, 'Liquid Chromatography/Tandem Mass Spectrometry [LC/MS-MS]'),
        (4, 'Headspace Gas Chromatography [HS/GC]'),
        (5, 'Liquid Chromatography/Time of Flight—Mass Spectrometry [LC/TOF-MS]'),
        (6, 'Enzyme Immunoassay [EIA]'),
        (8, 'Other Screening Test Method [Specify:]'),
        (9, 'Unknown Screening Test Method'),
        (11, 'High-Performance Liquid Chromatography [HPLC]'),
        (12, 'Liquid Chromatography/Mass Spectrometry [LC/MS]'),
        (13, 'Liquid Chromatography/Time of Flight—Mass Spectrometry [LC/TOF - MS]'),
        (14, 'Gas Chromatography and Mass Spectrometry [GC/MS]'),
        (15, 'Gas Chromatography [GC]'),
        (16, 'Liquid Chromatography/Tandem Mass Spectrometry [LC/MS-MS]'),
        (17, 'Liquid Chromatography/Time of Flight—Tandem Mass Spectrometry [LC/TOF-MS/MS]'),
        (20, 'Quadrupole Time of Flight [QTOF]'),
        (21, 'Liquid Chromatography/Quadrupole Time of Flight [LC/QTOF]'),
        (22, 'Quadrupole Time of Flight Mass Spectrometry [QTOF MS]'),
        (23, 'Gas Chromatography and Tandem Mass Spectrometry [GC/MS-MS]'),
        (24, 'Headspace Gas Chromatography [HS-GC]'),
        (25, 'Gas Chromatography With Flame Ionization Detection [GC FID]'),
        (26, 'Headspace Gas Chromatography With Flame Ionization Detection [HS-GC FID]'),
        (18, 'Other Confirmatory Test Method [Specify:]'),
        (19, 'Unknown Confirmatory Test Method'),
        (96, 'Not Reported'),
        (97, 'Unknown Testing Method'),
        (99, 'Reported as Unknown if Tested'),
    ]
    drug_test_method = models.PositiveSmallIntegerField(choices=drug_test_method_choices, null=True, blank=True)

    drug_quantity_choices = [
        (0, 'Test Not Given'),
        (1, 'None Detected/Below Threshold'),
        (2, 'Actual Drug Quantity'),
        (3, 'Presumptive Positive'),
        (4, 'Drugs Detected, Unknown Testing Method'),
        (96, 'Not Reported'),
        (97, 'Tested for Drugs, Results Unknown'),
        (98, 'Tested for Drugs, Drugs Detected, Unknown Quantity'),
        (99, 'Reported as Unknown if Tested for Drugs'),
    ]
    drug_quantity = models.PositiveSmallIntegerField(choices=drug_quantity_choices, null=True, blank=True)

    actual_drug_quantity = models.FloatField(null=True, blank=True)

    unit_of_measure_choices = [
        (1, 'mg/dL'),
        (2, 'mg/L'),
        (3, 'mcg/L'),
        (4, 'gm%'),
        (5, 'ng/mL'),
        (6, 'mcg/L'),
        (7, '%'),
        (8, 'Other [Specify:]'),
        (-9, 'Not Applicable')
    ]
    unit_of_measure = models.SmallIntegerField(choices=unit_of_measure_choices, null=True, blank=True)



    def interpret_test_result(self):
        year = self.person.accident.year
        result = self.drug_test_results
        if year < 1993:
            early_codes = {
                0: "Not Tested for Drugs",
                1: "No Drugs Reported",
                2: "Narcotic",
                3: "Depressant",
                4: "Stimulant",
                5: "Hallucinogen",
                6: "Cannabinol",
                7: "Phencyclidine (PCP)",
                8: "Inhalant",
                9: "Multiple Drugs (From Data Elements 02 to 08)",
                10: "Other Drugs (All Other Drugs Excluding Nicotine, Aspirin, Alcohol)",
                97: "Tested for Drugs, Results Unknown",
                98: "Tested for Drugs, Drugs Found, Type Unknown",
                99: "Unknown if Tested for Drugs"
            }
            return early_codes[result]
        if year < 2022:
            if result in {0}:
                return "Test Not Given"
            if result in {1}:
                return "None Detected/Below Threshold"
            if result in {95}:
                return "Not Reported"
            if result in {996}:
                return "Other Drug (Specify:)"
            if result in {997}:
                return "Tested for Drugs, Results Unknown"
            if result in {998}:
                return "Tested for Drugs, Drugs Found, Type Unknown/Positive"
            if result in {999}:
                return "Reported as Unknown if Tested for Drugs"
            if result >= 100 and result <= 295:
                return "Narcotics"
            if result >= 300 and result <= 399:
                return "Depressants"
            if result >= 400 and result <= 499:
                return "Stimulants"
            if result >= 500 and result <= 599:
                return "Hallucinogens"
            if result >= 600 and result <= 699:
                return "Cannabinoids" 
            if result >= 700 and result <= 799:
                return "Phencyclidine (PCP)"
            if result >= 800 and result <= 899:
                return "Anabolic Steroids"
            if result >= 900 and result <= 999:
                return "Inhalants"
        if result in {0}:
            return "Test Not Given"
        if result in {1}:
            return "Tested, No Drugs Found/Negative"
        if result in {9995}:
            return "Not Reported"
        if result in {9996}:
            return "Other Drug (Specify:)"
        if result in {9997}:
            return "Tested for Drugs, Results Unknown"
        if result in {9998}:
            return "Tested for Drugs, Drugs Detected, Type Unknown/Positive"
        if result in {9999}:
            return "Reported as Unknown if Tested for Drugs"
        if result >= 1001 and result <= 2000:
            return "Narcotic Analgesics"
        if result >= 2001 and result <= 3000:
            return "Depressants"
        if result >= 3001 and result <= 4000:
            return "Stimulants"
        if result >= 4001 and result <= 5000:
            return "Hallucinogens"
        if result >= 5001 and result <= 6000:
            return "Cannabinoids" 
        if result >= 6001 and result <= 7000:
            return "Dissociative Anesthetics"
        if result >= 7001 and result <= 8000:
            return "Inhalants"
        if result >= 8001 and result <= 9000:
            return "Anabolic Steroids" 
        if result >= 9001 and result <= 9994:
            return "Non-Psychoactive/Other Drugs"
        return result
        
    class Meta:
        db_table = "drugs"
        managed = True


class Race(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

    person = models.ForeignKey(Person, null=False, blank=False, on_delete = models.CASCADE)

    # SP3A RACE
    race_choices = [
        (0, 'Not a Fatality (Not Applicable)'),
        (1, 'White'),
        (2, 'Black or African American'),
        (3, 'North American Indian or Alaska Native'),
        (4, 'Chinese'),
        (5, 'Japanese'),
        (6, 'Native Hawaiian'),
        (7, 'Filipino'),
        (18, 'Asian Indian'),
        (19, 'Other Indian (Includes South and Central America, any others, except North American or Asian Indians)'),
        (28, 'Korean'),
        (38, 'Samoan'),
        (48, 'Vietnamese'),
        (58, 'Guamanian or Chamorro'),
        (68, 'Other Asian or Pacific Islander'),
        (78, 'Asian or Pacific Islander, No Specific (Individual) Race'),
        (96, 'Redacted'),
        (97, 'Multiple Races, Unspecified'),
        (98, 'Other Race'),
        (99, 'Unknown'),
    ]
    race = models.PositiveSmallIntegerField(choices=race_choices, default=0)
    # SP3AA MULTRACE
    is_multiple_races = models.BooleanField(default=False)
    # ORDER
    order = models.PositiveSmallIntegerField(null=False, blank=False, default=1)

    class Meta:
        db_table = "race"
        managed = True


class NonmotoristContributingCircumstance(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

    person = models.ForeignKey(Person, null=False, blank=False, on_delete = models.CASCADE)

    # NM14 MTM_CRSH NMCC
    nonmotorist_contributing_circumstance_choices = [
        (0, 'None Noted'),
        (1, 'Dart-out - Visual Obstruction Noted'),
        (2, 'Failure to Yield Right-Of-Way'),
        (3, 'Failure to Obey Traffic Signs, Signals or Officer'),
        (4, 'In Roadway Improperly (Standing, Lying, Working, Playing)'),
        (5, 'Entering/Exiting Parked or Stopped Vehicle'),
        (6, 'Inattentive (Talking, Eating, etc.)'),
        (7, 'Improper Turn/Merge'),
        (8, 'Improper Passing'),
        (9, 'Wrong-Way Riding or Walking'),
        (10, 'Riding on Wrong Side of Road'),
        (11, 'Dash - Run, No Visual Obstruction Noted'),
        (12, 'Improper Crossing of Roadway or Intersection (Jaywalking)'),
        (13, 'Failing to Have Lights on When Required'),
        (14, 'Operating Without Required Equipment'),
        (15, 'Improper or Erratic Lane Changing'),
        (16, 'Failure to Keep in Proper Lane or Running off Road'),
        (17, 'Making Improper Entry to or Exit From Trafficway'),
        (18, 'Operating in Other Erratic, Reckless, Careless or Negligent Manner'),
        (19, 'Not Visible (Dark Clothing, No Lighting, etc.)'),
        (20, 'Passing With Insufficient Distance or Inadequate Visibility or Failing to Yield to Overtaking Vehicle'),
        (21, 'Other'),
        (92, 'Contributing Circumstance - No Details'),
        (99, 'Reported as Unknown'),
    ]
    nonmotorist_contributing_circumstance = models.PositiveSmallIntegerField(choices=nonmotorist_contributing_circumstance_choices, default=99)

    class Meta:
        db_table = "nonmotorist_contributing_circumstance"
        managed = True


class NonmotoristDistracted(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

    person = models.ForeignKey(Person, null=False, blank=False, on_delete = models.CASCADE)

    # NM15 MNMDSTRD NMDISTRACT
    nonmotorist_distracted_by_choices = [
        (0, 'Not Distracted'),
        (2, 'By Other Non-Motorist(s)'),
        (3, 'By a Driver or Occupant of a Motor Vehicle'),
        (5, 'While Talking or Listening to Mobile Phone'),
        (6, 'While Manipulating Mobile Phone'),
        (7, 'Adjusting or Listening to Portable Audio Device (Other Than on a Mobile Phone)'),
        (8, 'Adjusting, Talking to, or Manipulating Other Portable Electronic Device'),
        (12, 'Distracted by Animal, Other Object, Event, or Activity'),
        (13, 'Eating or Drinking'),
        (14, 'Smoking Related'),
        (15, 'Other Mobile Phone Related'),
        (17, 'Distraction/Inattention'),
        (18, 'Distraction/Careless'),
        (19, 'Careless/Inattentive'),
        (92, 'Distraction (Distracted), Details Unknown'),
        (93, 'Inattention (Inattentive), Details Unknown'),
        (96, 'Not Reported'),
        (97, 'Lost in Thought/Daydreaming'),
        (98, 'Other Distraction'),
        (99, 'Reported as Unknown if Distracted'),
    ]
    nonmotorist_distracted_by = models.PositiveSmallIntegerField(choices=nonmotorist_distracted_by_choices, default=99)

    class Meta:
        db_table = "nonmotorist_distracted"
        managed = True


class NonmotoristImpaired(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

    person = models.ForeignKey(Person, null=False, blank=False, on_delete = models.CASCADE)

    #NM17 NMIMPAIR
    nonmotorist_impaired_choices = [
        (0, 'None/Apparently Normal'),
        (1, 'Ill, Blackout'),
        (2, 'Asleep or Fatigued'),
        (3, 'Walking With a Cane or Crutches'),
        (4, 'Paraplegic or in a Wheelchair'),
        (5, 'Impaired Due to Previous Injury'),
        (6, 'Deaf/Hard of Hearing'),
        (7, 'Blind/Low Vision'),
        (8, 'Emotional (Depressed, Angry, Disturbed, etc.)'),
        (9, 'Under the Influence of Alcohol, Drugs, or Medication'),
        (10, 'Physical Impairment - No Details'),
        (96, 'Other Physical Impairment'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown if Impaired'),
    ]
    nonmotorist_impaired = models.PositiveSmallIntegerField(choices=nonmotorist_impaired_choices, default=98)

    class Meta:
        db_table = "nonmotorist_impaired"
        managed = True


class NonmotoristPriorAction(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

    person = models.ForeignKey(Person, null=False, blank=False, on_delete = models.CASCADE)

    # MPR_ACT NMACTION NM13
    nonmotorist_prior_action_choices = [
        (1, 'Going to or From School [Pre-K-12]'),
        (2, 'Waiting to Cross Roadway'),
        (3, 'Crossing Roadway'),
        (4, 'Jogging/Running'),
        (5, 'Movement Along Roadway With Traffic (in or Adjacent to Travel Lane)'),
        (6, 'Movement Along Roadway Against Traffic (in or Adjacent to Travel Lane)'),
        (7, "Movement on Sidewalk"),
        (8, 'In Roadway-Other (Working, Playing, etc.)'),
        (9, 'Stationary and Adjacent to Roadway (e.g., Shoulder, Median, Sidewalk)'),
        (10, 'Working in Trafficway (Incident Response)'),
        (11, 'Entering/Exiting a Parked or Stopped Vehicle'),
        (12, 'Disabled Vehicle Related (Working on, Pushing, Leaving/Approaching)'),
        (14, 'Other'),
        (15, "None"),
        (16, 'Movement Along Roadway - Direction Unknown (Since 2012)'),
        (98, 'Not Reported'),
        (99, 'Reported as Unknown'),
    ]
    nonmotorist_prior_action = models.PositiveSmallIntegerField(choices=nonmotorist_prior_action_choices, default=98)

    class Meta:
        db_table = "nonmotorist_prior_action"
        managed = True


class SafetyEquipment(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)

    person = models.OneToOneField(Person, null=False, blank=False, on_delete = models.CASCADE)
    safety_equipment_choices = [
        (1, "No"),
        (2, "Yes"),
        (8, "Not Reported"),
        (9, "Reported as Unknown")
    ]
    # NM16A NMHELMET
    helmet = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)
    # NM16B NMPROPAD
    pads = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)
    # NM16C NMOTHPRO
    other_protective_equipment = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)
    # NM16D NMREFCLO
    reflective_equipment = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)
    # NM16E NMLIGHT
    lights = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)
    # NM16F NMOTHPRE
    other_preventative_equipment = models.PositiveSmallIntegerField(choices=safety_equipment_choices, default=8)


    class Meta:
        db_table = "safety_equipment"
        managed = True


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True) 
    accident = models.ForeignKey(Accident, on_delete=models.DO_NOTHING, null=False, blank=False)
    comment = models.TextField(null=False, blank=False)

    class Meta:
        db_table = "comment"
        managed = True

class CustomerEmail(models.Model):
    created = models.DateTimeField(auto_now_add=True) 
    email = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = "customer_email"
        managed = True


class FatalityTotals(models.Model):
    accident = models.OneToOneField(Accident, on_delete=models.DO_NOTHING)
    total_fatalities = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    vehicle_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    nonmotorist_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    # 5,10,19
    ped_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    # 6,7,8
    bike_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    
    #1
    driver_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #2
    passenger_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #3
    parked_vehicle_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #4
    nonmotorized_transport_device_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #5
    pedestrian_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #6
    bicycle_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #7
    pedalcyclist_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #8
    personal_conveyance_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    #9
    unknown_vehicle_occupant_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    # 10
    person_in_building_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    # 19
    unknown_nonmotorist_fatalities = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    class Meta:
        db_table = "fatality_totals"
        managed = True


class PodcastEpisode(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    audio_file = models.FileField(upload_to='podcasts/')
    publish_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    

class Subreddit(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

class RedditPost(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=16)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.DO_NOTHING)
    title = models.TextField(null=False, blank=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    score = models.BigIntegerField()
    url = models.TextField(null=True, blank=True)
    created_utc = models.PositiveBigIntegerField(null=False, blank=False)
    body = models.TextField(null=True, blank=True)
    def hours_ago(self):
        return round((int(time.time()) - self.created_utc)/3600, 2)

    class Meta:
        indexes = [
            models.Index(fields=["subreddit", "slug"]),
            models.Index(fields=["created_utc"]),
        ]
        unique_together = [["subreddit", "slug"]]
        managed = True

class MultiReddit(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.TextField(null=False)

    class Meta:
        db_table="multireddit"

from django.contrib.auth.models import User

class MissedConnection(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    crash_dt = models.DateTimeField(null=False, blank=False)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    location = gismodels.PointField(null=True, blank=True, geography=True)
    info = models.TextField(null=True, blank=True)
    

    def coordinates(self):
        if not self.longitude or not self.latitude:
            return [-999.9999,99.9999]
        return [self.longitude, self.latitude]
    class Meta:
        db_table="missed_connection"

class MissedConnectionComment(models.Model):
    missed_connection = models.ForeignKey(MissedConnection, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    comment = models.TextField(null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table="missed_connection_comment"