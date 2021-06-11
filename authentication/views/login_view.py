from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from authentication.models import UserDetails
from authentication.serializers import UserDetailsSerializers, LoginSerializer


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
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if not user.is_verified:
            return Response(
                {"error": "User not verified"}, status=status.HTTP_401_UNAUTHORIZED
            )

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
