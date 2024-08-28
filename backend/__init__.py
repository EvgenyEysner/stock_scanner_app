from .config.celery import app as celery_app
from .config.settings import CELERY_RETRY_DELAY, CELERY_RETRY_MAX_TIMES

# This will make sure the app is always imported when Django starts so that shared_task will use this app.
__all__ = ("celery_app", CELERY_RETRY_DELAY, CELERY_RETRY_MAX_TIMES)
