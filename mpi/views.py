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


def alerts(request, zipcode):
    incidents = []
    for incident in models.Incident.objects.filter(zipcode=zipcode):
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
                'zipcode': incident.zipcode,
                'description': treatments[0]['description'],
                'reportNotes': 'Myrtle rust has spread to many parts of New Zealand that have a suitable climate. If you believe you have seen myrtle rust: Do not touch the plant or the rust Call MPI\'s Exotic Pest and Disease Hotline on 0800 80 99 66. Note the location and if possible, take photos, including the type of plant the suspected rust is on. Do not attempt to touch or collect samples as this may increase the spread of this disease. If you accidently come in contact with the affected plant or the rust, make sure you bag your clothing and wash clothes, bags and shoes/boots when you get home.',
                'distribution': 'This fungus is indigenous to Central and South America and the Caribbean. It also occurs in Florida. Myrtle rust was found in Hawaii in 2005, where it was initially found on ohia (Metrosideros polymorpha) a species closely related to pohutukawa and rata. It was later found on other hosts (all in the Myrtaceae family). It reached Australia in 2010, where it was initially detected on a property on the central coast of New South Wales. Since then it has spread across much of New South Wales, Queensland and Victoria. It has also been found in Tasmania and, now has spread to many parts of New Zealand that have a suitable climate.',
                'symptoms': 'Myrtle rust attacks young, soft, actively growing leaves, shoot tips and young stems. Initial symptoms are powdery, bright yellow or orange-yellow pustules on leaves, tips and stems. The developing lesions may cause a deformation of the leaves and shoots, and twig dieback if the infection is severe. Symptoms also sometimes affect flowers and fruit. Infection of highly susceptible plants may result in plant death. Myrtle rust spores can be readily dispersed by wind or on clothing, equipment etc. Both modes of dispersal can transport spores very long distances.',
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
