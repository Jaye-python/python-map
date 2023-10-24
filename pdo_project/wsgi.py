import os

from django.core.wsgi import get_wsgi_application

env = os.environ

settings_file = 'local' if env.get('IS_LOCAL') else 'production'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdo_project.settings.' + settings_file)

application = get_wsgi_application()
