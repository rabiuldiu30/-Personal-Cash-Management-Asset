import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Name_ID_ManageCash.settings')

application = get_wsgi_application()
