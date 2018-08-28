from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, NeedForm
from .models import Need


from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages

from chartit import DataPool, Chart
from django.db.models import Avg
from chartit import PivotDataPool, PivotChart

def home(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NeedForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            message = form.cleaned_data['location']
            form.save()
            scsess_save_message = 'your data save successfully'
            return render(request, 'webgis/index.html', {'form': form, 'scsess_save_message' : scsess_save_message})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NeedForm()

    return render(request, 'webgis/index.html', {'form': form})




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
    return render(request, 'webgis/dashboard.html')

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


def rainfall_pivot_chart_view(request):
    # Step 1: Create a PivotDataPool with the data we want to retrieve.
    rainpivotdata = PivotDataPool(
        series=[{
            'options': {
                'source': Need.objects.all(),
                'categories': ['temporary_tent'],
                'legend_by': 'location',
                'top_n_per_cat': 3,
            },
            'terms': {
                'avg_rain': Avg('carpet'),
            }
        }]
    )

    # Step 2: Create the PivotChart object
    rainpivcht = PivotChart(
        datasource=rainpivotdata,
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
                    'text': 'Month'
                }
            }
        }
    )

    # Step 3: Send the PivotChart object to the template.
    return render(request, 'webgis/dashboard.html', {'rainpivchart': rainpivcht})
