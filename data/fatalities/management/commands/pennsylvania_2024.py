from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident, InjuryPerson, InjuryVehicle
import pandas as pd
import math
from data.settings import PENNSYLVANIA_PATH
from datetime import datetime
# array(['severe injury', 'no injury', 'killed', 'other visible injury',
#        'complaint of pain'], dtype=object)

def injury_severity_converter(severity):
    if severity == 0:
        return 0
    if severity == 4:
        return 1
    if severity == 3:
        return 2
    if severity == 2:
        return 3
    if severity == 1:
        return 4
    return 9

def get_collision_type(collision_id):
    collision_types = {
        0: "Non-collision",
        1: "Rear-end",
        2: "Head-on",
        3: "Backing",
        4: "Angle",
        5: "Sideswipe (same dir.)",
        6: "Sideswipe (Opposite dir.)",
        7: "Hit Fixed Object",
        8: "Hit Non-Motorist",
        9: "Other/Unknown (Expired)",
        98: "Other",
        99: "Unknown"
    }
    
    return collision_types.get(collision_id, "Unknown")



def get_county_name(county_id):
    counties = {
        1: "ADAMS",
        2: "ALLEGHENY",
        3: "ARMSTRONG",
        4: "BEAVER",
        5: "BEDFORD",
        6: "BERKS",
        7: "BLAIR",
        8: "BRADFORD",
        9: "BUCKS",
        10: "BUTLER",
        11: "CAMBRIA",
        12: "CAMERON",
        13: "CARBON",
        14: "CENTRE",
        15: "CHESTER",
        16: "CLARION",
        17: "CLEARFIELD",
        18: "CLINTON",
        19: "COLUMBIA",
        20: "CRAWFORD",
        21: "CUMBERLAND",
        22: "DAUPHIN",
        23: "DELAWARE",
        24: "ELK",
        25: "ERIE",
        26: "FAYETTE",
        27: "FOREST",
        28: "FRANKLIN",
        29: "FULTON",
        30: "GREENE",
        31: "HUNTINGDON",
        32: "INDIANA",
        33: "JEFFERSON",
        34: "JUNIATA",
        35: "LACKAWANNA",
        36: "LANCASTER",
        37: "LAWRENCE",
        38: "LEBANON",
        39: "LEHIGH",
        40: "LUZERNE",
        41: "LYCOMING",
        42: "MCKEAN",
        43: "MERCER",
        44: "MIFFLIN",
        45: "MONROE",
        46: "MONTGOMERY",
        47: "MONTOUR",
        48: "NORTHAMPTON",
        49: "NORTHUMBERLAND",
        50: "PERRY",
        51: "PIKE",
        52: "POTTER",
        53: "SCHUYLKILL",
        54: "SNYDER",
        55: "SOMERSET",
        56: "SULLIVAN",
        57: "SUSQUEHANNA",
        58: "TIOGA",
        59: "UNION",
        60: "VENANGO",
        61: "WARREN",
        62: "WASHINGTON",
        63: "WAYNE",
        64: "WESTMORELAND",
        65: "WYOMING",
        66: "YORK",
        67: "PHILADELPHIA"
    }
    
    return counties.get(county_id, "UNKNOWN")

