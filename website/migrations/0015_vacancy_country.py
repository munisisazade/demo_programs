# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-21 10:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20170521_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.VacancyMenu', verbose_name='ərazi'),
        ),
    ]
