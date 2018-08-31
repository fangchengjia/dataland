import datetime

from django.db import models


class Incident(models.Model):
    name = models.CharField(max_length=100, default='')
    photoUrl = models.CharField(blank=True, max_length=500, default='')
    description = models.TextField(blank=True, default='')
    treatment = models.CharField(blank=True, max_length=500, default='')
    reviewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()