def get_vehicle_make(make_code):
    vehicle_makes = {
        "AC": "A C (GREAT BRITAIN)",
        "ACAD": "ACADIAN (GM OF CANADA)",
        "ACUR": "ACURA",
        "AIH": "AMERICAN IRONHORSE",
        "ALFA": "ALFA ROMEO",
        "AMER": "AMERICAN MOTORS",
        "AMGN": "AM GENERAL",
        "AMIN": "ADVANCE MIXER",
        "APRI": "APRILIA SPA",
        "ARCA": "ARCTIC CAT (MOTORCYCLE)",
        "ARCC": "ARCTIC CAT (SNOWMOBILE)",
        "ASTO": "ASTON MARTIN",
        "ASUN": "ASUNA",
        "AUDI": "AUDI",
        "AUHE": "AUSTIN-HEALEY",
        "AUST": "AUSTIN",
        "AUTC": "AUTOCAR",
        "AVTI": "AVANTI",
        "AZUR": "AZURE DYNAMICS",
        "BEJE": "BEIJING JEEP",
        "BENT": "BENTLEY",
        "BERO": "BERTONE",
        "BESA": "BESASIE",
        "BGDG": "BIG DOG",
        "BLUB": "BLUEBIRD",
        "BMBR": "BOMBARDIER / BRP",
        "BMC": "BMC",
        "BMW": "BMW",
        "BORG": "BORGWARD",
        "BREM": "BREMEN SPORT EQUIPMENT",
        "BRIC": "BRICKLIN",
        "BROC": "BROCKWAY",
        "BRSH": "BRUSH",
        "BSA": "BSA",
        "BUEL": "BUELL",
        "BUGA": "BUGATTI",
        "BUIC": "BUICK",
        "BZEL": "B & Z ELECTRIC",
        "CADI": "CADILLAC",
        "CAGI": "CAGIVA",
        "CANA": "CAN-AM",
        "CASE": "CASE",
        "CAT": "CATERPILLAR",
        "CATE": "CATERHAM",
        "CCC": "CCC CRANE",
        "CCMH": "COUNTRY COACH",
        "CHEC": "CHECKER",
        "CHEV": "CHEVROLET",
        "CHRY": "CHRYSLER",
        "CHUC": "CHUCK BECK MOTORSPORTS",
        "CIMC": "CIMC",
        "CISI": "CISITALIA",
        "CITR": "CITROEN",
        "CLEN": "CLENET COACH WORKS",
        "CLND": "CROSS LANDER",
        "CLUB": "CLUB CAR",
        "CMPG": "CAMPAGNA",
        "COLB": "IMPERIAL",
        "COMV": "COMMUTER VEHICLES",
        "CONU": "CONSULIER",
        "CORD": "CORD",
        "CRBN": "CORBIN",
        "DAEW": "DAEWOO",
        "DAIH": "DAIHATSU",
        "DAKO": "DAKOTA",
        "DATS": "DATSUN",
        "DAYO": "DAYTONA",
        "DECO": "DECOURVILLE",
        "DEER": "JOHN DEERE",
        "DELG": "DELAGE",
        "DELO": "DELOREAN",
        "DESO": "DESOTO",
        "DETO": "DETOMASO",
        "DIAR": "DIAMOND REO",
        "DKW": "DKW",
        "DLHY": "DELAHAYE",
        "DODG": "DODGE",
        "DUCA": "DUCATI",
        "DUPL": "DUPLEX TRUCK",
        "EAGC": "EAGLE COACH",
        "EAGI": "EAGLE COACH (BUS)",
        "EAST": "EAST MANUFACTURING",
        "EDSE": "EDSEL",
        "EGIL": "EAGLE",
        "ELIO": "ELIO",
        "EMON": "E-ONE",
        "ENCR": "ENCORE",
        "ENVO": "ENVEMO",
        "ENVY": "ENVOY",
        "ERID": "E-RIDE",
        "EVNS": "EVANS",
        "EXCL": "EXCALIBUR",
        "FERR": "FERRARI",
        "FIAT": "FIAT",
        "FLYB": "FLYBO",
        "FONA": "FONTANE",
        "FORD": "FORD",
        "FRHT": "FREIGHTLINER",
        "FSKR": "FISKER",
        "FTWD": "FLEETWOOD",
        "FWD": "FWD",
        "GAZ": "GAZ",
        "GDAN": "GREAT DANE TRAILERS",
        "GENS": "GENESIS",
        "GENU": "GENUINE SCOOTERS",
        "GENZ": "GENZE",
        "GEO": "GEO",
        "GILG": "GILLIG",
        "GLAS": "GLAS",
        "GLBL": "GLOBAL ELECTRIC",
        "GM": "GENERAL MOTORS",
        "GMBH": "SETRA",
        "GMC": "GMC",
        "GRET": "GREENTECH",
        "GRUM": "GRUMMAN",
        "GWM": "KALMAR INDUSTRIES LLC",
        "GZL": "GAZELLE",
        "HAUI": "HAULMARK INDUSTRIES, INC",
        "HD": "HARLEY-DAVIDSON",
        "HEND": "HENDRICKSON",
        "HILL": "HILLMAN",
        "HINO": "HINO",
        "HOLD": "HOLDEN",
        "HOND": "HONDA",
        "HUDS": "HUDSON",
        "HUMM": "HUMMER",
        "HUSQ": "HUSQVARNA",
        "HYOS": "HYOSUNG MOTORS & MACHINERY",
        "HYTR": "HYUNDAI TRANSLEAD",
        "HYUN": "HYUNDAI",
        "ICRP": "IC BUS",
        "INDI": "INDIAN",
        "INFI": "INFINITI",
        "INTL": "INTERNATIONAL",
        "ISU": "ISUZU",
        "IVEC": "IVECO / MAGIRUS",
        "JAGU": "JAGUAR",
        "JEEP": "JEEP",
        "JENS": "JENSEN",
        "KAIS": "KAISER",
        "KAIT": "YIBEN",
        "KAWK": "KAWASAKI",
        "KIA": "KIA",
        "KTM": "KTM",
        "KUBO": "KUBOTA",
        "KVCH": "KOVATCH",
        "KW": "KENWORTH",
        "KYMC": "KYMCO",
        "LADA": "LADA",
        "LAFR": "AMERICAN LAFRANCE",
        "LAMO": "LAMBORGHINI",
        "LEXS": "LEXUS",
        "LINC": "LINCOLN",
        "LNCI": "LANCIA",
        "LNDR": "LAND ROVER",
        "LOTU": "LOTUS",
        "MACK": "MACK",
        "MACM": "MAC LTT",
        "MAHA": "MARMON HARRINGTON",
        "MAHI": "MAHINDRA",
        "MASE": "MASERATI",
        "MAYB": "MAYBACH",
        "MAZD": "MAZDA",
        "MCIN": "MCI (MOTOR COACH IND)",
        "MCKT": "MAC TRAILER MANUFACTURING",
        "MCLA": "MCLAREN",
        "MDNA": "MODERNA",
        "MELR": "BOBCAT",
        "MERC": "MERCURY",
        "MERK": "MERKUR",
        "MERZ": "MERCEDES-BENZ",
        "MESS": "MESSERSCHMITT",
        "METE": "METEOR",
        "MG": "MG",
        "MICC": "MICRO CONCEPT",
        "MIEV": "MILES ELECTRIC",
        "MIFU": "MITSUBISHI FUSO",
        "MILL": "MILLER TRAILERS",
        "MITS": "MITSUBISHI",
        "MNAC": "MONACO",
        "MNNI": "MINI COOPER",
        "MODE": "MODEL A-MODEL T",
        "MOGU": "MOTO-GUZZI",
        "MONA": "MONARCH",
        "MORG": "MORGAN",
        "MORR": "MORRIS",
        "MOSL": "MOSLER",
        "MOVT": "MOBILITY VENTURES",
        "MRCU": "MERCURY SNOWMOBILE",
        "MVAU": "MV AUGUSTA",
        "NASH": "NASH",
        "NAVI": "NAVISTAR",
        "NBLE": "NOBLE",
        "NDMC": "UD",
        "NEWH": "SPERRY NEW HOLLAND",
        "NFLY": "NEW FLYER",
        "NISS": "NISSAN",
        "NORT": "NORTON",
        "NOVB": "NOVABUS",
        "NSU": "NSU PRINZ",
        "OLDS": "OLDSMOBILE",
        "ONTR": "DAIMLERCHRYSLER COMMERCIAL BUS",
        "OPL": "OPEL",
        "OSHK": "OSHKOSH",
        "OTHR": "OTHER",
        "PACK": "PACKARD",
        "PANE": "PANTHER WESTWINDS",
        "PANZ": "PANOZ",
        "PASS": "PASSPORT",
        "PEUG": "PEUGEOT",
        "PIAG": "PIAGGIO AND VESPA",
        "PINI": "PINIFARINA",
        "PIRC": "PIERCE MANUFACTURING",
        "PLSR": "POLESTAR",
        "PLYM": "PLYMOUTH",
        "POLA": "POLAR TANK TRAILER",
        "POLS": "POLARIS",
        "PONI": "PONTIAC (CANADA)",
        "PONT": "PONTIAC",
        "POPE": "POPE",
        "PORS": "PORSCHE",
        "PREO": "PREVOST",
        "PRTA": "PROTERRA",
        "PTRB": "PETERBILT",
        "QVAL": "QVALE",
        "RAM": "RAM",
        "RAMB": "RAMBLER",
        "REIT": "REITNOUER",
        "RELA": "RELIANT",
        "RENA": "RENAULT",
        "REO": "REO 200",
        "REVO": "REVO",
        "RIVA": "RIVIAN",
        "ROAR": "ROAR MOTORCYCLES",
        "ROL": "ROLLS-ROYCE",
        "ROOT": "ROOTES",
        "ROSN": "RISSON",
        "ROV": "ROVER (BRITISH)",
        "RROV": "RANGE ROVER",
        "RUFA": "RUF AUTOMOBILES OF NA",
        "SAA": "SAAB",
        "SANG": "SANGYONG",
        "SCIO": "SCION",
        "SEAF": "SEAGRAVE",
        "SHEB": "SHELBY",
        "SIM": "SIMCA",
        "SIN": "SINGER",
        "SKOD": "SKODA",
        "SMRT": "SMART",
        "SOLE": "SOLECTRIA",
        "SPNR": "SPRINTER",
        "SPTN": "SPARTAN MOTORS",
        "SPYK": "SPYKER",
        "STRG": "STERLING",
        "STRN": "SATURN",
        "STU": "STUDEBAKER",
        "STUZ": "STUTZ",
        "SUBA": "SUBARU",
        "SUNB": "SUNBEAM",
        "SUTP": "SUTPHEN",
        "SUZI": "SUZUKI",
        "SYMG": "SYM USA/SANYANG",
        "TERX": "TEREX ADVANCE MIXER",
        "TESL": "TESLA",
        "THMS": "THOMAS BUILT",
        "THNK": "THINK",
        "TLCC": "TLC CARROSSIERS",
        "TNOM": "TANOM",
        "TOYT": "TOYOTA",
        "TRUM": "TRIUMPH",
        "TVR": "TVR",
        "UAZ": "UAZ",
        "ULTS": "ULTIMA SPORTS UNLIMITED",
        "UNKN": "UNKNOWN",
        "USEL": "US ELECTRICAR",
        "VACR": "VECTOR",
        "VAND": "VANDERHALL",
        "VANG": "VANGARD",
        "VANR": "VANGUARD TRAILER",
        "VAUX": "VAUXHALL",
        "VCTY": "VICTORY",
        "VESP": "VESPA",
        "VHPG": "VEHICLE PRODUCTION GROUP",
        "VNHL": "VAN HOOL",
        "VOLK": "VOLKSWAGEN",
        "VOLV": "VOLVO",
        "VSVC": "FREIGHTLINER (SPRINTER)",
        "WALK": "WALKER STAINLESS",
        "WANC": "WABASH",
        "WHGM": "WHITE GMC",
        "WHGO": "WHEEGO",
        "WHIT": "WHITE/AUTOCAR",
        "WINN": "WINNEBAGO",
        "WLLS": "WILLYS",
        "WRKH": "WORKHORSE",
        "WSTR": "WESTERN STAR",
        "YAMA": "YAMAHA",
        "ZAPP": "ZAP",
        "ZCZY": "YUGO",
        "ZENN": "ZENN MOTOR",
        "ZERO": "ZERO MOTORCYCLES",
        "ZMCC": "ZIMMER"
    }
    
    # Convert to uppercase for case-insensitive lookup
    return vehicle_makes.get(make_code.upper() if make_code else None)

