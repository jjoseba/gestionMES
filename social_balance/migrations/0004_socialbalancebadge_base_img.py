# Generated by Django 2.1.12 on 2019-10-16 11:21

from django.db import migrations
import helpers.filesystem
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('social_balance', '0003_socialbalance_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialbalancebadge',
            name='base_img',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=helpers.filesystem.RandomFileName('balance/badges/'), verbose_name='Plantilla para el sello de balance social'),
        ),
    ]
