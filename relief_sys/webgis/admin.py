from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin
from .models import Need, Unit

admin.site.register(Need, LeafletGeoAdmin)
admin.site.register(Unit, LeafletGeoAdmin)
