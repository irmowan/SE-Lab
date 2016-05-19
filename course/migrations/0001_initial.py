# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('courseId', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('courseName', models.CharField(max_length=30)),
                ('teacherId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Users')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Courses')),
                ('studentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Users')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='courseselection',
            unique_together=set([('courseId', 'studentId')]),
        ),
    ]
