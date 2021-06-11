from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from medical_store.models import CompanyDetails
from medical_store.serializers import CompanyDetailsSerializers


class CompanyDetailsViewSets(ModelViewSet):
    serializer_class = CompanyDetailsSerializers
    queryset = CompanyDetails.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        print(request.user)
        if request.user.is_superuser:
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                error_values = list(serializer.errors.values())
                error_keys = list(serializer.errors.keys())
                if len(error_keys) > 0 and len(error_values) > 0:
                    return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

            serializer.save()
            return Response(
                {"Comanay Details": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def retrieve(self, request, pk=None):
        try:
            company = CompanyDetails.objects.get(pk=pk)
        except CompanyDetails.DoesNotExist as exp:
            return Response(
                {"error": "Company with given pk not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if request.user.is_superuser:
            instance = self.get_object()
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                error_values = list(serializer.errors.values())
                error_keys = list(serializer.errors.keys())
                if len(error_keys) > 0 and len(error_values) > 0:
                    return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

            instance.company_name = serializer.data["company_name"]
            instance.company_contact = serializer.data["company_contact"]
            instance.company_address = serializer.data["company_address"]
            instance.company_email = serializer.data["company_email"]
            instance.gst_number = serializer.data["gst_number"]
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def partial_update(self, request, pk=None):
        if request.user.is_superuser:
            instance = self.get_object()
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                error_values = list(serializer.errors.values())
                error_keys = list(serializer.errors.keys())
                if len(error_keys) > 0 and len(error_values) > 0:
                    return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

            instance.company_name = serializer.data["company_name"]
            instance.company_contact = serializer.data["company_contact"]
            instance.company_address = serializer.data["company_address"]
            instance.company_email = serializer.data["company_email"]
            instance.gst_number = serializer.data["gst_number"]
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def destroy(self, request, pk=None):
        if request.user.is_superuser:
            instance = self.get_object()
            serializer = self.serializer_class(data=instance)
            serializer.is_valid(raise_exception=True)
            instance.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
