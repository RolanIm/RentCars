# Generated by Django 4.2.3 on 2023-07-29 17:17

import ads.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_alter_car_year_alter_make_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='city',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='owner',
            name='country',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1980), ads.models.max_value_current_year], verbose_name=('year',)),
        ),
    ]
