# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_about_us_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programs_Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Başlıq')),
                ('content', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True, verbose_name='Sayta görünüşü')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Bizim programlar başlığı',
                'verbose_name': 'Bizim programlar başlığı',
                'ordering': ('-id',),
            },
        ),
    ]