# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-04 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_signup_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='business_name',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Raz\xf3n social'),
        ),
        migrations.AddField(
            model_name='entity',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre'),
        ),
    ]
