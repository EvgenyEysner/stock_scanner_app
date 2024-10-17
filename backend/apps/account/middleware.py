from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CustomAdminMiddleware(MiddlewareMixin):
    ADMIN_PATHS = {
        "/zarg-admin/": settings.ZARG_JAZZMIN_SETTINGS,
        "/energieversum-admin/": settings.ENERGIEVERSUM_JAZZMIN_SETTINGS,
        "/senec-admin/": settings.SENEC_JAZZMIN_SETTINGS,
    }

    def process_request(self, request):
        for admin_path, jazzmin_setting in self.ADMIN_PATHS.items():
            if request.path.startswith(admin_path):
                settings.JAZZMIN_SETTINGS = jazzmin_setting
                break
