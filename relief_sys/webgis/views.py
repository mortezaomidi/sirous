from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.serializers import serialize
from .forms import SignUpForm, NeedForm
from .models import Need
from .mcda import ranking


from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages

from chartit import DataPool, Chart
from django.db.models import Sum
from chartit import PivotDataPool, PivotChart
from numpy import array
from .mcda import *

def home(request):
    u1004 = Need.objects.filter(unit__id=1004)
    u1005 = Need.objects.filter(unit__id=1005)
    u1020 = Need.objects.filter(unit__id=1020)
    u1024 = Need.objects.filter(unit__id=1024)
    u1031 =Need.objects.filter(unit__id=1031)

    def sum_shelter(q):
        a = 0
        for i in q:
            a += i.get_shelter()
        return a

    def sum_clothing(q):
        a = 0
        for i in q:
            a += i.get_clothing()
        return a

    def sum_bedspread(q):
        a = 0
        for i in q:
            a += i.get_bedspread()
        return a

    def sum_food(q):
        a = 0
        for i in q:
            a += i.get_food()
        return a

    def sum_emergency(q):
        a = 0
        for i in q:
            a += i.get_emergency()
        return a

    def sum_mashinary(q):
        a = 0
        for i in q:
            a += i.get_mashinary()
        return a

    l = {u1004, u1005, u1020, u1024, u1031}
    shelter = [sum_shelter(u1004), sum_shelter(u1005), sum_shelter(u1020), sum_shelter(u1024), sum_shelter(u1031)]
    cloth = [sum_clothing(u1004), sum_clothing(u1005), sum_clothing(u1020), sum_clothing(u1024), sum_clothing(u1031)]
    bedspread = [sum_bedspread(u1004), sum_bedspread(u1005), sum_bedspread(u1020), sum_bedspread(u1024), sum_bedspread(u1031)]
    food = [sum_food(u1004), sum_food(u1005), sum_food(u1020), sum_food(u1024), sum_food(u1031)]
    emergency = [sum_emergency(u1004), sum_emergency(u1005), sum_emergency(u1020), sum_emergency(u1024), sum_emergency(u1031)]
    mashinary = [sum_mashinary(u1004), sum_mashinary(u1005), sum_mashinary(u1020), sum_mashinary(u1024), sum_mashinary(u1031)]
    chart_data = {'shelter': shelter, 'cloth': cloth, 'bedspread': bedspread, 'food': food, 'emergency': emergency, 'mashinary': mashinary}

    dm = array([shelter, cloth, bedspread, food, emergency, mashinary])
    w = array([0.3, 0.3, 0.1, 0.1, 0.1, 0.1])
    rank = topsis(dm, w, 'l', 'm')
    rank = {'rank': list(rank)}


    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NeedForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            message = form.cleaned_data['geom']
            form.save()
            scsess_save_message = 'your data save successfully'
            return render(request, 'webgis/index.html', {'form': form, 'scsess_save_message' : scsess_save_message})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NeedForm()

    return render(request, 'webgis/index.html', {'form': form, 'chart_data': chart_data, 'rank': rank})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'webgis/signup.html', {'form': form})

def dashboard(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    need_data = PivotDataPool(
        series=[{
            'options': {
                'source': Need.objects.all(),
                'categories': ['temporary_tent'],
                'legend_by': 'unit',
                'top_n_per_cat': 5,
            },
            'terms': {
                'avg_rain': Sum('temporary_tent'),
            }
        }]
    )


    # Step 2: Create the PivotChart object
    cht = PivotChart(
        datasource=need_data,
        series_options=[{
            'options': {
                'type': 'column',
                'stacking': True
            },
            'terms': ['avg_rain']
        }],
        chart_options={
            'title': {
                'text': 'Rain by Month in top 3 cities'
            },
            'xAxis': {
                'title': {
                    'text': 'sum of need'
                }
            }
        }
    )



    return render(request, 'webgis/dashboard.html', {'content': cht})



def login(request):
    if request.user.is_authenticated():
        return render(request, 'webgis/panel.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'نام کاربری یا گذرواژه اشتباه است')

    return render(request, 'webgis/login.html')

def panel(request):
    if not request.user.is_authenticated():
        return redirect('login')

    return render(request, 'webgis/panel.html')



def mcda(request):
    object_list = ranking()
    return render(request, 'webgis/mcda.html', {'object_list': object_list})

#     lati = Vsoil.objects.values_list('latitude',flat=True)
# longi = Vsoil.objects.values_list('longitude',flat=True)
# ids = Vsoil.objects.values_list('id',flat=True)

# geo_json = [ {"type": "Feature",
#                     "properties": {
#                         "id":  ident,
#                         "popupContent":  "id=%s" % (ident,)
#                         },
#                     "geometry": {
#                         "type": "Point",
#                         "coordinates": [lon,lat] }}
#                     for ident,lon,lat in zip(ids,longi,lati) ]
#
#
# return render_to_response('map.html',
#                           {'geo_json': geo_json},
#                           context_instance=RequestContext(request))
# var geojsonFeature = {{ geo_json|safe }}
