# Generated by Django 2.1.12 on 2020-06-17 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_bpm', '0013_process_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processworkflowevent',
            name='timestamp',
            field=models.DateTimeField(verbose_name='Fecha'),
        ),
    ]
