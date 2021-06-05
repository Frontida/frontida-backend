from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..Models.userdetails import UserDetails
from ..Serializers.userdetailsserializer import UserDetailsSerializers

class UserDetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_details = UserDetails.objects.get(account=request.user)
            serializer = UserDetailsSerializers(user_details)
            email = request.user.email
            response = {"data": serializer.data, "email": email}
            return Response(response, status=status.HTTP_200_OK)
        except UserDetails.DoesNotExist:
            return Response(
                {"error": "User details not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        serializer = UserDetailsSerializers(data=request.data)
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
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except UserDetails.DoesNotExist:
            serializer.save(account=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)