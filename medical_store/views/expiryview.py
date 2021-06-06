from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from ..utils import CheckExpiry


class ExpiryAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        expired_medicine = CheckExpiry.check(request.user)
        return Response({"medicine_names": expired_medicine}, status=status.HTTP_200_OK)