# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-22 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0006_cif_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestaccount',
            name='cyclos_user',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Antiguo usuario en Cyclos'),
        ),
    ]