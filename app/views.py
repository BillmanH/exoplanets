from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.models import *
from app.creators.account import Account
from .creators import universe


from .forms import HomeSystemForm, SignUpForm


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
    all_count_query = "g.V().count()"
    count_accounts_query = "g.V().hasLabel('account').count()"
    time_units_query = "g.V().hasLabel('time').values('currentTime')"
    c = CosmosdbClient()
    c.add_query(all_count_query)
    c.add_query(count_accounts_query)
    c.add_query(time_units_query)
    c.run_queries()
    context = {"all_count": c.res[all_count_query], 
                "count_accounts": c.res[count_accounts_query], 
                "time": c.res[time_units_query]}
    return render(request, "app/index.html", context)


@login_required
def new_game(request):
    context = {}
    c = CosmosdbClient()
    if request.method == "GET":
        acc = Account(request.user.username, c)
        acc.sync_to_graph(c)
        context['account'] = acc.get_json()
    return render(request, "app/creation/genesis_view.html", context)


@login_required
def genesis(request):
    res = get_system(request.user.username)
    context = {"solar_system": res,
                "username": request.user.username}
    return render(request, "app/creation/genesis_view.html", context)


@login_required
def system_map(request):
    res = get_system(request.user.username)
    context = {"solar_system": res}
    return render(request, "app/system_map.html", context)

@login_required
def system_ui(request):
    res = get_system(request.user.username)
    context = {"solar_system": res}
    return render(request, "app/system_ui.html", context)


@login_required
def pop_ui_local(request):
    res = get_local_population(request.user.username)
    context = {"data": res}
    return render(request, "app/population_local.html", context)



@login_required
def galaxy_map(request):
    res = get_galaxy_nodes()
    context = {"galaxies": res}
    return render(request, "app/galaxy_map.html", context)


@login_required
def populations_view(request):
    res = get_factions(request.user.username)
    context = {"factions": res}
    return render(request, "app/populations.html", context)


