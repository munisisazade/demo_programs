# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 22:52
from __future__ import unicode_literals

from django.db import migrations, models
import school.options.tools


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20170416_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='about_us',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=school.options.tools.get_about_us_photo_file_name, verbose_name='Şəkil'),
        ),
    ]
