from django.db import models

# Create your models here.

class State(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=256, null=False)

    class Meta:
        db_table = "state"
        managed = True


class County(models.Model):
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    county_id = models.PositiveIntegerField(null=False)
    name = models.CharField(max_length=512, null=False)

    class Meta:
        db_table = "county"
        managed = True



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