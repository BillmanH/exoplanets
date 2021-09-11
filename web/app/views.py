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

