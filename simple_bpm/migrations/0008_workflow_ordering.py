# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-15 13:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_bpm', '0007_completedby_optional'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processworkflowevent',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Evento de Proceso', 'verbose_name_plural': 'Eventos de proceso'},
        ),
    ]
