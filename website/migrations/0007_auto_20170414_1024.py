# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 06:24
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import school.options.tools


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_programs_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Başlıq')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('cover_picture', models.ImageField(blank=True, null=True, upload_to=school.options.tools.get_news_photo_file_name)),
                ('status', models.BooleanField(default=True, verbose_name='Sayta görünüşü')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Bizim programlar başlığı',
                'verbose_name': 'Bizim programlar başlığı',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Bölmələr',
                'verbose_name': 'Bölmə',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='news',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Sections'),
        ),
    ]