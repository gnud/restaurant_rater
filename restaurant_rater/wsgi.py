"""
WSGI config for restaurant_rater project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_rater.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.environ.get('APP_STATIC_DIR', 'static'))
application.add_files('docs', 'docs')
