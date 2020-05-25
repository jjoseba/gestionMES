# Generated by Django 2.1.12 on 2020-05-25 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_account_lastupdate'),
        ('payments', '0016_sepabatch_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountAnnualFeeCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
            ],
            options={
                'verbose_name': 'Cobro anual de cuota a socia',
                'verbose_name_plural': 'Cobros anuales de cuota a socias',
            },
        ),
        migrations.CreateModel(
            name='AnnualFeeCharges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='Año')),
                ('accounts', models.ManyToManyField(related_name='annual_fee_charges', through='payments.AccountAnnualFeeCharge', to='accounts.Account', verbose_name='Socias')),
            ],
            options={
                'verbose_name': 'Cobro anual de cuota',
                'verbose_name_plural': 'Cobros anuales de cuota',
                'ordering': ['-year'],
            },
        ),
        migrations.AddField(
            model_name='accountannualfeecharge',
            name='annual_charge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.AnnualFeeCharges'),
        ),
        migrations.AddField(
            model_name='accountannualfeecharge',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.PendingPayment'),
        ),
    ]
