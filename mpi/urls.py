from django.conf.urls import url

from mpi import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^alerts/$', views.alerts, name='alerts'),
    url(r'^upload/$', views.upload, name='upload'),
]
