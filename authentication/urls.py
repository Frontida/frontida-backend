from django.urls import path
from .views import (
    UserVerification,
    RegisterView,
    LoginAPI,
    LogoutView,
    UserDetailsView,
    RequestPasswordResetEmail,
    PasswordResetConfirm
)


urlpatterns = [
    path(
        "user_verification/<uidb64>/<token>", UserVerification, name="user_verification"
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user-details/", UserDetailsView.as_view(), name="user_details"),
    path(
        "request-reset-email/",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirm.as_view(),
        name="password-reset-confirm",
    ),
]
