from .models import Global

def global_values(request):
    """
    Context processor for global values.
    """
    try:
        global_values = Global.objects.first()
        return {'global':global_values}
    except:
        pass

from django.conf import settings

def selected_settings(request):
    # return the version value as a dictionary
    # you may add other values here as well
    return {'APP_VERSION_NUMBER': settings.APP_VERSION_NUMBER}

