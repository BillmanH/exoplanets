from django.shortcuts import render
from django.http import HttpResponse
from app.models import get_client,run_query

#for this app I'm including the client object as a global
client = get_client()

def index(request):
    res = run_query(client,query="g.V().count()")
    return HttpResponse(f"the model has {res} objects in it")