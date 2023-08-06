from django import forms
from django.contrib.auth.models import User
from ads.models import Owner
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username')


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ('phone', 'bio')
        labels = {
            'bio': 'About me'
        }
