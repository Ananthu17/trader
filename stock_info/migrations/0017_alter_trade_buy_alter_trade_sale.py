# Generated by Django 4.0 on 2022-01-28 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0016_alter_today_diffrence_alter_today_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='buy',
            field=models.FloatField(blank=True, null=True, verbose_name='Buy Price'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='sale',
            field=models.FloatField(blank=True, null=True, verbose_name='Sale Price'),
        ),
    ]