def get_unit_type(unit_type_id):
    unit_types = {
        # Motor Vehicle Types
        1: "Automobile",
        2: "Motorcycle",
        3: "Bus",
        4: "Small truck",
        5: "Large truck",
        6: "SUV",
        7: "Van",
        8: "Autocycle",
        9: "ROV",
        10: "Snowmobile",
        11: "Farm Equipment",
        12: "Construction Equipment",
        13: "ATV",
        14: "Golf Cart",
        15: "Low Speed Vehicle",
        16: "Large Limo",
        17: "Motor Home (RV)",
        18: "Other type special vehicle",
        19: "Unknown type special vehicle",
        # Non-Motorist Types
        20: "Bicycle",
        21: "Other Pedalcycle",
        22: "Horse and buggy",
        23: "Horse and rider",
        24: "Train",
        25: "Trolley",
        31: "Pedestrian",
        32: "Wheelchair/ Mobility Device",
        33: "Skates",
        34: "Skateboard",
        35: "Self Balancing Board",
        36: "Scooter (Standing or Seated)",
        98: "Other Conveyance",
        99: "Unknown Vehicle or Conveyance"
    }
    
    return unit_types.get(unit_type_id)


def get_person_type(person_type_id):
    person_types = {
        1: "Driver",
        2: "Passenger",
        4: "Non-Motorist Operator",
        5: "Non-Motorist Occupant",
        7: "Pedestrian",
        8: "Other",
        9: "Unknown"
    }
    
    return person_types.get(person_type_id, "Unknown")


