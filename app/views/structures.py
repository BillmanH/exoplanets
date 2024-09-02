from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from django.conf import settings
ms_identity_web = settings.MS_IDENTITY_WEB

from ..functions import configurations
from ..models.models import get_object_by_id

@ms_identity_web.login_required
def new_structure(request):
    buildings = configurations.get_building_configurations()
    faction = get_object_by_id(request.GET['factionid'])
    pop = get_object_by_id(request.GET['popid'])
    context = {"buildings": buildings,"faction":faction, "pop":pop}
    return render(request, "app/population_local.html", context)