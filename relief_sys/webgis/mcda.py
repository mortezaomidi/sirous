from django.contrib.gis.db.models import Sum
from numpy import *

from .models import Need
from .models import Unit

# Step 1: make dm matrix
def make_dm_matrix():
    """ a function for create DM matrix
        this function has no argument.
	"""


    #step1.1: get ids of target units
    alternatives = Unit.objects.all()
    unique_alts_ids = [alt.id for alt in set(alternatives)]
    # OR target_units = Unit.objects.filter(pk__in=alternatives_ids())


    #step1.2: make criteria dict
    fields = ['temporary_tent', 'permanent_tent', 'conex', 'carpet', 'blanket', 'water']

    data = {}
    dm = []
    for i in unique_alts_ids:
        data[i] = {}

    for id in unique_alts_ids:
        for field in fields:
            s = Need.objects.filter(unit__pk=id).aggregate(
            Sum(field)) [field + '__sum']
            if s == None or 0 :
                s = 0.0
            data[id][field] = s

    #step1.3: make dm array / matrix

    for key, value in data.items():
        dm.append(list(data[key].values()))

    return array(dm)


# Step 1: normalize the decision matrix
def norm(x, y):
    """ normalization function; x is the array with the
    performances and y is the normalization method.
    For vector input 'v' and for linear 'l'
	"""
    if y == 'v':
        k = array(cumsum(x**2, 0))
        z = array([[round(x[i, j] / sqrt(k[x.shape[0] - 1,
            j]), 3) for j in range(x.shape[1])]
            for i in range(x.shape[0])])
        return z
    else:
        yy = []
        for i in range(x.shape[1]):
            yy.append(amax(x[:, i:i + 1]))
            k = array(yy)
        z = array([[round(x[i, j] / k[j], 3)
            for j in range(x.shape[1])]
            for i in range(x.shape[0])])
        return z
