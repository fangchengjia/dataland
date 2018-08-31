from django.contrib import admin
from mpi import models as mpimodels


@admin.register(mpimodels.Incident)
class Incident(admin.ModelAdmin):
    list_display = ['name', 'photoUrl', 'description', 'lat', 'lon',
    	'treatment', 'reviewed', 'timestamp']


@admin.register(mpimodels.Record)
class Record(admin.ModelAdmin):
    list_display = ['name', 'description', 'url']
