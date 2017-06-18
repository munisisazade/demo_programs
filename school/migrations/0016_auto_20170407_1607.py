# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0015_studend_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='studend',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Tam adi'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='prize',
            field=models.FloatField(max_length=255, verbose_name='Ödəniş məbləği'),
        ),
    ]