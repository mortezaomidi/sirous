# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-02 22:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webgis', '0004_need_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='need',
            old_name='location',
            new_name='geom',
        ),
    ]