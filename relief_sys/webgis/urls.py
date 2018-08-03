from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    url('^$', views.home, name='home'),
    url('^dashboard$', views.rainfall_pivot_chart_view, name='dashboard'),
    url('^signup$', views.signup, name='register'),
    url(r'^login/$',views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^panel/$',views.panel, name='panel'),

]
