from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetConfirmView)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from .forms import (OwnerForm, CreateUserForm, UpdateUserForm,
                    UserForgotPasswordForm, UserSetNewPasswordForm)
from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerUserView(View):
    """
    Parent class for user registration and update profile.
    """

    template_name = 'users/profile_update.html'
    action = None

    def get(self, request, user_form=None, owner_form=None):
        forms = [user_form, owner_form]
        ctx = {
            'forms': forms
        }
        return render(request, self.template_name, ctx)

    @transaction.atomic
    def post(self, request, user_form=None, owner_form=None):

        if not (user_form.is_valid() and owner_form.is_valid()):
            forms = [user_form, owner_form]
            ctx = {
                'forms': forms
            }
            return render(request, self.template_name, ctx)

        owner = owner_form.save(commit=False)
        # if UpdateUserView subclass
        if self.action == 'update':
            user = user_form.save(commit=False)
            user.username = request.user.username
            owner.user = request.user
            user.save()
            messages.success(request, _('Your profile updated!'))
            success_url = reverse('ads:ad_profile',
                                  args=[request.user.username])
        # if CreateUserView subclass
        else:
            user = user_form.save()
            # load the owner instance created by the signal
            user.refresh_from_db()
            owner = OwnerForm(request.POST, instance=user.owner)
            owner.full_clean()
            # automatically login after registration
            new_user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password2']
            )
            login(request, new_user)
            messages.success(request, _('You are registered!'))
            success_url = reverse_lazy('ads:all')
        owner.save()
        return redirect(success_url)


class CreateUserView(OwnerUserView):
    """
    Subclass for user registration.
    """

    template_name = 'users/signup.html'
    success_url = reverse_lazy('ads:all')
    action = 'signup'

    def get(self, request, user_form=None, owner_form=None):
        user_form = CreateUserForm()
        owner_form = OwnerForm()
        return super().get(request, user_form, owner_form)

    @transaction.atomic
    def post(self, request, user_form=None):
        user_form = CreateUserForm(request.POST or None)
        owner_form = OwnerForm(request.POST or None)
        return super().post(request, user_form, owner_form)


class UpdateUserView(LoginRequiredMixin, OwnerUserView):
    """
    Subclass for update profile of user.
    """

    template_name = 'users/profile_update.html'
    action = 'update'

    def get(self, request, user_form=None, owner_form=None):
        user_form = UpdateUserForm(instance=request.user)
        owner_form = OwnerForm(instance=request.user.owner)
        return super().get(request, user_form, owner_form)

    @transaction.atomic
    def post(self, request, user_form=None):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        owner_form = OwnerForm(request.POST, instance=request.user.owner)
        return super().post(request, user_form, owner_form)


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    View for password reset by email.
    """

    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('ads:all')
    success_message = '''
            An instructions on how to reset your
            password has been sent to your email.
            '''
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'password recovery request'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin,
                                   PasswordResetConfirmView):
    """
    Set new password view.
    """

    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('ads:all')
    success_message = 'Password done! Yoy can login on the site.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Set new password'
        return context
