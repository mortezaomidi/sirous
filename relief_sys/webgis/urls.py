from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from djgeojson.views import GeoJSONLayerView
from .models import Unit, Need


from . import views

urlpatterns = [
    url('^$', views.home, name='home'),
    url('^dashboard$', views.dashboard, name='dashboard'),
    url('^signup$', views.signup, name='register'),
    url(r'^login/$',views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^panel/$',views.panel, name='panel'),
    url(r'^mcda/$',views.mcda, name='mcda'),
    url(r'^unit_data.geojson$', GeoJSONLayerView.as_view(model=Unit, properties=('name',)), name='unit_data'),
    url(r'^need_data.geojson$', GeoJSONLayerView.as_view(model=Need, properties=('water','police',)), name='need_data'),

]
