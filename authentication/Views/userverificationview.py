import os
from django.shortcuts import redirect
from ..Models.user import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.utils.encoding import (
    force_str,
    DjangoUnicodeDecodeError
)



def UserVerification(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
    except DjangoUnicodeDecodeError:
        raise AuthenticationFailed("Not a valid account verification link", 401)
    except User.DoesNotExist:
        raise AuthenticationFailed("Not a valid account verification link", 401)

    if token != Token.objects.get(user=user).key:
        raise AuthenticationFailed("Not a valid account verification link", 401)
    else:
        if not user.is_verified:
            user.is_verified = True
            user.save()
        user.auth_token.delete()
        Token.objects.create(user=user)
        frontend_login_url = os.environ.get("FRONTEND_LOGIN_URL")
        return redirect(frontend_login_url)