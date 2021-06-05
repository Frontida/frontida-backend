from django.urls import path
from .Views import (
    userverificationview,
    registerview,
    loginview,
    logoutview,
    userdetailsview,
    passwordresetemailview,
    passwordresetconfirm
)


urlpatterns = [
    path(
        "user_verification/<uidb64>/<token>", userverificationview.UserVerification, name="user_verification"
    ),
    path("register/", registerview.RegisterView.as_view(), name="register"),
    path("login/", loginview.LoginAPI.as_view(), name="login"),
    path("logout/", logoutview.LogoutView.as_view(), name="logout"),
    path("user-details/", userdetailsview.UserDetailsView.as_view(), name="user_details"),
    path(
        "request-reset-email/",
        passwordresetemailview.RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        passwordresetconfirm.PasswordResetConfirm.as_view(),
        name="password-reset-confirm",
    ),
]
