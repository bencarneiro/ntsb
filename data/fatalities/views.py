from django.shortcuts import render, redirect

from django.db.models import Q, Sum, Count
from ninja import Schema, Field, FilterSchema, Query, Redoc, NinjaAPI
from django.contrib.gis.geos import GEOSGeometry
from fatalities.models import Accident, Comment, County, Person, State
from django.http import JsonResponse, HttpResponse
import json
import folium
from django.contrib.gis.geos import Point
from django.views.generic.base import RedirectView
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from data.filter_schemas import AccidentLocationFilterSchema
from django.db.models import Q
from django.contrib.gis.geoip2 import GeoIP2
from fatalities.forms import CommentForm

import csv

from django.db import connection


def three_year_moving_avg(years):
    new_list = []
    for idx in range(len(years)):
        if idx == 0:
            new_list += [round(years[idx], 2)]
        elif idx == 1:
            new_list += [ round((years[idx - 1] + years[idx]) / 2, 2) ]
        else:
            new_list += [ round((years[idx - 2] + years[idx - 1] + years[idx]) / 3, 2) ]
    return new_list



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def crashes(request):
    return render(request, "landing_page.html", context={})

def schema(request):
    return render(request, "schema.html", context={})

def leaflet(request):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        return redirect("/leaflet?lat=37.756745231&lon=-122.442857530&radius=4")
    return render(request, "leaflet.html", context={})

def testmap(request):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        ip = get_client_ip(request)
        # print(ip)
        try:
            g = GeoIP2()
            country = g.country(ip)
            if country['country_code'] != "US":
                return redirect("/testmap?lat=37.756745231&lon=-122.442857530&radius=4")
            coordinates = g.lat_lon(ip)
            return redirect(f"/testmap?lat={coordinates[0]}&lon={coordinates[1]}&radius=4")
        except Exception as e:
            print(e)
            return redirect("/testmap?lat=37.756745231&lon=-122.442857530&radius=4")
        
        
    return render(request, "leaflet.html", context={})

def nonmotorist_map(request):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        ip = get_client_ip(request)
        print(ip)
        try:
            g = GeoIP2()
            country = g.country(ip)
            if country['country_code'] != "US":
                return redirect("/nonmotorist_map?lat=37.756745231&lon=-122.442857530&radius=4")
            coordinates = g.lat_lon(ip)
            return redirect(f"/nonmotorist_map?lat={coordinates[0]}&lon={coordinates[1]}&radius=4")
        except Exception as e:
            print(e)
            return redirect("/nonmotorist_map?lat=37.756745231&lon=-122.442857530&radius=4")
        
        
    return render(request, "nonmotorist_map.html", context={})


def map(request):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        ip = get_client_ip(request)
        print(ip)
        try:
            g = GeoIP2()
            country = g.country(ip)
            if country['country_code'] != "US":
                return redirect("/map?lat=37.8011&lon=-122.3267&radius=4")
            coordinates = g.lat_lon(ip)
            return redirect(f"/map?lat={coordinates[0]}&lon={coordinates[1]}&radius=4")
        except Exception as e:
            print(e)
            return redirect("/map?lat=37.8011&lon=-122.3267&radius=4")
        
        
    return render(request, "test.html", context={})

def home(request):
    context = {
        "url": "/"
    }
    return render(request, "map.html", context)

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)



# def accidents_by_loction(request, filters: AccidentLocationFilterSchema = Query(...)):
    # if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
    #     return "Required Parameters are lat, lon, radius"
    # try:
    #     search_location = Point(x=float(request.GET['lon']), y=float(request.GET['lat']), srid=4326)
    #     radius_in_miles = float(request.GET['radius'])
    # except:
    #     return list()

    # queryset = Accident.objects.annotate(
    #     distance=Distance('location', search_location)
    # ).order_by('distance').filter(location__distance_lte=(search_location, D(mi=radius_in_miles)))
    # qe = filters.get_filter_expression()
    # q = Q()
    # for param in qe.deconstruct()[1]:
    #     if param[0] not in {'lat', 'lon', 'radius'}:
    #         q &= Q((param[0], param[1]))
    # queryset = queryset.filter(q)
    # return list(queryset)


