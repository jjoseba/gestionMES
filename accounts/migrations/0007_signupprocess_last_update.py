# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-15 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_signup_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupprocess',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='\xdaltima actualizaci\xf3n'),
        ),
    ]