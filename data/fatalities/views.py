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

def crashes(request):
    return redirect("/v1/docs")

def schema(request):
    return render(request, "schema.html", context={})

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