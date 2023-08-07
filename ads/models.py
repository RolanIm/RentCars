from django.db import models
from django.core.validators import (MinLengthValidator,
                                    MinValueValidator,
                                    MaxValueValidator, MaxLengthValidator)
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
import datetime


class Ad(models.Model):
    price_per_choice = [
        ('Hour', 'hour'),
        ('Day', 'day'),
        ('Week', 'week'),
        ('Month', 'month'),
    ]
    currency_choice = [
        ('$', 'Dollar'),
        ('€', 'Euro'),
        ('元', 'Yuan'),
        ('₽', 'Ruble'),
        ('£', 'Pound'),
        ('¥', 'Yen'),
        ('₸', 'Tenge'),
        ('₿', 'Bitcoin')
    ]

    #  Description
    text = models.TextField(null=True, blank=True)
    #  user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #  auto
    car = models.ForeignKey('Car',
                            blank=False,
                            null=False,
                            on_delete=models.CASCADE)
    #  reviews users about landlord
    comments = models.ManyToManyField(User,
                                      through='Comment',
                                      related_name='comments_owned'
                                      )
    #  Optional picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True,
                                    help_text='The MIMEType of the file')
    #  Favorites
    favorites = models.ManyToManyField(User,
                                       through='Fav',
                                       related_name='favorite_ads')
    #  Import TaggableManager from taggit
    tags = TaggableManager(blank=True)
    #  rental price
    price_per = models.CharField(max_length=5,
                                 blank=False,
                                 null=False,
                                 choices=price_per_choice,
                                 default='H')
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[
            MinValueValidator(
                0.1,
                'The rental price should be greater than zero.'
            )
        ]
    )
    currency = models.CharField(max_length=1,
                                null=False,
                                blank=False,
                                choices=currency_choice,
                                default='$')
    #  location
    country = models.CharField(max_length=50,
                               blank=False,
                               null=False)
    city = models.CharField(max_length=50,
                            blank=False,
                            null=False)
    #  Optional data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the Admin list
    def __str__(self):
        return f'{self.car.make.name} {self.car.model_name}, {self.car.year}'


class Fav(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['ad', 'owner']

    def __str__(self):
        title = (f'{self.ad.car.make.name} '
                 f'{self.ad.car.model_name}, '
                 f'{self.ad.car.year}')
        return '%s likes %s' % (self.owner.username, title)


class Comment(models.Model):
    text = models.TextField(
        validators=[
            MinLengthValidator(3, "Comment must be greater than 3 characters"),
            MaxLengthValidator(50, "Comment must be lower than 51 characters")
        ]
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15:
            return self.text
        return self.text[:11] + ' ...'


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Make(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)

    def __str__(self):
        return self.name


class Car(models.Model):
    choice_transmission = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual')
    ]
    min_val_msg = 'Minimum quantity horse powers - 70'
    max_val_msg = 'Maximum quantity horse powers - 1200'

    model_name = models.CharField(null=False, blank=False, max_length=30)
    transmission = models.CharField(
        max_length=9,
        null=False,
        blank=False,
        choices=choice_transmission
    )
    passenger_numbers = models.IntegerField(
        null=False,
        blank=False,
        choices=[(x, x) for x in range(1, 12)]
    )
    hp = models.IntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(70, message=min_val_msg),
            MaxValueValidator(1200, message=max_val_msg)
        ]
    )
    year = models.IntegerField('year', validators=[
        MinValueValidator(1980),
        max_value_current_year
    ])
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.make.name} {self.model_name}, {self.year}'


class Owner(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Owner.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.owner.save()
