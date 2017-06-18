# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 12:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_auto_20170306_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('take_part', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize', models.FloatField(max_length=255)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='RelationDateLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Subject')),
                ('teach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher_lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher_student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='allowedipaddress',
            name='failed_login',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studend',
            name='plan',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher_student',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Studend'),
        ),
        migrations.AddField(
            model_name='teacher_student',
            name='teach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='relationdatelesson',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Teacher_lesson'),
        ),
        migrations.AddField(
            model_name='payment',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Studend'),
        ),
        migrations.AddField(
            model_name='payment',
            name='teach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendense',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Studend'),
        ),
        migrations.AddField(
            model_name='attendense',
            name='teach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]