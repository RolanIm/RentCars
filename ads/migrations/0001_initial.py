# Generated by Django 4.2.4 on 2023-08-06 10:23

import ads.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('picture', models.BinaryField(editable=True, null=True)),
                ('content_type', models.CharField(help_text='The MIMEType of the file', max_length=256, null=True)),
                ('price_per', models.CharField(choices=[('Hour', 'hour'), ('Day', 'day'), ('Week', 'week'), ('Month', 'month')], default='H', max_length=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0.1, 'The rental price should be greater than zero.')])),
                ('currency', models.CharField(choices=[('$', 'Dollar'), ('€', 'Euro'), ('元', 'Yuan'), ('₽', 'Ruble'), ('£', 'Pound'), ('¥', 'Yen'), ('₸', 'Tenge'), ('₿', 'Bitcoin')], default='$', max_length=1)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fav',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.ad')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(validators=[django.core.validators.MinLengthValidator(3, 'Comment must be greater than 3 characters')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.ad')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=30)),
                ('transmission', models.CharField(choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')], max_length=9)),
                ('passenger_numbers', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)])),
                ('hp', models.IntegerField(validators=[django.core.validators.MinValueValidator(70, message='Minimum quantity horse powers - 70'), django.core.validators.MaxValueValidator(1200, message='Maximum quantity horse powers - 1200')])),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1980), ads.models.max_value_current_year], verbose_name='year')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.make')),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.car'),
        ),
        migrations.AddField(
            model_name='ad',
            name='comments',
            field=models.ManyToManyField(related_name='comments_owned', through='ads.Comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ad',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_ads', through='ads.Fav', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ad',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL),
        ),
    ]
