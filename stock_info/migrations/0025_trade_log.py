# Generated by Django 4.0 on 2022-01-28 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0024_alter_trade_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='log',
            field=models.TextField(blank=True),
        ),
    ]
