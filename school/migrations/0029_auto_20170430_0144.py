# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-29 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0028_pandabranch_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pandabranch',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Sistemdə görünməyi'),
        ),
    ]
