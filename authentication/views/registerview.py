from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import (
    force_str,
    smart_bytes
)
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from rest_framework import status
from ..models import User
from ..serializers import RegisterSerializer



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            error_values = list(serializer.errors.values())
            error_keys = list(serializer.errors.keys())
            if len(error_keys) > 0 and len(error_values) > 0:
                return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

        user = User.objects.create_user(**serializer.validated_data)
        print(user)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = Token.objects.create(user=user).key

        user_verification_link = get_current_site(request).domain + reverse(
            "user_verification", kwargs={"uidb64": uidb64, "token": token}
        )

        subject = "Account verification for " + str(user.email)
        message = (
            "Hello, \n Thankyou for joining us, please login to complete your details and registration process. \n"
            + user_verification_link
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list,
        )
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED)