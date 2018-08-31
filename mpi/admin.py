import requests

from django.contrib import admin
from mpi import models as mpimodels


GOOGLEMAP_KEY = 'AIzaSyC3_ZNlG2nHQViosKvhbN56hqpli22REo4'
GEOCODE_API = 'https://maps.googleapis.com/maps/api/geocode/json'
REQ_FORMAT = '{api}?key={key}'


def _payload_parser(payload_dict):
    return '&'.join(['{}={}'.format(key, value) 
        for key, value in payload_dict.items()])


def process_incident(modeladmin, request, queryset):
    for incident in queryset:
        if incident.lat != '' and incident.lon != '':
            payload = _payload_parser({
                'latlng': '40.714224,-73.961452'
            })
            rsp = requests.get(REQ_FORMAT.format(
                api=GEOCODE_API, key=GOOGLEMAP_KEY) + '&' + payload
            ).json()
            components = rsp['results'][0]['address_components']
            for component in components:
                if 'postal_code' in component['types']:
                    code = component['short_name']
                    incident.zipcode = code
                    incident.alert = True
                    incident.save()
                    break


@admin.register(mpimodels.Incident)
class Incident(admin.ModelAdmin):
    list_display = ['name', 'photoUrl', 'description', 'lat', 'lon',
        'alert', 'zipcode', 'treatment', 'timestamp']
    actions = [process_incident]


@admin.register(mpimodels.Record)
class Record(admin.ModelAdmin):
    list_display = ['name', 'description', 'url']
