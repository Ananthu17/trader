# Generated by Django 4.0 on 2022-01-01 10:59

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('stock_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('trades', models.IntegerField(blank=True, verbose_name='Number Of Trades')),
                ('success', models.IntegerField(blank=True, verbose_name='Success')),
                ('failure', models.IntegerField(blank=True, verbose_name='Failure')),
                ('profit', models.IntegerField(blank=True, verbose_name='Total Profit')),
                ('loss', models.IntegerField(blank=True, verbose_name='Total Loss')),
                ('wallet', models.IntegerField(blank=True, verbose_name='Wallet Balance')),
                ('target_percentage', models.IntegerField(blank=True, verbose_name='Target Percentage')),
                ('gain_margin', models.IntegerField(blank=True, verbose_name='Margin')),
            ],
        ),
    ]
