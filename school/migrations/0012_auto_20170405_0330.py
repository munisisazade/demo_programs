# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='studend',
            name='plan',
            field=models.IntegerField(blank=True, null=True, verbose_name='Dərs planı'),
        ),
    ]
