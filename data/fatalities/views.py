from django.shortcuts import render, redirect

from django.db.models import Q, Sum, Count, Min
from ninja import Schema, Field, FilterSchema, Query, Redoc, NinjaAPI
from django.contrib.gis.geos import GEOSGeometry
from fatalities.models import Accident, Comment, County, PedestrianType, Person, State, Vehicle
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
from fatalities.forms import CommentForm, EmailForm

from PIL import Image, ImageDraw, ImageFont
import time

import qrcode
from io import BytesIO

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
    return redirect("beta")
    # return render(request, "landing_page.html", context={})

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


def connection(request, **kwargs):
    
    a = MissedConnection.objects.get(id=kwargs['id'])
    return render(request, "connection.html", {"connection": a, "form": CommentForm})


def post_missed_connection_comment(request):
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
                "missed_connection_id": request.POST['connection_id'],
                "comment": request.POST['comment']
            }
            MissedConnectionComment.objects.create(**data_to_save)
            # redirect to a new URL:
            return redirect(f"/connection/{request.POST['connection_id']}")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    return render(request, "name.html", {"form": form})



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


def collect_email(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        print(request)
        print(request.POST)
        # create a form instance and populate it with data from the request:
        form = EmailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data_to_save = {
                "email": request.POST['email']
            }
            CustomerEmail.objects.create(**data_to_save)
            # redirect to a new URL:
            return redirect(f"/info?success=True#email")
    
    return redirect(f"/info#email")

    # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = EmailForm()

    # return render(request, "name.html", {"form": form})



def county_dashboard(request, **kwargs):
    county = County.objects.get(id=kwargs['county_id'])
    return render(request, "county_dashboard.html", {"county": county})



def total_fatalities(request):
    county = County.objects.get(id=request.GET['county_id'])

    years = [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]

    fatalities_by_year = Accident.objects.filter(county=county).values("year").annotate(total_fatalities=Sum("fatalities")).order_by("year")
    pedestrian_accidents_list = Person.objects.filter(accident__county=county, injury_severity=4, vehicle__isnull=True, parked_vehicle__isnull=True, person_type__in=[5,10,19]).values_list("accident_id", flat=True)
    pedestrian_fatalities_qs = Accident.objects.filter(id__in=list(pedestrian_accidents_list)).values("year").annotate(pedestrian_fatalities=Sum("fatalities")).order_by("year")
    bicycle_accidents_list = Person.objects.filter(accident__county=county, injury_severity=4, vehicle__isnull=True, parked_vehicle__isnull=True, person_type__in=[6,7,8]).values_list("accident_id", flat=True)
    bicycle_fatalities_qs = Accident.objects.filter(id__in=list(bicycle_accidents_list)).values("year").annotate(bicycle_fatalities=Sum("fatalities")).order_by("year")
    list_of_cars_which_hit_people = Person.objects.filter(accident__county=county, person_type__in=[5,6,7,8,10,19], injury_severity=4).values_list("vehicle_which_struck_non_motorist__id", flat=True)
    
    

    data = {"labels": years, "total": [], "vehicle_fatalities": [ ], "nonmotorist_fatalities": [] , "pedestrian_fatalities": [] , "bicycle_fatalities": []}
    
    functional_system_data = []
    total_lanes_data = []
    body_type_data = []
    for year in years:
        total_deaths = 0
        for f in fatalities_by_year:
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


        fatalities_by_num_lanes = Accident.objects.filter(county=county, year=year).values('functional_system').annotate(fatalities=Sum("fatalities")).order_by("functional_system")
        # print(fatalities_by_num_lanes)
        this_years_data = {"x": year, "99": 0}
        for f in fatalities_by_num_lanes:
            # grouping three categories into "other"
            if f['functional_system'] in {"96","98", "99"}:
                this_years_data["99"] += f['fatalities']
            else:
                this_years_data[f['functional_system']] = f['fatalities']
        functional_system_data += [this_years_data]


        deaths_by_lanes_in_roadway = Vehicle.objects.filter(accident__year=year, id__in=list_of_cars_which_hit_people).values("total_lanes_in_roadway").annotate(fatalities=Sum("accident__fatalities")).order_by("total_lanes_in_roadway")
        # print(fatalities_by_num_lanes)
        this_years_data = {"x": year}
        for f in deaths_by_lanes_in_roadway:
            this_years_data[f['total_lanes_in_roadway']] = f['fatalities']
        total_lanes_data += [this_years_data]


        deaths_by_body_type = Vehicle.objects.filter(accident__year=year, id__in=list_of_cars_which_hit_people).values("body_type").annotate(fatalities=Sum("accident__fatalities")).order_by("body_type")
        # print(fatalities_by_num_lanes)
        this_years_data = {"x": year}
        for f in deaths_by_body_type:
            this_years_data[f['body_type']] = f['fatalities']
        body_type_data += [this_years_data]



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
    data['functional_system_data'] = functional_system_data
    data['total_lanes_data'] = total_lanes_data
    data['body_type_data'] = body_type_data
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


def pedestrian_safety(request):
    
    years = [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]

    context = {
        "pedestrian_death_labels": years, 
        "pedestrian_death_counts": [], 
        "bicycle_death_counts": [], 
        "pedestrian_crash_type_labels": [], 
        "pedestrian_crash_type_counts": [],
        "pedestrian_crash_group_labels": [], 
        "pedestrian_crash_group_counts": [],
        "pedestrian_position_labels": [], 
        "pedestrian_position_counts": [],
        "pedestrian_location_labels": [], 
        "pedestrian_location_counts": [],
        "bicycle_crash_type_labels": [], 
        "bicycle_crash_type_counts": [],
        "bicycle_crash_group_labels": [], 
        "bicycle_crash_group_counts": [],
        "bicycle_position_labels": [], 
        "bicycle_position_counts": [],
        "bicycle_location_labels": [], 
        "bicycle_location_counts": []}
   
    fatalities_by_year = Person.objects.filter(injury_severity=4, person_type__in=[5,10,19]).values("accident__year").annotate(total_fatalities=Count("id")).order_by("accident__year")
    for year in years: 
        total_deaths = 0
        for f in fatalities_by_year:
            if f['accident__year'] == year:
                total_deaths = f['total_fatalities']
                break
        context['pedestrian_death_counts'] += [total_deaths]


    fatalities_by_year = Person.objects.filter(injury_severity=4, person_type__in=[6,7,8]).values("accident__year").annotate(total_fatalities=Count("id")).order_by("accident__year")
    for year in years: 
        total_deaths = 0
        for f in fatalities_by_year:
            if f['accident__year'] == year:
                total_deaths = f['total_fatalities']
                break
        context['bicycle_death_counts'] += [total_deaths]


    positions = Person.objects.filter(accident__year__gte=2014, person_type__in=[5]).values("pedestriantype__pedestrian_position").annotate(total=Count("id"))
    for p in positions:
        # print(p)
        q = PedestrianType.objects.filter(pedestrian_position=p['pedestriantype__pedestrian_position'])[0].get_pedestrian_position_display()
        # print(type(q))
        # print(q)
        context['pedestrian_position_labels'] += [q]
        context['pedestrian_position_counts'] += [p['total']]


    positions = Person.objects.filter(accident__year__gte=2014, person_type__in=[5]).values("pedestriantype__pedestrian_location").annotate(total=Count("id"))
    for p in positions:
        # print(p)
        q = PedestrianType.objects.filter(pedestrian_location=p['pedestriantype__pedestrian_location'])[0].get_pedestrian_location_display()
        # print(type(q))
        # print(q)
        context['pedestrian_location_labels'] += [q]
        context['pedestrian_location_counts'] += [p['total']]

    crash_types = Person.objects.filter(accident__year__gte=2014, person_type__in=[5]).values("pedestriantype__pedestrian_crash_type").annotate(total=Count("id"))
    for p in crash_types:
        # print(p)
        q = PedestrianType.objects.filter(pedestrian_crash_type=p['pedestriantype__pedestrian_crash_type'])[0].get_pedestrian_crash_type_display()
        # print(type(q))
        # print(q)
        context['pedestrian_crash_type_labels'] += [q]
        context['pedestrian_crash_type_counts'] += [p['total']]


    crash_groups = Person.objects.filter(accident__year__gte=2014, person_type__in=[5]).values("pedestriantype__pedestrian_crash_group").annotate(total=Count("id"))
    for p in crash_groups:
        # print(p)
        q = PedestrianType.objects.filter(pedestrian_crash_group=p['pedestriantype__pedestrian_crash_group'])[0].get_pedestrian_crash_group_display()
        # print(type(q))
        # print(q)
        context['pedestrian_crash_group_labels'] += [q]
        context['pedestrian_crash_group_counts'] += [p['total']]

    positions = Person.objects.filter(accident__year__gte=2014, person_type__in=[6,7]).values("pedestriantype__bicycle_position").annotate(total=Count("id"))
    for p in positions:
        # print(p)
        q = PedestrianType.objects.filter(bicycle_position=p['pedestriantype__bicycle_position'])[0].get_bicycle_position_display()
        # print(type(q))
        # print(q)
        context['bicycle_position_labels'] += [q]
        context['bicycle_position_counts'] += [p['total']]


    positions = Person.objects.filter(accident__year__gte=2014, person_type__in=[6,7]).values("pedestriantype__bicycle_location").annotate(total=Count("id"))
    for p in positions:
        # print(p)
        q = PedestrianType.objects.filter(bicycle_location=p['pedestriantype__bicycle_location'])[0].get_bicycle_location_display()
        # print(type(q))
        # print(q)
        context['bicycle_location_labels'] += [q]
        context['bicycle_location_counts'] += [p['total']]

    crash_types = Person.objects.filter(accident__year__gte=2014, person_type__in=[6,7]).values("pedestriantype__bicycle_crash_type").annotate(total=Count("id"))
    for p in crash_types:
        # print(p)
        q = PedestrianType.objects.filter(bicycle_crash_type=p['pedestriantype__bicycle_crash_type'])[0].get_bicycle_crash_type_display()
        # print(type(q))
        # print(q)
        context['bicycle_crash_type_labels'] += [q]
        context['bicycle_crash_type_counts'] += [p['total']]


    context['pedestrian_death_average'] = three_year_moving_avg(context['pedestrian_death_counts'])
    
    context['bicycle_death_average'] = three_year_moving_avg(context['bicycle_death_counts'])

    return render(request, "pedestrian_safety.html", context)

def vehicle(request):
    return render(request, "vehicle.html", {})

def beta(request):
    return render(request, "beta.html", {})

def info(request):
    if "success" in request.GET:
        return render(request, "info.html", {"form": EmailForm, "success_message": "You have been added to our newsletter"})
    
    return render(request, "info.html", {"form": EmailForm, "success_message": ""})


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

def comments(request):
    comments = Comment.objects.all().order_by("-created")
    return render(request, "comment_moderation.html", {"comments": comments})

from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import CustomerEmail, MissedConnection, MissedConnectionComment, PodcastEpisode, RedditPost  # Assume you have a model for episodes

from django.utils import feedgenerator

class PodcastFeedGenerator(feedgenerator.Rss201rev2Feed):

    def root_attributes(self):
        attrs = super().root_attributes()
        attrs["xmlns:itunes"] = "http://www.itunes.com/dtds/podcast-1.0.dtd"
        return attrs
    
    def add_root_elements(self, handler):
        super(PodcastFeedGenerator, self).add_root_elements(handler)
        #image

        handler.addQuickElement(u'itunes:image href="https://roadway.report/static/podcast.jpg"', '',{}) 
        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", u"https://roadway.report/static/podcast.jpg")
        handler.addQuickElement(u"title", u"Are You Into Bus Stuff?")
        handler.addQuickElement(u"link", u"https://roadway.report/podcast")
        handler.endElement(u'image') 
        handler.startElement(u'itunes:owner', {})
        handler.addQuickElement(u"itunes:name", u"roadway.report")
        handler.addQuickElement(u"itunes:email", u"ben@roadway.report")
        handler.endElement(u"itunes:owner")
        handler.addQuickElement(u"copywright", u'All Rights Reserved',{})  
        #itunes image 
        #itunes categories
        handler.addQuickElement(u"itunes:subtitle", u"A Podcast by roadway.report")
        handler.startElement(u'itunes:category text="News"', {})
        handler.addQuickElement(u'itunes:category text="Politics"', u"")
        handler.endElement(u'itunes:category') 
        handler.addQuickElement(u'itunes:category text="Comedy"', u"")
        #itunes explicit
        handler.addQuickElement(u"itunes:explicit", 'true',{})  
        handler.addQuickElement(u"itunes:author", 'roadway.report',{})  
        handler.addQuickElement(u"itunes:type", 'episodic',{}) 



#   <itunes:category text="Society &amp; Culture">
#     <itunes:category text="Documentary" />
#   </itunes:category>

class PodcastFeed(Feed):
    feed_type = PodcastFeedGenerator
    title = "Are You Into Bus Stuff?"
    link = "/podcast"
    description = "The ONLY comedy podcast about traffic deaths --- Hosted by Ben Carneiro of roadway.report and Lucas Reilly of Blurbanist"
    language="en"

    def items(self):
        # Fetch the latest episodes from your model
        return PodcastEpisode.objects.order_by("-publish_date")  # Get the 10 most recent episodes

    def item_title(self, item):
        return item.title  # Title of the episode

    def item_description(self, item):
        return item.description  # Description of the episode

    def item_link(self, item):
        # Link to the episode's page
        return reverse('episode_detail', args=[item.slug])

    def item_enclosure_url(self, item):
        # URL to the actual audio file
        return "https://roadway.report/podcasts/" + item.slug + ".mp3"  # Ensure this is a file path or URL

    def item_enclosure_length(self, item):
        # Size of the file in bytes
        return item.audio_file.size  # Return file size in bytes

    def item_enclosure_mime_type(self, item):
        return 'audio/mpeg'  # Set MIME type for the podcast audio
    
    def item_pubdate(self, item):
        return item.publish_date

    # def root_attributes(self):
    #     attrs = super().root_attributes()
    #     attrs["xmlns:itunes"] = "http://www.itunes.com/dtds/podcast-1.0.dtd"
    #     return attrs
    
    # def add_root_elements(self, handler):
    #     super().add_root_elements(handler)
    #     handler.addQuickElement("itunes:explicit", "clean")
    

def episode_detail(request, **kwargs):
    episode = PodcastEpisode.objects.get(slug=kwargs['slug'])
    return render(request, "episode_detail.html", {"episode": episode})

def episodes(request, **kwargs):
    episodes = PodcastEpisode.objects.all().order_by("-publish_date")
    return render(request, "podcast_list.html", {"episodes": episodes})

def privacy(request):
    return render(request, "privacy.html", {})

def texas(request):
    return render(request, "texas.html", {})

def missed_connections(request):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        ip = get_client_ip(request)
        # print(ip)
        try:
            g = GeoIP2()
            country = g.country(ip)
            if country['country_code'] != "US":
                return redirect("/missed_connections?lat=37.756745231&lon=-122.442857530&radius=4")
            coordinates = g.lat_lon(ip)
            return redirect(f"/missed_connections?lat={coordinates[0]}&lon={coordinates[1]}&radius=4")
        except Exception as e:
            print(e)
            return redirect("/missed_connections?lat=37.756745231&lon=-122.442857530&radius=4")
        
    return render(request, "missed_connections.html", {})

def create_missed_connection(request):
    print(request)
    print(request.POST)
    data_to_save = {
        "latitude": request.POST['latitude'],
        "longitude": request.POST['longitude'],
        "crash_dt": request.POST['crash_dt'],
        "info": request.POST['info']
        }
    print(data_to_save)
    MissedConnection.objects.create(**data_to_save)
    # redirect to a new URL:
    # return redirect(f"/connections/{request.POST['accident_id']}")
    return redirect("/missed_connections")

def population(request):
    return render(request, "population.html", {})

def population_nonmotorist(request):
    return render(request, "population_nonmotorist.html", {})

def newsletter_intake(request):
    return render()


def reddit(request):
    posts = RedditPost.objects.filter(created_utc__gt=round(time.time() - 1209600)).order_by("-created_utc")[:2500]
    return render(request, "reddit.html", {"posts": posts})

def gooner_army(request):
    return redirect("https://ko-fi.com/roadwayreport")


def someone_died_here(request):
    # Get the link from the query parameters
    crash_id = request.GET.get('id', None)
    title = "Someone Died Here"
    try:
        crash_id = int(crash_id)
    except:
        return redirect("https://roadway.report")
    
    link = "https://roadway.report/accidents/" + str(crash_id) + "/"
    footer = "roadway.report"
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=50,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    qr_img = qr.make_image(fill='black', back_color='white')
    qr_img = qr_img.convert('RGB')


    # Define heights for the title and footer
    title_height = 350  # Space for the title
    footer_height = 350  # Space for the footer
    img_width, img_height = qr_img.size

    # Create a blank image with space for the title and footer
    combined_img = Image.new(
        'RGB',
        (img_width, img_height + title_height + footer_height),
        'white'
    )

    # Add the title to the image
    draw = ImageDraw.Draw(combined_img)

    # Use a custom font for the title and footer
    try:
        # Replace 'arial.ttf' with the path to your font file
        font = ImageFont.truetype("arial.ttf", size=200)  # Increase size as needed
    except IOError:
        # Fallback to default font if custom font is not available
        font = ImageFont.load_default()

    # Draw the title
    title_text_width = draw.textlength(title, font=font)
    title_text_height = 200
    title_position = (
        (img_width - title_text_width) // 2,  # Center horizontally
        (title_height - title_text_height) // 2  # Center vertically
    )
    draw.text(title_position, title, fill='black', font=font)

    # Paste the QR code below the title
    combined_img.paste(qr_img, box=(0, title_height,img_width,title_height + img_height), mask=None)

    # Draw the footer
    footer_text_width = draw.textlength(footer, font=font)
    footer_text_height = 200
    footer_position = (
        (img_width - footer_text_width) // 2,  # Center horizontally
        title_height + img_height + (footer_height - footer_text_height) // 2  # Position below QR code
    )
    draw.text(footer_position, footer, fill='black', font=font)

    # Save the combined image to a BytesIO object
    buffer = BytesIO()
    combined_img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the image as a response
    return HttpResponse(buffer, content_type="image/png")