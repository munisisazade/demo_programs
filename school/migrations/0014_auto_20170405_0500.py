# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0013_teacher_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='studend',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studend',
            name='testiq',
            field=models.BooleanField(default=False),
        ),
    ]
