# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Adı')),
                ('link', models.CharField(max_length=255, verbose_name='Linki')),
                ('status', models.BooleanField(default=True, verbose_name='Saytda görünməsi')),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name_plural': 'Sosial Linklər',
                'verbose_name': 'Sosial Link',
            },
        ),
    ]