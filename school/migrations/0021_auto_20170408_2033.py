# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-08 16:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0020_payment_qalan_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studend',
            name='name',
        ),
        migrations.RemoveField(
            model_name='studend',
            name='surname',
        ),
    ]
