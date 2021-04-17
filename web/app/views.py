from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app.models import get_client, get_galaxy_nodes, get_system, run_query

from .creators import universe
from .forms import HomeSystemForm, SignUpForm

# for this app I'm including the client object as a global
# I may change this as I'm not sure of the best practice.
client = get_client()


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            returnApp = request.GET.get("next", "/")
            return redirect(returnApp)
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def index(request):
    res = run_query(client, query="g.V().count()")
    context = {"node_cnt": res}
    return render(request, "app/index.html", context)


def explore(request):
    res = run_query(client, query="g.V().count()")
    context = {"node_cnt": res}
    return render(request, "app/index.html", context)


@login_required
def new_universe(request):
    context = {}
    form = HomeSystemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form = HomeSystemForm(request.POST)
        # Create the new system
        universe.build_homeSystem(request.POST)
        # load the galaxy map, thus starting the game
        return redirect(system_map)
    if request.method == "GET":
        form = HomeSystemForm()
        context["form"] = form
    return render(request, "app/creation/new_universe.html", context)


@login_required
def system_map():
    res = get_system(client)
    context = {"galaxies": res}
    return render(request, "app/galaxy_map.html", context)


@login_required
def galaxy_map(request):
    res = get_galaxy_nodes(client)
    context = {"galaxies": res}
    return render(request, "app/galaxy_map.html", context)
