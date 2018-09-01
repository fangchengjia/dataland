from django.conf.urls import url

from mpi import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^incidents/$', views.incidents, name='incidents'),
    url(r'^incident/(?P<incident_id>[0-9]+)/$', views.incident, name='incident'),
    url(r'^alerts/(?P<zipcode>[0-9]+)/$', views.alerts, name='alerts'),
    url(r'^upload/$', views.upload, name='upload'),
]
