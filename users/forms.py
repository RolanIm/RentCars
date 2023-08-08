from django import forms
from django.contrib.auth.models import User
from ads.models import Owner
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       PasswordResetForm, SetPasswordForm)


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'email', 'username')
        labels = {'Name': 'first_name'}
        help_texts = {
            'first_name': 'your name or your company name',
            'email': 'if you lost your password, '
                     'you can reset it only with email'
        }


class UpdateUserForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'email')
        labels = {'Name': 'first_name'}


class OwnerForm(forms.ModelForm):

    class Meta:
        model = Owner
        fields = ['phone', 'bio']
        labels = {
            'bio': 'About me'
        }


class UserForgotPasswordForm(PasswordResetForm):
    """
    Password recovery request.
    """

    def __init__(self, *args, **kwargs):
        """
        Update form styles.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Changing user password after confirmation.
    """

    def __init__(self, *args, **kwargs):
        """
        Update form styles.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
