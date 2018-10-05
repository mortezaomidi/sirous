from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist


class Unit(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	center = models.CharField(max_length=50, blank=True, null=True)
	county = models.CharField(max_length=50, blank=True, null=True)
	bakhsh = models.CharField(max_length=50, blank=True, null=True)
	province = models.CharField(max_length=50, blank=True, null=True)
	geom = models.MultiPolygonField(srid=4326, blank=True, null=True)

	def __str__(self):
		if self.name:
			return "%s--مرکز: %s--شهرستان: %s--استان: %s" %(self.name, self.center, self.county, self.province)
		return 'No name'


class Contributor(models.Model):
	role_choices = (
		('C', 'citizen'),
		('I', 'staf'),
		)
	name = models.CharField(max_length = 30)
	tell = models.CharField(max_length = 11,unique = True)
	nc = models.CharField(max_length = 10, unique = True)
	role = models.CharField(max_length = 1, choices = role_choices, default = 'C')
	user = models.OneToOneField(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.name


class Need(models.Model):
    geom = models.PointField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True, null = True )
    #define shelter needs
    temporary_tent = models.PositiveSmallIntegerField(blank=True, null=True)
    permanent_tent = models.PositiveSmallIntegerField(blank=True, null=True)
    conex = models.PositiveSmallIntegerField(blank=True, null=True)

    def get_shelter(self):
        a = 0
        for i in [self.temporary_tent, self.permanent_tent, self.conex]:
            if i:
                a += i
            else:
                continue
        return a

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

    def get_clothing(self):
        a = 0
        for i in  [self.men_pants , self.women_pants, self.child_pants, self.men_shirt, self.women_shirt, self.men_shoes, self.women_shoes, self.child_shoes, self.women_shoes]:
            if i:
                a += i
            else:
                continue
        return a

    # define Flooring and bedspread
    carpet = models.PositiveSmallIntegerField(blank=True, null=True)
    blanket = models.PositiveSmallIntegerField(blank=True, null=True)

    def get_bedspread(self):
        a = 0
        for i in  [self.carpet, self.blanket]:
            if i:
                a += i
            else:
                continue
        return a

    # define food and drink
    water = models.PositiveSmallIntegerField(blank=True, null=True)
    canned_food = models.PositiveSmallIntegerField(blank=True, null=True)
    compote_and_juice = models.PositiveSmallIntegerField(blank=True, null=True)

    def get_food(self):
        a = 0
        for i in  [self.water, self.canned_food, self.compote_and_juice]:
            if i:
                a += i
            else:
                continue
        return a

    #define emergency services
    helicopter = models.PositiveSmallIntegerField(blank=True, null=True)
    ambulance = models.PositiveSmallIntegerField(blank=True, null=True)
    firefighter = models.PositiveSmallIntegerField(blank=True, null=True)
    doctor = models.PositiveSmallIntegerField(blank=True, null=True)
    nurse = models.PositiveSmallIntegerField(blank=True, null=True)
    police = models.PositiveSmallIntegerField(blank=True, null=True)
    voluntry_manpower = models.PositiveSmallIntegerField(blank=True, null=True)

    def get_emergency(self):
        a = 0
        for i in  [self.helicopter, self.ambulance, self.firefighter, self.doctor, self.nurse, self.police, self.voluntry_manpower]:
            if i:
                a += i
            else:
                continue
        return a


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

    def get_mashinary(self):
        a = 0
        for i in  [self.crane, self.excavator, self.bulldozer, self.truck, self.grinder, self.electric_hammer, self.electrik_driller, self.welding_engine, self.gas_welding, self.shovel, self.pocket, self.hammer]:
            if i:
                a += i
            else:
                continue
        return a

    # def save(self, *args, **kwargs):
    #     if Need.objects.filter(unit__geom__contains=self.location):
    #         return super(Unit, self).save(*args, **kwargs)
    def __str__(self):
        try:
            name = Unit.objects.get(geom__contains=self.geom).name
            return name
        except ObjectDoesNotExist:
            return 'شهرستان  خارج از سرپل'


    def save(self, *args, **kwargs):
        if not self.unit:
            self.unit = Unit.objects.get(geom__contains=Unit.objects.get(geom__contains=self.geom).geom)
        super(Need, self).save(*args, **kwargs)
