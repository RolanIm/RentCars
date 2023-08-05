from django import forms
from django.contrib.auth import get_user_model
from ads.models import Owner

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ('phone', 'bio')
        labels = {
            'bio': 'About me'
        }
