from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from medical_store.models import Purchase, CompanyDetails, MedicineInventory
from medical_store.serializers import PurchaseSerializers


class PurchaseViewSets(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request):
        purchases = Purchase.objects.filter(account=request.user)
        company_name = [
            company.company_name for company in CompanyDetails.objects.all()
        ]
        serializer = self.serializer_class(purchases, many=True)
        responsedata = {"previousbills": serializer.data, "companynames": company_name}
        return Response(responsedata, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            error_values = list(serializer.errors.values())
            error_keys = list(serializer.errors.keys())
            if len(error_keys) > 0 and len(error_values) > 0:
                return Response({f"{error_keys[0]}": f"{error_values[0][0]}"})
        try:
            company = CompanyDetails.objects.get(
                company_name=serializer.validated_data.get("company_name")
            )
        except CompanyDetails.DoesNotExist as exp:
            return Response(
                {"error": "Invalid company name"}, status=status.HTTP_400_BAD_REQUEST
            )
        purchase = serializer.save(account=request.user, company_name=company)
        purchase_inventory = purchase.purchaseinventory.all()
        for entry in purchase_inventory:
            try:
                med_inventory = MedicineInventory.objects.get(
                    medicine_name=entry.medicine_name, batch_number=entry.batch_number
                )
                med_inventory.medicine_quantity += entry.quantity
                med_inventory.save()
            except MedicineInventory.DoesNotExist as identifier:
                med_inventory = MedicineInventory(
                    medicine_name=entry.medicine_name,
                    batch_number=entry.batch_number,
                    company_name=company,
                    mfd=entry.mfd,
                    expiry=entry.expiry,
                    purchase_price=entry.price_of_each,
                    sale_price=entry.mrp,
                    medicine_quantity=entry.quantity,
                    account=request.user,
                )
                med_inventory.save()
        serializer = PurchaseSerializers(instance=purchase)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            purchase = Purchase.objects.get(pk=pk)
            serializer = self.serializer_class(purchase)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Purchase.DoesNotExist as exp:
            return Response(
                {"doesNotExist": "does not exist in database"},
                status=status.HTTP_404_NOT_FOUND,
            )
