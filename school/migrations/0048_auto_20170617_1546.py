# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-17 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0047_pandabranch_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='pandabranch',
            name='admin_color',
            field=models.CharField(default='#000000', max_length=25, verbose_name='Rəngin kodu'),
        ),
        migrations.AlterField(
            model_name='pandabranch',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yaradıldığı tarix'),
        ),
    ]
