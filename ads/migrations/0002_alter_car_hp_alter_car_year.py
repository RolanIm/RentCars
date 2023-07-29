# Generated by Django 4.2.3 on 2023-07-29 16:26

import ads.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='hp',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(70, message='Minimum quantity horse powers - 70'), django.core.validators.MaxValueValidator(1200, message='Maximum quantity horse powers - 1200')]),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1980), ads.models.max_value_current_year], verbose_name=('year',)),
        ),
    ]
