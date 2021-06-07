import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from ..models import Sales, MedicineInventory
from ..serializers import SalesSerializers


class SalesViewSets(ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request):
        sales = Sales.objects.filter(account=request.user)
        medicine_name = [
            medicine.medicine_name
            for medicine in MedicineInventory.objects.filter(
                account=request.user, isexpired=False
            )
        ]
        medicine_name = list(set(medicine_name))
        if len(sales) == 0:
            return Response(
                {"empty": "no records as of now"}, status=status.HTTP_200_OK
            )

        serializer = self.serializer_class(sales, many=True)
        responsedata = {
            "previoussales": serializer.data,
            "medicine_name": medicine_name,
        }
        return Response(responsedata, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error_values = list(serializer.errors.values())
            error_keys = list(serializer.errors.keys())
            if len(error_keys) > 0 and len(error_values) > 0:
                return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})

        for entry in serializer.validated_data.get("salesinventory"):
            medicine_name = entry.get("medicine_name")
            required_quantity = entry.get("quantity")
            med_inventory = list(
                MedicineInventory.objects.filter(medicine_name=medicine_name).order_by(
                    "sale_price"
                )
            )
            if len(med_inventory) == 0:
                return Response(
                    {"medicine": "not found"}, status=status.HTTP_400_BAD_REQUEST
                )
            available_stock = 0
            for medicine in med_inventory:
                if (medicine.expiry - datetime.date.today()) < datetime.timedelta(
                    days=90
                ):
                    medicine.isexpired = True
                    med_inventory.remove(medicine)
                    medicine.save()
                else:
                    available_stock += medicine.medicine_quantity

            if required_quantity > available_stock:
                return Response(
                    {"medicine": "not enough stock"}, status=status.HTTP_400_BAD_REQUEST
                )

            for medicine in med_inventory:
                if required_quantity < medicine.medicine_quantity:
                    medicine.medicine_quantity -= required_quantity
                    medicine.save()
                    break
                else:
                    required_quantity -= medicine.medicine_quantity
                    medicine.delete()

        sales = serializer.save(account=request.user)
        serializer = SalesSerializers(instance=sales)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            sales = Sales.objects.get(pk=pk)
            serializer = self.serializer_class(sales)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Sales.DoesNotExist as exp:
            return Response(
                {"doesNotExist": "does not exist in database"},
                status=status.HTTP_404_NOT_FOUND,
            )