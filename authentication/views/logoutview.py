from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import status

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            request.user.auth_token.delete()
        except Exception as exp:
            raise AuthenticationFailed(exp, 401)

        logout(request)

        return Response(
            {"success": "Successfully logged out."}, status=status.HTTP_200_OK
        )