# Generated by Django 2.1.12 on 2020-07-07 13:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_entity_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Tipo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('color', models.CharField(blank=True, max_length=30, null=True, verbose_name='Color de etiqueta (código hexadecimal)')),
                ('default_fee', models.FloatField(blank=True, null=True, verbose_name='Cuota por defecto')),
            ],
            options={
                'verbose_name': 'Tipos de colaboración',
                'verbose_name_plural': 'Tipos de colaboración',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EntityCollaboration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Orden')),
                ('special_agreement', models.TextField(blank=True, verbose_name='Acuerdos especiales')),
                ('custom_fee', models.FloatField(blank=True, null=True, verbose_name='Cuota específica')),
                ('started', models.DateField(default=django.utils.timezone.now, verbose_name='Inicio de la colaboración')),
                ('ended', models.DateField(blank=True, null=True, verbose_name='Fin de la colaboración')),
                ('collaboration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batch_payments', to='accounts.Collaboration')),
                ('entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batch_payments', to='accounts.Entity')),
            ],
            options={
                'verbose_name': 'Colaboración de entidad',
                'verbose_name_plural': 'Colaboraciones con entidad',
                'ordering': ['-started'],
            },
        ),
        migrations.AddField(
            model_name='entity',
            name='collabs',
            field=models.ManyToManyField(related_name='entities', through='accounts.EntityCollaboration', to='accounts.Collaboration', verbose_name='Colaboraciones'),
        ),
    ]
