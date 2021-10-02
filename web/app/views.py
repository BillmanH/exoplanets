from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.models import *

from .creators import universe, homeworld


from .forms import HomeSystemForm, SignUpForm, QueryForm


# managing the connection (sync)
#   c = get_client()  <- Fetches the client object.
#   c.close() closes the connection afterwards, to avoid lingering connections.


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
    c = get_client()
    all_count = run_query(c, query="g.V().count()")
    count_accounts = run_query(c,query="g.V().hasLabel('account').count()")
    context = {
        "all_count": all_count,
        "count_accounts":count_accounts
    }
    c.close()
    return render(request, "app/index.html", context)


@login_required
def explore(request):
    c = get_client()
    form = QueryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form = HomeSystemForm(request.POST)
        # TODO: Add query form
        res = run_query(c, query="g.V().count()")
    context = {"node_cnt": res}
    c.close()
    return render(request, "app/index.html", context)


@login_required
def new_universe(request):
    c = get_client()
    context = {}
    form = HomeSystemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Get some info from the client
        form = HomeSystemForm(request.POST)
        username = request.user.username
        # Delete the old sytem
        account.drop_account(c, username)
        # Create the new system
        universe_nodes, universe_edges = universe.build_homeSystem(request.POST, username)
        # Create the homeworld and it's people. 
        homeworld_nodes, homeworld_edges = homeworld.build_people(request.POST)
        # Attach the people to the homeworld
        homeworld_edges = homeworld_edges + homeworld.attach_people_to_world(homeworld_nodes,universe_nodes)
        # Get the global list of objectives (prerequisite of desires)
        res = run_query(c, query="g.V().hasLabel('objective').valueMap()")
        objectives = [clean_node(n) for n in res]
        # Get the pop desire for those objectives
        homeworld_edges = homeworld_edges + homeworld.get_pop_desires([p for p in homeworld_nodes if p['label']=='pop'],objectives)
        # Upload all of that data that was created. 
        data = {"nodes": universe_nodes + homeworld_nodes, "edges": universe_edges + homeworld_edges}
        upload_data(c, username, data)
        # load the galaxy map, thus starting the game
        return redirect("system_map")
    if request.method == "GET":
        form = HomeSystemForm()
        context["form"] = form
    c.close()
    return render(request, "app/creation/new_universe.html", context)


@login_required
def system_map(request):
    c = get_client()
    res = get_system(c, request.user.username)
    context = {"solar_system": res}
    c.close()
    return render(request, "app/system_map.html", context)


@login_required
def galaxy_map(request):
    c = get_client()
    res = get_galaxy_nodes(c)
    context = {"galaxies": res}
    c.close()
    return render(request, "app/galaxy_map.html", context)