def folium_map(request):
    # deaths = Accident.objects.filter(state_id=48, county_id__in=[48453])
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        return redirect("/map?lat=37.8011&lon=-122.3267&radius=25")
    try:
        search_location = Point(x=float(request.GET['lon']), y=float(request.GET['lat']), srid=4326)
        radius_in_miles = float(request.GET['radius'])
    except:
        return list()

    queryset = Accident.objects.annotate(
        distance=Distance('location', search_location)
    ).order_by('distance').filter(location__distance_lte=(search_location, D(mi=radius_in_miles)))
    # return list(queryset)
    if len(queryset) > 5000:
        return JsonResponse({"Error": "Try a smaller radius"})
    feature_collection = """
        { "type": "FeatureCollection",
            "features": [
    """
    for death in queryset:
        if death.latitude and death.longitude:
            feature = f"""
                {{ "type": "Feature",
                    "geometry": {{"type": "Point", "coordinates": [{death.longitude}, {death.latitude}]}},
                    "properties": {{"fatalities": "{death.fatalities}", "datetime": "{death.datetime}", "details": "{death.link()}"}}
                }},"""
            feature_collection += feature
    feature_collection = feature_collection[:-1]
    feature_collection += "]}"

    print(feature_collection)
    loady_loads = json.loads(feature_collection)
    m = folium.Map(location=[request.GET['lat'], request.GET['lon']], zoom_start=11).add_child(
        folium.ClickForMarker("<a target='_blank' href='/map?lat=${lat}&lon=${lng}&radius=25'>RELOAD MAP AT THIS POINT</a>")
    )

    popup = folium.GeoJsonPopup(
        fields=["fatalities", "datetime", "details"]
    )
    
    folium.GeoJson(loady_loads, name="geojson", popup=popup).add_to(m)
    
    m = m._repr_html_()
    context = {"map": m}
    return render(request, "map.html", context=context)
    # return JsonResponse(loady_loads, safe=False)

def accident_summary(request, **kwargs):
    a = Accident.objects.get(id=kwargs['id'])
    return render(request, "accident_details.html", {"accident": a, "form": CommentForm})


