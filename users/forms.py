from django import forms
from django.contrib.auth.models import User
from ads.models import Owner
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       PasswordResetForm, SetPasswordForm)


class CreateUserForm(UserCreationForm):
    """
    Registration form. Includes first name, email and username.
    """

    class Meta:
        model = User
        fields = ('first_name', 'email', 'username')
        labels = {'Name': 'first_name'}
        help_texts = {
            'first_name': 'Your name or your company name.',
            'email': 'If you lost your password, '
                     'you can reset it only with email.'
        }


class UpdateUserForm(UserChangeForm):
    """
    Update profile form. Includes first name and email.
    """

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'email')
        labels = {'Name': 'first_name'}


class OwnerForm(forms.ModelForm):
    """
    Form for the Owner model. Includes phone and bio of the user.
    """

    class Meta:
        model = Owner
        fields = ['phone', 'bio']
        labels = {
            'bio': 'About me'
        }
        help_texts = {
            'phone': 'The phone number will be visible to all users '
                     'in your profile and in your ads.'
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
