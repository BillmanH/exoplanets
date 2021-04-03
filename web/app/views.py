from django.shortcuts import render
from django.http import HttpResponse
from app.models import get_client,run_query,get_galaxy_nodes

#for this app I'm including the client object as a global
# I may change this as I'm not sure of the best practice. 
client = get_client()

def index(request):
    res = run_query(client,query="g.V().count()")
    context={'node_cnt':res}
    return render(request, 'app/index.html', context)


def galaxy_map(request):
    res = get_galaxy_nodes(client)
    context={'galaxies':res}
    return render(request, 'app/galaxy_map.html', context)