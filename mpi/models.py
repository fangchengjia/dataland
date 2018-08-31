import datetime

from django.db import models


class Incident(models.Model):
    name = models.CharField(max_length=100, default='')
    photoUrl = models.CharField(
        blank=True, max_length=500, default='')
    description = models.TextField(blank=True, default='')
    predictions = models.TextField(blank=True, default='')
    lat = models.CharField(max_length=100, default='', blank=True)
    lon = models.CharField(max_length=100, default='', blank=True)

    alert = models.BooleanField(default=False)
    zipcode = models.CharField(
        max_length=100, default='', blank=True)
    treatment = models.CharField(
        blank=True, max_length=500, default='')

    timestamp = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class Record(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, default='')
    url = models.CharField(blank=True, max_length=500, default='')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()
