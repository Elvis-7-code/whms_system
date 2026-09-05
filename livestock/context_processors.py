from .models import FarmSettings


def farm_settings(request):

    farm = FarmSettings.objects.first()

    return {
        'farm': farm,
    }