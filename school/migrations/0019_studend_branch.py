# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 21:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0018_myuser_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='studend',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.PandaBranch', verbose_name='Tələbənin filialı'),
        ),
    ]
