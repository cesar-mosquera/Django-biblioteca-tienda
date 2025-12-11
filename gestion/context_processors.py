from django.conf import settings

def project_settings(request):
    return {
        'TITLE': getattr(settings, 'TITLE', 'Biblioteca'),
    }
