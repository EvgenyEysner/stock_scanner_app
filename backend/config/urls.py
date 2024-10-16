from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.account.admin import custom_admin_site, second_admin

urlpatterns = [
    path("zarg-admin/", admin.site.urls),
    path("energieversum-admin/", second_admin.urls),
    path("admin/", custom_admin_site.urls),
    path("api/v1/", include("apps.api.urls")),
    path("app/", include("apps.warehouse.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
