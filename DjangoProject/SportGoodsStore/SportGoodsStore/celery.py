import os
from celery import Celery

# задать стандартный модуль настроек Django
#  для программы 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SportGoodsStore.settings')
app = Celery('SportGoodsStore')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()