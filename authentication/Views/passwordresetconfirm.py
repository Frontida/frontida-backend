from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from rest_framework.exceptions import AuthenticationFailed
from ..Models.user import User
from ..Serializers.setnewpasswordserializer import SetNewPasswordSerializer



class PasswordResetConfirm(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if token != Token.objects.get(user=user).key:
                raise AuthenticationFailed("Not a valid reset link", 400)
            else:
                return Response({"success": "Token authenticated"})
        except DjangoUnicodeDecodeError:
            raise AuthenticationFailed("Not a valid reset link", 400)

    def patch(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if token != Token.objects.get(user=user).key:
                raise AuthenticationFailed("Not a valid reset link", 400)
            else:
                serializer = SetNewPasswordSerializer(data=request.data)

                if not serializer.is_valid():
                    error_values = list(serializer.errors.values())
                    error_keys = list(serializer.errors.keys())
                    if len(error_keys) > 0 and len(error_values) > 0:
                        return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

                password1 = serializer.data["password1"]
                password2 = serializer.data["password2"]

                if password1 != password2:
                    return Response(
                        {"error": "The two passwords do not match"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.set_password(password1)
                user.save()
                return Response(
                    {"success": "Password reset successfull"}, status=status.HTTP_200_OK
                )

        except DjangoUnicodeDecodeError:
            raise AuthenticationFailed("Not a valid user", 401)
