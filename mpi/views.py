from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets

from mpi import models
from mpi import forms
from mpi import serializers


def index(request):
    return render(
        request,
        'mpi/index.html'
    )


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
            incident.save()
            return render(request, 'mpi/upload.html', {
                'uploaded_file_url': uploaded_file_url
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
