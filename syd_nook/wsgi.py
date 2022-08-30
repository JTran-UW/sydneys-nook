"""
WSGI config for syd_nook project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syd_nook.settings')

commands = [
    "source /home/sydnpljf/virtualenv/sydnook_app/3.9/bin/activate",
    "cd /home/sydnpljf/sydnook_app/",
    "pip install -r requirements.txt",
    "python manage.py collectstatic --noinput"
]
startup = os.system(" && ".join(commands))

application = get_wsgi_application()
