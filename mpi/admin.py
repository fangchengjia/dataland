import requests
import json
import os

from django.contrib import admin
from mpi import models as mpimodels
from mpi import engine


GOOGLEMAP_KEY = 'AIzaSyC3_ZNlG2nHQViosKvhbN56hqpli22REo4'
GEOCODE_API = 'https://maps.googleapis.com/maps/api/geocode/json'
REQ_FORMAT = '{api}?key={key}'


def _payload_parser(payload_dict):
    return '&'.join(['{}={}'.format(key, value) 
        for key, value in payload_dict.items()])


def reverse_geocoding(lat, lon):
    payload = _payload_parser({'latlng': '{},{}'.format(lat, lon)})
    rsp = requests.get(REQ_FORMAT.format(
        api=GEOCODE_API, key=GOOGLEMAP_KEY) + '&' + payload
    ).json()
    if rsp['results'] == []:
        return None
    components = rsp['results'][0]['address_components']
    for component in components:
        if 'postal_code' in component['types']:
            return component['short_name']
    return None


def analyse(modeladmin, request, queryset):
    for incident in queryset:
        if incident.zipcode != '':
            incident.save()
        elif incident.lat != '' and incident.lon != '':
            code = reverse_geocoding(incident.lat, incident.lon)
            if code is not None:
                incident.zipcode = code
                incident.save()
        if incident.predictions == '':
            incident.predictions = json.dumps(
                engine.predict(incident.photoUrl.lstrip('/')))
            incident.save()


def alert(modeladmin, request, queryset):
    for incident in queryset:
        incident.alert = True
        incident.save()


@admin.register(mpimodels.Incident)
class Incident(admin.ModelAdmin):
    list_display = ['name', 'photoUrl', 'description', 'lat', 'lon',
        'alert', 'zipcode', 'treatment', 'timestamp']
    actions = [analyse, alert]


@admin.register(mpimodels.Record)
class Record(admin.ModelAdmin):
    list_display = ['name', 'description', 'url']
