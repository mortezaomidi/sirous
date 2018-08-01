from django.db import models

from django.contrib.gis.db import models

class Need(models.Model):
    location = models.PointField()
    #define shelter needs
    temporary_tent = models.PositiveSmallIntegerField(blank=True, null=True)
    permanent_tent = models.PositiveSmallIntegerField(blank=True, null=True)
    conex = models.PositiveSmallIntegerField(blank=True, null=True)

    # define clothing needs
    men_pants = models.PositiveSmallIntegerField(blank=True, null=True)
    women_pants = models.PositiveSmallIntegerField(blank=True, null=True)
    child_pants = models.PositiveSmallIntegerField(blank=True, null=True)
    men_shirt = models.PositiveSmallIntegerField(blank=True, null=True)
    women_shirt = models.PositiveSmallIntegerField(blank=True, null=True)
    men_shoes = models.PositiveSmallIntegerField(blank=True, null=True)
    women_shoes = models.PositiveSmallIntegerField(blank=True, null=True)
    child_shoes = models.PositiveSmallIntegerField(blank=True, null=True)
    child_pants = models.PositiveSmallIntegerField(blank=True, null=True)

    # define Flooring and bedspread
    carpet = models.PositiveSmallIntegerField(blank=True, null=True)
    blanket = models.PositiveSmallIntegerField(blank=True, null=True)

    # define food and drink
    water = models.PositiveSmallIntegerField(blank=True, null=True)
    canned_food = models.PositiveSmallIntegerField(blank=True, null=True)
    compote_and_juice = models.PositiveSmallIntegerField(blank=True, null=True)

    #define emergency services
    helicopter = models.PositiveSmallIntegerField(blank=True, null=True)
    ambulance = models.PositiveSmallIntegerField(blank=True, null=True)
    firefighter = models.PositiveSmallIntegerField(blank=True, null=True)
    doctor = models.PositiveSmallIntegerField(blank=True, null=True)
    nurse = models.PositiveSmallIntegerField(blank=True, null=True)
    police = models.PositiveSmallIntegerField(blank=True, null=True)
    voluntry_manpower = models.PositiveSmallIntegerField(blank=True, null=True)

    #define mashinary needs
    crane = models.PositiveSmallIntegerField(blank=True, null=True)
    excavator = models.PositiveSmallIntegerField(blank=True, null=True)
    bulldozer = models.PositiveSmallIntegerField(blank=True, null=True)
    truck = models.PositiveSmallIntegerField(blank=True, null=True)
    grinder = models.PositiveSmallIntegerField(blank=True, null=True)
    electric_hammer = models.PositiveSmallIntegerField(blank=True, null=True)
    electrik_driller = models.PositiveSmallIntegerField(blank=True, null=True)
    welding_engine = models.PositiveSmallIntegerField(blank=True, null=True)
    gas_welding = models.PositiveSmallIntegerField(blank=True, null=True)
    shovel = models.PositiveSmallIntegerField(blank=True, null=True)
    pocket = models.PositiveSmallIntegerField(blank=True, null=True)
    hammer = models.PositiveSmallIntegerField(blank=True, null=True)
    
