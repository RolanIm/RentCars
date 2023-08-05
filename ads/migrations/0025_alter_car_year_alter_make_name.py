# Generated by Django 4.2.3 on 2023-08-04 12:14

import ads.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0024_alter_car_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1980), ads.models.max_value_current_year], verbose_name=('year',)),
        ),
        migrations.AlterField(
            model_name='make',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]