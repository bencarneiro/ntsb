from django.shortcuts import render, redirect

from django.db.models import Q
from ninja import Schema, Field, FilterSchema, Query, Redoc, NinjaAPI
from django.contrib.gis.geos import GEOSGeometry
from fatalities.models import Accident
from django.http import JsonResponse
import json
import folium
from django.contrib.gis.geos import Point
from django.views.generic.base import RedirectView
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from data.filter_schemas import AccidentLocationFilterSchema
from django.db.models import Q
from django.contrib.gis.geoip2 import GeoIP2

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def crashes(request):
    return redirect("/testmap")

def schema(request):
    return render(request, "schema.html", context={})

def leaflet(request):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        return redirect("/leaflet?lat=37.8011&lon=-122.3267&radius=15")
    return render(request, "leaflet.html", context={})


def testmap(request):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        ip = get_client_ip(request)
        print(ip)
        try:
            g = GeoIP2()
            country = g.country(ip)
            if country['country_code'] != "US":
                return redirect("/testmap?lat=37.8011&lon=-122.3267&radius=15")
            coordinates = g.lat_lon(ip)
            return redirect(f"/testmap?lat={coordinates[0]}&lon={coordinates[1]}&radius=15")
        except Exception as e:
            print(e)
            return redirect("/testmap?lat=37.8011&lon=-122.3267&radius=15")
        
        
    return render(request, "leaflet.html", context={})


def test(request):
    if "lon" not in request.GET or "lat" not in request.GET or "radius" not in request.GET or not request.GET['lon'] or not request.GET['lat'] or not request.GET['radius']:
        ip = get_client_ip(request)
        print(ip)
        try:
            g = GeoIP2()
            country = g.country(ip)
            if country['country_code'] != "US":
                return redirect("/test?lat=37.8011&lon=-122.3267&radius=15")
            coordinates = g.lat_lon(ip)
            return redirect(f"/test?lat={coordinates[0]}&lon={coordinates[1]}&radius=15")
        except Exception as e:
            print(e)
            return redirect("/test?lat=37.8011&lon=-122.3267&radius=15")
        
        
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


def map(request):
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