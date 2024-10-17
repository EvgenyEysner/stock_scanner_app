from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView

from apps.account.admin import custom_admin_site, second_admin, core_admin, first_admin

urlpatterns = [
    path(
        "", RedirectView.as_view(pattern_name="admin:index")
    ),  # redirect to admin site
    path("zarg-admin/", core_admin.urls),
    path("energieversum-admin/", second_admin.urls),
    path("senec-admin/", first_admin.urls),
    path("admin/", custom_admin_site.urls),
    path("api/v1/", include("apps.api.urls")),
    path("app/", include("apps.warehouse.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
