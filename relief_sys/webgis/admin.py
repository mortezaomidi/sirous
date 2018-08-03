from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin
from .models import Need

admin.site.register(Need, LeafletGeoAdmin)
