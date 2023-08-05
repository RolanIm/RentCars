# Generated by Django 4.2.3 on 2023-08-02 09:46

import ads.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0021_alter_car_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='currency',
            field=models.CharField(choices=[('$', 'Dollar'), ('€', 'Euro'), ('元', 'Yuan'), ('₽', 'Ruble'), ('£', 'Pound'), ('¥', 'Yen'), ('₸', 'Tenge'), ('₿', 'Bitcoin')], default='$', max_length=1),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1980), ads.models.max_value_current_year], verbose_name=('year',)),
        ),
    ]