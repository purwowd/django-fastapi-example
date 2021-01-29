import os
import django
from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
apps.populate(settings.INSTALLED_APPS)
django.setup()
