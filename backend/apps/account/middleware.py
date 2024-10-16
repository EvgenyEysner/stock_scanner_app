from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CustomAdminMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/zarg-admin/"):
            settings.JAZZMIN_SETTINGS = settings.ZARG_JAZZMIN_SETTINGS
        elif request.path.startswith("/energieversum-admin/"):
            settings.JAZZMIN_SETTINGS = settings.ENERGIEVERSUM_JAZZMIN_SETTINGS
        else:
            settings.JAZZMIN_SETTINGS = settings.JAZZMIN_SETTINGS
