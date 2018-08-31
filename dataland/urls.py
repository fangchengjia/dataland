from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from mpi import views as mpi_views


schema_view = get_schema_view(title='Bio No Shock API')
admin.autodiscover()

router = DefaultRouter()
router.register(r'mpi', mpi_views.IncidentViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mpi/', include('mpi.urls')),
    url(r'^api/v1/', include(router.urls)),
]


urlpatterns += static(settings.STATIC_URL,
	document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
	document_root=settings.MEDIA_ROOT)
