from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import get_client,run_query
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, HomeSystemForm
from app.models import get_client,run_query,get_galaxy_nodes

#for this app I'm including the client object as a global
# I may change this as I'm not sure of the best practice. 
client = get_client()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            returnApp = request.GET.get('next','/')
            return redirect(returnApp)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



def index(request):
    res = run_query(client,query="g.V().count()")
    context={'node_cnt':res}
    return render(request, 'app/index.html', context)


def explore(request):
    res = run_query(client,query="g.V().count()")
    context={'node_cnt':res}
    return render(request, 'app/index.html', context)

@login_required
def new_universe(request):
    res = run_query(client)
    context={'node_cnt':res}
    form = HomeSystemForm()
    context['form']=form
    return render(request, 'app/creation/new_universe.html', context)

def galaxy_map(request):
    res = get_galaxy_nodes(client)
    context={'galaxies':res}
    return render(request, 'app/galaxy_map.html', context)
