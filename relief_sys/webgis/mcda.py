from django.contrib.gis.db.models import Sum
from django.core.serializers import serialize
from numpy import *
import json

from .models import Need
from .models import Unit


    #step1.1: get ids of target units
alternatives = Unit.objects.all()
unique_alts_ids = [alt.id for alt in set(alternatives)]
    # OR target_units = Unit.objects.filter(pk__in=alternatives_ids())

# Step 1: make dm matrix
def make_dm_matrix():
    """ a function for create DM matrix
        this function has no argument.
	"""





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


# Step 2: normalize the decision matrix
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

# Step 3: find the weighted normalized decision matrix
def mul_w(r, t):
    """ multiplication of each evaluation by the associate
    weight; r stands for the weights matrix and t for
    the normalized matrix resulting from norm()
	"""
    z = array([[round(t[i, j] * r[j], 3)
        for j in range(t.shape[1])]
        for i in range(t.shape[0])])
    return z

# Step 4: calculate the ideal and anti-ideal solutions
def zenith_nadir(x, y):
    """ zenith and nadir virtual action function; x is the
    weighted normalized decision matrix and y is the
    action used. For min/max input 'm' and for absolute
    input enter 'a'
	"""
    if y == 'm':
        bb = []
        cc = []
        for i in range(x.shape[1]):
            bb.append(amax(x[:, i:i + 1]))
            b = array(bb)
            cc.append(amin(x[:, i:i + 1]))
            c = array(cc)
        return (b, c)
    else:
        b = ones(x.shape[1])
        c = zeros(x.shape[1])
        return (b, c)


# Step 5: determine the distance to the ideal and anti-ideal
# solutions
def distance(x, y, z):
    """ calculate the distances to the ideal solution (di+)
    and the anti-ideal solution (di-); x is the result
    of mul_w() and y, z the results of zenith_nadir()
	"""
    a = array([[(x[i, j] - y[j])**2
		for j in range(x.shape[1])]
		for i in range(x.shape[0])])
    b = array([[(x[i, j] - z[j])**2
		for j in range(x.shape[1])]
        for i in range(x.shape[0])])
    return (sqrt(sum(a, 1)), sqrt(sum(b, 1)))

# TOPSIS method: it calls the other functions and includes
# step 6
def topsis(matrix, weight, norm_m, id_sol):
    """ matrix is the initial decision matrix, weight is
	the weights matrix, norm_m is the normalization
	method, id_sol is the action used, and pl is 'y'
	for plotting the results or any other string for
	not
	"""
    z = mul_w(weight, norm(matrix, norm_m))
    s, f = zenith_nadir(z, id_sol)
    p, n = distance(z, s, f)
    final_s = array([n[i] / (p[i] + n[i])
		for i in range(p.shape[0])])

    return final_s

def ranking():
    # step 7: ranking
    matrix = make_dm_matrix()
    w = array([0.2, 0.1,0.1,0.6,0.01,0.3])
    rank = topsis(matrix, w,norm(matrix,'l'), 'a')
    dict_data = {}
    for idx, val in enumerate(unique_alts_ids):
        dict_data[val] = rank[idx]
    geojson_data = serialize('geojson', Unit.objects.all(),
    geometry_field='geom',
          fields=('name','pk',))

    geojson_data = json.loads(geojson_data)

    for i in range(len(geojson_data['features'])):
        if int(geojson_data['features'][i]['properties']['pk']) in list(dict_data.keys()):
            geojson_data['features'][i]['properties']['rank'] = str(dict_data[int(geojson_data['features'][i]['properties']['pk'])])
        else:
            geojson_data['features'][i]['properties']['rank'] = str(0.0)

    geojson_data = json.dumps(geojson_data)

    return geojson_data