# Example usage:
print(get_person_type(1))  # Output: Driver
print(get_person_type(2))  # Output: Passenger
print(get_person_type(7))  # Output: Pedestrian
print(get_person_type(9))  # Output: Unknown
print(get_person_type(3))  # Output: None
class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        InjuryPerson.objects.filter(injury_accident__state_id=42, injury_accident__dt__year=2024).delete()
        InjuryVehicle.objects.filter(injury_accident__state_id=42, injury_accident__dt__year=2024).delete()
        InjuryAccident.objects.filter(state_id=42, dt__year=2024).delete()

        crashes_path = f"{PENNSYLVANIA_PATH}crash_2024.csv"
        roadway_path = f"{PENNSYLVANIA_PATH}roadway_2024.csv"
        vehicle_path = f"{PENNSYLVANIA_PATH}vehicle_2024.csv"
        person_path = f"{PENNSYLVANIA_PATH}person_2024.csv"
        crashes = pd.read_csv(crashes_path)
        roadways = pd.read_csv(roadway_path)
        vehicles = pd.read_csv(vehicle_path)
        persons = pd.read_csv(person_path)
        crash_list = []
        vehicle_list = []
        person_list = []
        for x in crashes.index:
            crash_roadways = roadways[roadways['CRN'] == crashes['CRN'][x]].reset_index()
            if len(crash_roadways == 0):
                street_1, street_2 = None, None
            elif len(crash_roadways) == 1:
                street_1, street_2 = crash_roadways['STREET_NAME'][0], None
            else:
                street_1, street_2 = crash_roadways['STREET_NAME'][0], crash_roadways['STREET_NAME'][1]
            crash_vehicles = vehicles[vehicles['CRN'] == crashes['CRN'][x]]
            crash_persons = persons[persons['CRN'] == crashes['CRN'][x]]
            print(x)
            year = 2024
            month = crashes['CRASH_MONTH'][x]
            if month < 1 or month > 12 or pd.isnull(month):
                month = "01"
            month = str(month).zfill(2)
            time = crashes['ARRIVAL_TM'][x]
            if pd.isnull(time):
                print("That time is null")
                time = "00:00:00"
            else:
                hours = str(math.floor(int(time)/100)).zfill(2)
                minutes = str(int(time) % 100).zfill(2)
                time = f"{hours}:{minutes}:00"
            
            timestamp = datetime.strptime(f"{year}-{month}-01T{time}", "%Y-%m-%dT%H:%M:%S")
            new_crash = InjuryAccident(
                state_id=42,
                state_accident_id = crashes['CRN'][x],
                dt = timestamp,
                latitude = crashes['DEC_LATITUDE'][x],
                longitude = crashes['DEC_LONGITUDE'][x],
                county = get_county_name(crashes['COUNTY'][x]),
                street_1 = street_1,
                street_2 = street_2,
                crash_type = get_collision_type(crashes['COLLISION_TYPE'][x]),
                death_count = crashes['FATAL_COUNT'][x],
                severe_injury_count = crashes['SUSP_SERIOUS_INJ_COUNT'][x]
            )
            crash_list += [new_crash]
            veh_dict = {}
            for y in crash_vehicles.index:
                veh_num = int(crash_vehicles['UNIT_NUM'][y]),
                make = get_vehicle_make(crash_vehicles['MAKE_CD'][y]),
                body_type = get_unit_type(crash_vehicles['UNIT_TYPE'][y])
                hit_and_run = False
                if int(crash_vehicles['DVR_PRES_IND'][y]) in {3, 4}:
                    hit_and_run = True
                new_vehicle = InjuryVehicle(
                    injury_accident=new_crash,
                    vehicle_number=veh_num,
                    make=make,
                    body_type=body_type,
                    hit_and_run=hit_and_run
                )
                vehicle_list += [new_vehicle]
                veh_dict[veh_num] = new_vehicle
            for z in crash_persons.index:
                print(veh_dict)
                new_person = InjuryPerson(
                    injury_accident=new_crash,
                    injury_vehicle=veh_dict[int(crash_persons['UNIT_NUM'][z])],
                    age = crash_persons['AGE'][z],
                    sex = crash_persons['SEX'][z],
                    injury_severity = injury_severity_converter(crash_persons['INJ_SEVERITY'][z]),
                    person_type = get_person_type(crash_persons['PERSON_TYPE'][z])
                )
                person_list += [new_person]
        InjuryAccident.objects.bulk_create(crash_list)
        InjuryVehicle.objects.bulk_create(vehicle_list)
        InjuryPerson.objects.bulk_create(person_list)



