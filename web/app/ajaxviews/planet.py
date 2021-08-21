from django.contrib.auth.models import User
from django.http import JsonResponse

def get_planet(request):
    request = request.GET
    data = {'valid':'true'}
    return JsonResponse(data)