def post_comment(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        print(request)
        print(request.POST)
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data_to_save = {
                "accident_id": request.POST['accident_id'],
                "comment": request.POST['comment']
            }
            Comment.objects.create(**data_to_save)
            # redirect to a new URL:
            return redirect(f"/accidents/{request.POST['accident_id']}")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    return render(request, "name.html", {"form": form})

def county_dashboard(request, **kwargs):
    county = County.objects.get(id=kwargs['county_id'])
    return render(request, "county_dashboard.html", {"county": county})



def total_fatalities(request):
    county = County.objects.get(id=request.GET['county_id'])

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """
    #         SELECT 
    #             accident.year, 
    #             sum(accident.fatalities) as total_fatalities
    #         FROM 
    #             accident 
    #         WHERE 
    #             county_id = %s
    #         AND
    #             accident.id IN (SELECT person.accident_id FROM person WHERE person.person_type IN (6,7,8))
    #         GROUP BY 
    #             year
    #         ORDER BY
    #             year;
    #         """, 
    #         [county.id]
    #     )
    #     rows = cursor.fetchall()
    #     for row in rows:
    #         print(row)
    # return JsonResponse({})

    years = [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]

    fatalities_by_year = Accident.objects.filter(county=county).values("year").annotate(total_fatalities=Sum("fatalities")).order_by("year")

    pedestrian_accidents_list = Person.objects.filter(accident__county=county, injury_severity=4, vehicle__isnull=True, parked_vehicle__isnull=True, person_type__in=[5,10,19]).values_list("accident_id", flat=True)
    pedestrian_fatalities_qs = Accident.objects.filter(id__in=list(pedestrian_accidents_list)).values("year").annotate(pedestrian_fatalities=Sum("fatalities")).order_by("year")
    print(pedestrian_fatalities_qs)
    # print(len(pedestrian_fatalities_qs))
    bicycle_accidents_list = Person.objects.filter(accident__county=county, injury_severity=4, vehicle__isnull=True, parked_vehicle__isnull=True, person_type__in=[6,7,8]).values_list("accident_id", flat=True)
    bicycle_fatalities_qs = Accident.objects.filter(id__in=list(bicycle_accidents_list)).values("year").annotate(bicycle_fatalities=Sum("fatalities")).order_by("year")
    
    print(bicycle_fatalities_qs)
    print(fatalities_by_year)
    print(fatalities_by_year[0])
    

    # print(fatalities_by_year[0].__dict__)
    data = {"labels": years, "total": [], "vehicle_fatalities": [ ], "nonmotorist_fatalities": [] , "pedestrian_fatalities": [] , "bicycle_fatalities": []}
    for year in years:
        print(year)
        total_deaths = 0
        for f in fatalities_by_year:
            print(f)
            if f['year'] == year:
                total_deaths = f['total_fatalities']
                break
        pedestrian_deaths = 0
        for f in pedestrian_fatalities_qs:
            if f['year'] == year:
                pedestrian_deaths = f['pedestrian_fatalities']
                break
        micromobility_deaths = 0
        for f in bicycle_fatalities_qs:
            if f['year'] == year:
                micromobility_deaths = f['bicycle_fatalities']
                break
        nonmotorist_deaths = pedestrian_deaths + micromobility_deaths
        vehicle_deaths = total_deaths - nonmotorist_deaths
        data['total'] += [total_deaths]
        data['vehicle_fatalities'] += [vehicle_deaths]
        data['nonmotorist_fatalities'] += [nonmotorist_deaths]
        data['pedestrian_fatalities'] += [pedestrian_deaths]
        data['bicycle_fatalities'] += [micromobility_deaths]
    data['total_average'] = three_year_moving_avg(data['total'])
    data['vehicle_fatalities_average'] = three_year_moving_avg(data['vehicle_fatalities'])
    data['nonmotorist_fatalities_average'] = three_year_moving_avg(data['nonmotorist_fatalities'])
    data['pedestrian_fatalities_average'] = three_year_moving_avg(data['pedestrian_fatalities'])
    data['bicycle_fatalities_average'] = three_year_moving_avg(data['bicycle_fatalities'])
            






    # labels, total_fatalities = [], []
    # for year_of_fatalities in fatalities_by_year:
    #     labels += [year_of_fatalities['year']]
    #     total_fatalities += [year_of_fatalities['total_fatalities']]
    # pedestrian_fatalities, bicycle_fatalities = [], []
    # for year_of_fatalities in pedestrian_fatalities_qs:
    #     pedestrian_fatalities += [year_of_fatalities['pedestrian_fatalities']]
    # for year_of_fatalities in bicycle_fatalities_qs:
    #     bicycle_fatalities += [year_of_fatalities['bicycle_fatalities']]

    # vehicle_deaths = []
    # print(len(total_fatalities))
    # print(len(pedestrian_fatalities))
    # print(len(bicycle_fatalities))
    # for x in range(len(total_fatalities)):
    #     num_vehicle_deaths = total_fatalities[x] - pedestrian_fatalities[x] - bicycle_fatalities[x]
    #     vehicle_deaths += [num_vehicle_deaths]

    
    
    return JsonResponse(data)


def county_selector(request):
    states = State.objects.all()
    return render(request, "county_selector.html", {"states": states})

def county_table(request):
    state = State.objects.get(id=request.GET['state_id'])
    counties = County.objects.filter(state=state).order_by("name")
    return render(request, "county_table.html", {"counties": counties})

def new_map(request):
    return render(request, "new_map.html", {})

def nonmotorist(request):
    return render(request, "nonmotorist.html", {})

def vehicle(request):
    return render(request, "vehicle.html", {})

def beta(request):
    return render(request, "beta.html", {})

def info(request):
    return render(request, "info.html", {})


def total_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    year = request.GET['year']
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="total_fatalities_{year}.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])

    crashes = Accident.objects.filter(year=year)
    for crash in crashes:
        writer.writerow([crash.st_case, crash.fatalitytotals.total_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])

    return response


def vehicle_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    year = request.GET['year']
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="vehicle_fatalities_{year}.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])

    crashes = Accident.objects.filter(year=year, fatalitytotals__vehicle_fatalities__gte=1)
    for crash in crashes:
        writer.writerow([crash.st_case, crash.fatalitytotals.vehicle_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])

    return response

def nonmotorist_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    year = request.GET['year']
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="nonmotorist_fatalities_{year}.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["st_case", "fatalities", "month", "year", "day", "LATITUDE", "LONGITUDE"])

    crashes = Accident.objects.filter(year=year, fatalitytotals__nonmotorist_fatalities__gte=1)
    for crash in crashes:
        writer.writerow([crash.st_case, crash.fatalitytotals.nonmotorist_fatalities, crash.month, crash.year, crash.day, crash.latitude, crash.longitude])

    return response