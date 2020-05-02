"""
WSGI config for Django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
path1 = 'Django'
path2 = '/app/Django'
sys.path.append(path1)
sys.path.append(path2)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django.settings')

application = get_wsgi_application()
