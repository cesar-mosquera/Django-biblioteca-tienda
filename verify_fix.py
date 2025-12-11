import os
import django
from django.conf import settings
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

# Verify settings.TITLE
print(f"Settings TITLE: {getattr(settings, 'TITLE', 'NOT FOUND')}")

# Verify Template Rendering
from django.template.loader import get_template

factory = RequestFactory()
request = factory.get('/')

try:
    template = get_template('home.html')
    # views.py passes {'t': 'Hola Mundo'}
    rendered = template.render({'t': 'Hola Mundo'}, request)
    
    if "Biblioteca" in rendered:
        print("SUCCESS: 'Biblioteca' found in rendered template.")
    else:
        print("FAILURE: 'Biblioteca' NOT found in rendered template.")
        print("Snippet:", rendered[:200])

except Exception as e:
    print(f"ERROR: {e}")
