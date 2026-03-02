import os
import sys

# Path to the folder that contains your 'manage.py' file
project_home = u'/home/thesoyelife/getover.api'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set the environment variable to point to your settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'getover_api.settings'

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()