from django import http
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt


from mpi import models
from mpi import forms
from mpi import serializers
from mpi.admin import reverse_geocoding


def index(request):
    return render(
        request,
        'mpi/index.html'
    )


def alerts(request):
    alerts = []
    for incident in models.Incident.objects.filter(alert=True):
        alerts.append({
            'name': incident.name,
            'photoUrl': incident.photoUrl,
            'description': incident.description,
            'zipcode': incident.zipcode,
            'treatment': incident.treatment,
            'timestamp': incident.timestamp
        })
    return http.JsonResponse({
        'alerts': alerts
    })


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
            return http.JsonResponse({
                'name': uploaded_file_url
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
