from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    register,
    login_view,
    logout_view,
    profile,
    edit_profile_view,
    confirm_email,
    confirm_registration,
)

app_name = "account"


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path("edit_profile/", edit_profile_view, name="edit_profile"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("account:password_change_done"),
            template_name="account/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("confirm_email/", confirm_email, name="confirm_email"),
    path("confirm_registration", confirm_registration, name="confirm_registration"),
]
