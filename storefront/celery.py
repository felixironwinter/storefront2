import os
from celery import Celery
# from storefront.celery import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

celery = Celery('storefront')  #creating celery instance with the input "storefront" as the name
celery.config_from_object('django.conf:settings',namespace='CELERY') 
# go into the module djanog.conf and load the settings part, set the namespace to whatever the prefix you want for your settings see settings.py 

celery.autodiscover_tasks() 