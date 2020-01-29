# -*- coding: utf-8 -*-
# Generated by Django 2.1.12 on 2020-01-15 10:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_account_opted_out_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborator',
            name='custom_fee',
            field=models.FloatField(blank=True, null=True, verbose_name='Cuota específica'),
        ),
        migrations.AddField(
            model_name='colaborator',
            name='is_collaborator',
            field=models.BooleanField(default=False, verbose_name='Es colaboradora'),
        ),
        migrations.AddField(
            model_name='colaborator',
            name='is_sponsor',
            field=models.BooleanField(default=False, verbose_name='Es patrocinadora'),
        ),
        migrations.AddField(
            model_name='colaborator',
            name='special_agreement',
            field=models.TextField(blank=True, verbose_name='Acuerdos especiales'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='start_year',
            field=models.PositiveSmallIntegerField(blank=True, default=2020, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2020)], verbose_name='Año de inicio del proyecto'),
        ),
    ]
