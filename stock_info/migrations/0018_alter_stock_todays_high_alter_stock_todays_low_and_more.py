# Generated by Django 4.0 on 2022-01-28 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0017_alter_trade_buy_alter_trade_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='todays_high',
            field=models.FloatField(blank=True, null=True, verbose_name="Today's High"),
        ),
        migrations.AlterField(
            model_name='stock',
            name='todays_low',
            field=models.FloatField(blank=True, null=True, verbose_name="Today's Low"),
        ),
        migrations.AlterField(
            model_name='trade',
            name='status',
            field=models.CharField(blank=True, choices=[('Po', 'Profit'), ('Ls', 'Loss'), ('No', 'NO Change'), ('In', 'In Progress')], max_length=30, verbose_name='Status'),
        ),
    ]
