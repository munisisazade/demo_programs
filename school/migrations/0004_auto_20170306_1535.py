# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-06 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20170306_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='birthday',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='ad günü'),
        ),
    ]
