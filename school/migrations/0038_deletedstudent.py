# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-14 16:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0037_paymentexception_filyal'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Studend')),
            ],
        ),
    ]
