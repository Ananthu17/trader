# Generated by Django 4.0 on 2022-01-03 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0006_alter_stock_change_rate_alter_stock_percentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentprice',
            name='price',
            field=models.FloatField(blank=True, verbose_name='Price'),
        ),
    ]
