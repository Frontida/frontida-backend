from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from authentication.models import User
from authentication.serializers import PasswordResetEmailRequestSerializer


class RequestPasswordResetEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetEmailRequestSerializer(data=request.data)

        if not serializer.is_valid():
            error_values = list(serializer.errors.values())
            error_keys = list(serializer.errors.keys())
            if len(error_keys) > 0 and len(error_values) > 0:
                return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

        email = serializer.validated_data.get("email")
        try:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = Token.objects.get(user=user).key
            password_reset_link = (
                "https://frontida.netlify.app/resetPassword/"
                + uidb64
                + "/"
                + token
                + "/"
            )

            subject = "Password reset link for " + str(user.email)
            message = (
                "Hello, \n Below is the link to reset your password \n"
                + password_reset_link
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [
                user.email,
            ]

            email = EmailMessage(
                subject,
                message,
                from_email,
                recipient_list,
            )
            email.send()

            return Response(
                {"success": "Password reset link sent, check your inbox"},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "No user registered with this email"},
                status=status.HTTP_400_BAD_REQUEST,
            )
