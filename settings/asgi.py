"""
ASGI config for settings project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import yaml

from django.core.asgi import get_asgi_application

# Get the local settings of the server
server_settings = {}
SETTINGS_FILE = (
    "SETTINGS_FILE" in os.environ
    and os.environ["SETTINGS_FILE"]
    or "/etc/django/settings-tournesol.yaml"
)
try:
    with open(SETTINGS_FILE, "r") as f:
        server_settings = yaml.full_load(f)
except FileNotFoundError:
    print("No local settings.")
    pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

application = get_asgi_application()
