# Generated by Django 4.0 on 2022-01-28 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0018_alter_stock_todays_high_alter_stock_todays_low_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='day',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='stock_info.today'),
        ),
    ]
