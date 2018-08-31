from django.contrib.gis.db.models import Sum, Avg
import numpy
from .models import Need
from .models import Unit


def make_criterion_dic():
    c1_fields = ['temporary_tent', 'permanent_tent', 'conex']
    c2_fields = ['carpet', 'blanket', 'water']

    c1_sum = {}
    c2_sum = {}

    for field in c1_fields:
        c1_sum[field] = Need.objects.all().aggregate(
        Sum(field)) [field + '__sum'] or 0.0

    for field in c2_fields:
        c2_sum[field] = Need.objects.all().aggregate(
        Sum(field)) [field + '__sum'] or 0.0

    criterion = {'c1_sum': c1_sum, 'c2_sum': c2_sum}
    return criterion


def make_alternatives_dic():
    alternatives = Unit.objects.all()

    alternatives_pk_list = [item.pk for item in alternatives]
    alternatives_name_list = [item.name for item in alternatives]

    alternatives = {}
    counter = 0

    for pk in alternatives_pk_list:
        alternatives[pk] = alternatives_name_list[counter]
        counter += 1
    return alternatives


def make_dm_matrix():
    col_dic = make_criterion_dic()
    row_dic = make_alternatives_dic()

    dm = numpy.zeros(shape=(len(row_dic), len(col_dic)), dtype=float)
    pass
