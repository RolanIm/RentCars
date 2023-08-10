from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views
from .views import (UserPasswordResetConfirmView, UserForgotPasswordView,
                    UserPasswordChangeView)


app_name = 'users'
urlpatterns = [
    path(
        'auth/signup/',
        views.CreateUserView.as_view(),
        name='signup'
    ),
    path(
        'auth/logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'auth/login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'auth/profile/update',
        views.UpdateUserView.as_view(),
        name='profile_update'
    ),
    path(
        'auth/password-reset/',
        UserForgotPasswordView.as_view(),
        name='password_reset'
    ),
    path(
        'auth/set-new-password/<uidb64>/<token>/',
        UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        '<int:pk>/password/',
        UserPasswordChangeView.as_view(),
        name='password_change'
    ),
]
