from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views
from .views import UserPasswordResetConfirmView, UserForgotPasswordView

app_name = 'users'
urlpatterns = [
    path(
        'signup/',
        views.CreateUserView.as_view(),
        name='signup'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'profile/update',
        views.UpdateUserView.as_view(),
        name='profile_update'
    ),
    path(
        'password-reset/',
        UserForgotPasswordView.as_view(),
        name='password_reset'
    ),
    path(
        'set-new-password/<uidb64>/<token>/',
        UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]
