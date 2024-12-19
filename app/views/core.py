from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.models.models import *
from app.objects.account import Account
from ..creators import universe


from django.conf import settings

ms_identity_web = settings.MS_IDENTITY_WEB



def index(request):
    all_count_query = "g.V().count()"
    count_accounts_query = "g.V().hasLabel('account').count()"
    count_pops_query = "g.V().haslabel('pop').count()"
    time_units_query = "g.V().hasLabel('time').values('currentTime')"
    c = CosmosdbClient()
    c.add_query(all_count_query)
    c.add_query(count_accounts_query)
    c.add_query(count_pops_query)
    c.add_query(time_units_query)
    c.run_queries()
    stars = get_star_systems()
    context = {"all_count": c.res[all_count_query], 
                "count_accounts": c.res[count_accounts_query], 
                "time": c.res[time_units_query],
                "all_pops": c.res[count_pops_query],
                "stars": stars,
                "data": {"time":{'currentTime':c.res[time_units_query]}}
    }
    
    return render(request, "app/index.html", context)

@ms_identity_web.login_required
def token_details(request):
    return render(request, 'auth/token.html')


@ms_identity_web.login_required
def call_ms_graph(request):
    ms_identity_web.acquire_token_silently()
    graph = 'https://graph.microsoft.com/v1.0/users'
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    # trim the results down to 5 and format them.
    if 'value' in results:
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:5]

    return render(request, 'auth/call-graph.html', context=dict(results=results))

# Creates a new acount. Only done when creating a new login for the first time. 
@ms_identity_web.login_required
def new_game(request):
    context = {}
    c = CosmosdbClient()
    if request.method == "GET":
        acc = Account(request.identity_context_data._id_token_claims, c)
        acc.sync_to_graph(c)
        context['account'] = acc.get_json()
    return render(request, "app/creation/genesis_view.html", context)

# Creates a new system, using an old acount
@ms_identity_web.login_required
def genesis(request):
    c = CosmosdbClient()
    acc = Account(request.identity_context_data._id_token_claims, c)
    acc.sync_to_graph(c)
    context = {'account': acc.get_json()}
    return render(request, "app/creation/genesis_view.html", context)



@ms_identity_web.login_required
def home_system_ui(request):
    res = get_home_system(request.identity_context_data._id_token_claims['oid'])
    time = get_time()
    data = get_foreign_systems(request, res)
    if res == "No home system found":
        return redirect("genesis")
    context = {
        "data": {"time":time,
                 "solar_system": data,
                 }
    }
    return render(request, "app/system_ui.html", context)

@ms_identity_web.login_required
def system_ui(request):
    res = get_system(request.GET['objid'],request.GET['orientation'])
    time = get_time()
    data = get_foreign_systems(request, res)
    context = {
        "data": {"time":time,
                 "solar_system": data,
                 }
    }
    return render(request, "app/system_ui.html", context)


@ms_identity_web.login_required
def pop_ui_local(request):
    identity = request.identity_context_data._id_token_claims['oid']
    res = get_local_population(request.GET['objid'])
    time = get_time()
    res['time'] = time
    data = get_foreign_systems(request, res)
    context = {
        "data": data
        }
    return render(request, "app/population_local.html", context)



@ms_identity_web.login_required
def galaxy_map(request):
    res = get_star_systems()
    time = get_time()
    context = {"stars": res}
    context = {
        "data": {"time":time},
        "stars": res
        }
    return render(request, "app/galaxy_map.html", context)


