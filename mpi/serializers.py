from rest_framework import serializers
from mpi import models


class IncidentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Incident
        fields = '__all__'


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Record
        fields = '__all__'

