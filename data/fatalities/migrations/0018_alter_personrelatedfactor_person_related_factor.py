# Generated by Django 4.1.5 on 2024-06-19 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0017_alter_nonmotoristprioraction_nonmotorist_prior_action"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personrelatedfactor",
            name="person_related_factor",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "None Noted"),
                    (1, "Not Visible"),
                    (2, "Darting, Running, or Stumbling Into Roadway (1995-2009)"),
                    (3, "Improper Crossing or Roadway or Intersection"),
                    (
                        4,
                        "Walking/Riding With or Against Traffic, Playing, Working, Sitting, Lying, Standing, etc., in Roadway",
                    ),
                    (5, "Interfering With Driver"),
                    (6, "Ill, Passed out/Blackout (1995-2009)"),
                    (7, "Emotional (e.g., Depression, Angry, Disputed)"),
                    (
                        8,
                        "Person with an Intellectual, Cognitive, or Developmental Disability",
                    ),
                    (9, "Construction/Maintenance/Utility Worker"),
                    (10, "Alcohol and/or Drug Test Refused"),
                    (11, "Walking With Cane or Crutches"),
                    (12, "Restricted to Wheelchair"),
                    (13, "Motorized Wheelchair Rider"),
                    (14, "Impaired Due to Previous Injury"),
                    (15, "Deaf 1982-1994"),
                    (16, "Blind"),
                    (17, "Other Physical Impairment"),
                    (18, "Mother of Dead Fetus/Mother of Infant Born Post-Crash"),
                    (19, "Pedestrian"),
                    (20, "Leaving Vehicle Unattended in Roadway (1975-1994)"),
                    (
                        21,
                        "Overloading or Improper Loading of Vehicle With Passengers or Cargo",
                    ),
                    (22, "Towing or Pushing Vehicle Improperly (1982-2003)"),
                    (
                        23,
                        "Failing to [Dim Lights or, Since 1995] Have Lights on When Required",
                    ),
                    (24, "Operating Without Required Equipment"),
                    (
                        25,
                        "Creating Unlawful Noise or Using Equipment Prohibited by Law (1982-2002)",
                    ),
                    (26, "Following Improperly"),
                    (27, "Improper or Erratic Lane Changing"),
                    (28, "Improper Lane Usage"),
                    (
                        29,
                        "Intentional Illegal Driving on Road Shoulder, in Ditch, on Sidewalk, on Median",
                    ),
                    (30, "Making Improper Entry to or Exit From Trafficway"),
                    (31, "Default Code Used for Vehicle Numbering"),
                    (
                        32,
                        "Opening Vehicle Closure Into Moving Traffic or While Vehicle Is in Motion",
                    ),
                    (
                        33,
                        "Passing Where Prohibited by Posted Signs, Pavement Markings, or School Bus Displaying Warning Not to Pass",
                    ),
                    (34, "Passing on Wrong Side"),
                    (
                        35,
                        "Passing With Insufficient Distance or Inadequate Visibility or Failing to Yield to Overtaking Vehicle",
                    ),
                    (
                        36,
                        "Operating the Vehicle in Other Erratic, Reckless, Careless , or Negligent Manner (or Operating at Erratic or Suddenly Changing Speeds, 1995-2009)",
                    ),
                    (37, "Traveling on Prohibited Trafficway"),
                    (38, "Failure to Yield Right-of-Way"),
                    (
                        39,
                        "Failure to Obey Actual Traffic Signs, Traffic Control Devices or Traffic Officers; Failure to Obey Safety Zone Traffic Laws",
                    ),
                    (
                        40,
                        "Passing Through or Around Barrier Positioned to Prohibit or Channel Traffic",
                    ),
                    (
                        41,
                        "Failure to Observe Warnings or Instructions on Vehicles Displaying Them",
                    ),
                    (42, "Failure to Signal Intentions"),
                    (43, "Giving Wrong Signal (1982-1996)"),
                    (
                        44,
                        "Driving Too Fast for Conditions or in Excess of Posted Maximum",
                    ),
                    (45, "Driving Less Than Posted Maximum"),
                    (
                        46,
                        "Operating at Erratic or Suddenly Changing Speeds (1982-1996)",
                    ),
                    (
                        47,
                        "Making Right Turn From Left-Turn Lane, Left Turn From RightTurn Lane",
                    ),
                    (48, "Making Other Improper Turn"),
                    (49, "Driving Wrong Way on One-Way Trafficway"),
                    (
                        50,
                        "Driving on Wrong Side of Road (Intentional or Unintentional, 1995-2009)",
                    ),
                    (51, "Operator Inexperience"),
                    (52, "Unfamiliar With Roadway"),
                    (53, "Non-Motorist Previously Used a Motor Vehicle for Motion"),
                    (54, "Non-Motorist Attempting to Use a Motor Vehicle for Motion"),
                    (
                        55,
                        "Non-Motorist Attempting to Use or Previously Used a Motor Vehicle for Motion, Details Not Reported",
                    ),
                    (56, "Non-Operator Flees Scene"),
                    (57, "Improper Tire Pressure"),
                    (59, "Overcorrecting"),
                    (60, "Rain, Snow, Fog, Smoke, Sand, Dust"),
                    (61, "Reflected Glare, Bright Sunlight, Headlights"),
                    (
                        62,
                        "Curve, Hill, or Other Design Features (Including Traffic Signs, Embankment)",
                    ),
                    (63, "Building, Billboard, Other Structures"),
                    (64, "Trees, Crops, Vegetation"),
                    (65, "Motor Vehicle (Including Load)"),
                    (66, "Parked Vehicle"),
                    (67, "Splash or Spray or Passing Vehicle"),
                    (68, "Inadequate Lighting System"),
                    (69, "Obstructing Angles on Vehicle"),
                    (70, "Mirrors"),
                    (72, "Other Visual Obstruction"),
                    (73, "Severe Crosswind"),
                    (74, "Wind From Passing Truck"),
                    (75, "Slippery or Loose Surface"),
                    (76, "Tire Blow-Out or Flat"),
                    (77, "Debris or Objects in Road"),
                    (78, "Ruts, Holes, Bumps in Road"),
                    (79, "Live Animals in Road"),
                    (80, "Vehicle in Road"),
                    (81, "Phantom Vehicle"),
                    (82, "Pedestrian, Pedalcyclist, or Other Non-Motorist"),
                    (
                        83,
                        "Ice, Snow, Slush, Water, Sand, Dirt, Oil, Wet Leaves on Road",
                    ),
                    (84, "Jaywalk (1982-1994)"),
                    (85, "Jog (1982-1994)"),
                    (87, "Police or Law Enforcement Officer"),
                    (
                        88,
                        "Seat Back Not in Normal Upright Position, Seat Back Reclined",
                    ),
                    (
                        89,
                        "Parked Motor Vehicle With Equipment Extending Into the Travel Lane",
                    ),
                    (90, "Non-Motorist Pushing a Vehicle"),
                    (91, "Portable Electronic Devices"),
                    (92, "Person in Ambulance Treatment Compartment"),
                    (93, "Non-Motorist Wearing Motorcycle Helmet"),
                    (94, "Emergency Medical Services Personnel"),
                    (95, "Fire Personnel"),
                    (96, "Tow Operator"),
                    (
                        97,
                        "Transportation (Maintenance Workers, Safety Service Patrol Operators, etc.)",
                    ),
                    (100, "Using a Shared Micromobility Device"),
                    (101, "Obstructed Sidewalk (for this Person)"),
                ],
                default=0,
            ),
        ),
    ]