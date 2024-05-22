from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from fatalities.models import Accident
from django.http import JsonResponse
import json
import folium

def crashes(request):
    deaths = Accident.objects.filter(state_id=48, county__county_id__in=[453,491, 209, 51, 53,21])

    feature_collection = """
        { "type": "FeatureCollection",
            "features": [
    """
    for death in deaths:
        if death.latitude and death.longitude:
            feature = f"""
                {{ "type": "Feature",
                    "geometry": {{"type": "Point", "coordinates": [{death.longitude}, {death.latitude}]}},
                    "properties": {{"fatalities": "{death.fatalities}"}}
                }},"""
            feature_collection += feature
    feature_collection = feature_collection[:-1]
    feature_collection += "]}"

    print(feature_collection)
    loady_loads = json.loads(feature_collection)
    m = folium.Map(location=[30.297370913553245, -97.7313631855747], zoom_start=12)
    folium.GeoJson(loady_loads, name="geojson", tooltip="").add_to(m)
    
    m = m._repr_html_()
    context = {"map": m}
    return render(request, "map.html", context=context)
    # return JsonResponse(loady_loads, safe=False)