from django.shortcuts import render, redirect
from django.contrib.gis.geos import GEOSGeometry
from fatalities.models import Accident
from django.http import JsonResponse
# import json
# import folium
from django.views.generic.base import RedirectView


def crashes(request):
    return redirect("/v1/docs")


favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
    # deaths = Accident.objects.filter(state_id=48, county_id__in=[48453])

    # feature_collection = """
    #     { "type": "FeatureCollection",
    #         "features": [
    # """
    # for death in deaths:
    #     if death.latitude and death.longitude:
    #         feature = f"""
    #             {{ "type": "Feature",
    #                 "geometry": {{"type": "Point", "coordinates": [{death.longitude}, {death.latitude}]}},
    #                 "properties": {{"fatalities": "{death.fatalities}", "datetime": "{death.datetime}"}}
    #             }},"""
    #         feature_collection += feature
    # feature_collection = feature_collection[:-1]
    # feature_collection += "]}"

    # print(feature_collection)
    # loady_loads = json.loads(feature_collection)
    # m = folium.Map(location=[30.297370913553245, -97.7313631855747], zoom_start=12)
    # tooltip = folium.GeoJsonTooltip(
    #     fields=["fatalities", "datetime"],
    #     # aliases=["State:", "2015 Median Income(USD):", "Median % Change:"],
    #     # localize=True,
    #     # sticky=False,
    #     # labels=True,
    #     # style="""
    #     #     background-color: #F0EFEF;
    #     #     border: 2px solid black;
    #     #     border-radius: 3px;
    #     #     box-shadow: 3px;
    #     # """,
    #     # max_width=800,
    # )
    # folium.GeoJson(loady_loads, name="geojson", tooltip=tooltip).add_to(m)
    
    # m = m._repr_html_()
    # context = {"map": m}
    # return render(request, "map.html", context=context)
    # # return JsonResponse(loady_loads, safe=False)