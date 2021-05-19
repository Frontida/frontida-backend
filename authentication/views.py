import os
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    PasswordResetEmailRequestSerializer, 
    UserDetailsSerializers, 
    SetNewPasswordSerializer
) 
from .models import User, UserDetails
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.utils.encoding import (
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.core.mail import EmailMessage

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

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = Token.objects.get(user=user).key

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


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            error_values = list(serializer.errors.values())
            error_keys = list(serializer.errors.keys())
            if len(error_keys) > 0 and len(error_values) > 0:
                return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

        user = authenticate(
            email=serializer.data.get("email"), password=serializer.data.get("password")
        )

        if not user:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_200_OK)
        if not user.is_verified:
            return Response({"error": "User not verified"}, status=status.HTTP_200_OK)
        
        login(request, user)
        
        token = Token.objects.filter(user=user)
        if len(token) > 0:
            token.delete()
        
        token = Token.objects.create(user=user).key
        
        try:
            user_details = UserDetailsSerializers(
                instance=UserDetails.objects.get(account=request.user)
            )
        except UserDetails.DoesNotExist as exp:
            return Response(
                {"NoUserDetails": "User details not provided", "token": token},
                status=status.HTTP_200_OK,
            )
        
        response_data = {
            "email": serializer.data.get("email"),
            "user_type": request.user.user_type,
            "token": token,
            "user_details": user_details.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            request.user.auth_token.delete()
        except Exception as exp:
            raise AuthenticationFailed(exp, 200)

        logout(request)

        return Response(
            {"success": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class UserDetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if not request.user.is_authenticated:
        #     return Response(
        #         {"error": "User not logged  in"}, status=status.HTTP_401_UNAUTHORIZED
        #     )

        try:
            user_details = UserDetails.objects.get(account=request.user)
            serializer = UserDetailsSerializers(user_details)
            email = request.user.email
            response = {"data": serializer.data, "email": email}
            return Response(response, status=status.HTTP_200_OK)
        except UserDetails.DoesNotExist:
            return Response(
                {"error": "User details not provided"}, status=status.HTTP_200_OK
            )

    def post(self, request):
        serializer = UserDetailsSerializers(data=request.data)
        # if not request.user.is_authenticated:
        #     return Response(
        #         {"error": "User not logged  in"}, status=status.HTTP_401_UNAUTHORIZED
        #     )

        if not serializer.is_valid():
            error_values = list(serializer.errors.values())
            error_keys = list(serializer.errors.keys())
            if len(error_keys) > 0 and len(error_values) > 0:
                return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

        try:
            UserDetails.objects.get(account=request.user)
            return Response(
                {
                    "DetailsExists": "Requested user details already exist try updating it"
                }
            )
        except UserDetails.DoesNotExist:
            serializer.save(account=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            password_reset_link = request.META.get("HTTP_HOST") + reverse(
                "password-reset-confirm", kwargs={"uidb64": uidb64, "token": token}
            )

            subject = "Password reset link for " + str(user.email)
            message = "Hello, \n Below is the link to reset your password \n" + password_reset_link
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
            return Response({"error": "No user registered with this email"} ,status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirm(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if token != Token.objects.get(user=user).key:
                raise AuthenticationFailed("Not a valid reset link", 200)
            else:
                return Response({"success": "Token authenticated"})
        except DjangoUnicodeDecodeError:
            raise AuthenticationFailed("Not a valid reset link", 200)

    def patch(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            
            if token != Token.objects.get(user=user).key:
                raise AuthenticationFailed("Not a valid reset link", 200)
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
                    return Response({'error':'The two passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(password1)
                user.save()
                return Response(
                    {"success": "Password reset successfull"}, status=status.HTTP_200_OK
                )
        
        except DjangoUnicodeDecodeError:
            raise AuthenticationFailed("Not a valid user", 200)
