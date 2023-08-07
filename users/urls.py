from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path(
        'signup/',
        views.SignUpView.as_view(),
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
    # path(
    #     'password_reset/',
    #     PasswordResetView.as_view(template_name='users/password_reset.html'),
    #     'password_reset'
    # ),
]
