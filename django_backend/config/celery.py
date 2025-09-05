from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo de settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Cargar la configuración de Django (celery namespace='CELERY')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto descubrir tareas en apps registradas en INSTALLED_APPS
app.autodiscover_tasks()