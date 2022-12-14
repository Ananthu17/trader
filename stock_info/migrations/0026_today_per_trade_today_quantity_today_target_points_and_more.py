# Generated by Django 4.0 on 2022-01-31 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0025_trade_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='today',
            name='per_trade',
            field=models.FloatField(blank=True, null=True, verbose_name='Per Trade'),
        ),
        migrations.AddField(
            model_name='today',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='today',
            name='target_points',
            field=models.FloatField(blank=True, null=True, verbose_name='Target Points'),
        ),
        migrations.AddField(
            model_name='today',
            name='today_target',
            field=models.FloatField(blank=True, null=True, verbose_name='Target Today'),
        ),
    ]