# class InjuryAccident(models.Model):
#     id = models.AutoField(primary_key=True)
#     state = models.ForeignKey(State, on_delete= models.DO_NOTHING)
#     state_accident_id = models.DecimalField(max_digits=20, decimal_places=0)
#     dt = models.DateTimeField(null=False, blank=False)
#     latitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
#     longitude = models.DecimalField(null=True, blank=True, decimal_places=7, max_digits=10)
#     city = models.TextField(null=True, blank=True)
#     county = models.TextField(null=True, blank=True)
#     street_1 = models.TextField(null=True)
#     street_2 = models.TextField(null=True)
#     crash_type = models.TextField(null=True, blank=True)
#     death_count = models.PositiveSmallIntegerField(null=True, blank=True)
#     severe_injury_count = models.PositiveSmallIntegerField(null=True, blank=True)
#     def map_link(self):
#         return f"<a href='https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}'>({self.latitude}, {self.longitude})</a>"

# class InjuryVehicle(models.Model):
#     injury_accident = models.ForeignKey(InjuryAccident, on_delete=models.CASCADE)
#     vehicle_number = models.PositiveSmallIntegerField(null=False, blank=False)
#     make = models.TextField(null=True, blank=True)
#     model = models.TextField(null=True, blank=True)
#     body_type = models.TextField(null=True, blank=True)
#     violation = models.TextField(null=True, blank=True)
#     hit_and_run = models.BooleanField(default=False)

# class InjuryPerson(models.Model):
#     injury_accident = models.ForeignKey(InjuryAccident, on_delete=models.CASCADE)
#     injury_vehicle = models.ForeignKey(InjuryVehicle, null=True, blank=True, on_delete = models.CASCADE)
#     age = models.PositiveSmallIntegerField(null = True, blank = True)
#     #p6 
#     sex = models.CharField(max_length=64, null=True, blank=True)
#     person_type = models.CharField(max_length=256,null=True, blank=True)
#     #p8 injury_severity
#     injury_severity_choices = [
#         (0, 'No Apparent Injury (O)'),
#         (1, 'Possible Injury (C)'),
#         (2, 'Suspected Minor Injury (B)'),
#         (3, 'Suspected Serious Injury (A)'),
#         (4, 'Fatal Injury (K)'),
#         (5, 'Injured, Severity Unknown (U) (Since 1978)'),
#         (6, 'Died Prior to Crash'),
#         (9, 'Unknown/Not Reported')
#     ]			
#     injury_severity = models.PositiveSmallIntegerField(choices=injury_severity_choices, default=9)