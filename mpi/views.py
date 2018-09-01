import json

from django import http
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from mpi import engine


from mpi import models
from mpi import forms
from mpi import serializers
from mpi.admin import reverse_geocoding


def index(request):
    return render(
        request,
        'mpi/index.html'
    )


def incidents(request):
    incidents = []
    for incident in models.Incident.objects.all():
        treatments = []
        if incident.treatment != '':
            for match_id in json.loads(incident.treatment):
                record = models.Record.objects.get(id=match_id)
                treatments.append({
                    'name': record.name,
                    'description': record.description,
                    'url': record.url,
                })
            incidents.append({
                'id': incident.id,
                'name': incident.name,
                'photoUrl': incident.photoUrl,
                'lat': incident.lat,
                'lon': incident.lon,
                'zipcode': incident.zipcode,
                'predictions': incident.predictions,
                'treatments': treatments,
                'timestamp': incident.timestamp
            })
    return http.JsonResponse({
        'incidents': incidents
    })


def incident(request, incident_id):
    incident_detail = ''
    incident = models.Incident.objects.get(id=incident_id)
    treatments = []
    if incident.treatment != '':
        for match_id in json.loads(incident.treatment):
            record = models.Record.objects.get(id=match_id)
            treatments.append({
                'name': record.name,
                'description': record.description,
                'url': record.url,
            })
        incident_detail = {
            'id': incident.id,
            'name': incident.name,
            'photoUrl': incident.photoUrl,
            'lat': incident.lat,
            'lon': incident.lon,
            'zipcode': incident.zipcode,
            'probability': incident.predictions,
            'description': treatments[0]['description'],
            'timestamp': incident.timestamp
        }
    return http.JsonResponse(incident_detail)


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['name']
            description = request.POST['description']
            photo = request.FILES['photo']
            lat = request.POST['lat']
            lon = request.POST['lon']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            uploaded_file_url = fs.url(filename)
            incident = models.Incident(
                name=name,
                photoUrl=uploaded_file_url,
                description=description,
                lat=lat,
                lon=lon)
            if incident.lat != '' and incident.lon != '':
                code = reverse_geocoding(lat, lon)
                if code is not None:
                    incident.zipcode = code
            incident.save()
            predictions = engine.predict(
                incident.photoUrl.lstrip('/'))
            most_likely_name = predictions[0]['label'].replace('_', ' ')
            incident.predictions = predictions[0]['probability']
            matches = []
            for match in models.Record.objects.filter(
                    name__icontains=most_likely_name):
                matches.append(match.id)
            incident.treatment = json.dumps(matches)
            incident.save()
            return http.JsonResponse({
                'name': incident.name,
                'photoUrl': uploaded_file_url,
                'predictions': predictions
            })
    form = forms.UploadFileForm()
    return render(request, 'mpi/upload.html', {'form': form})


def upload2(request):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            photo = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            uploaded_file_url = fs.url(filename)
            with open('media/reglist.csv') as infile:
                for line in infile.readlines():
                    name, description, url = line.split('|')
                    models.Record(
                        name=name,
                        description=description,
                        url=url.strip('\n')).save()
            return render(request, 'mpi/upload.html', {
                'uploaded_file_url': ''
            })
    form = forms.UploadFileForm()
    return render(request, 'mpi/upload.html', {'form': form})


class IncidentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Incident.objects.all()
    serializer_class = serializers.IncidentSerializer


class RecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer
