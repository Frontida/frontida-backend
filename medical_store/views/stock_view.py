from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from medical_store.models import MedicineInventory


class StockAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        medicine_names = [
            medicine.medicine_name
            for medicine in MedicineInventory.objects.filter(account=request.user)
        ]
        medicine_names = list(set(medicine_names))
        low_stock = {}
        for medicine_name in medicine_names:
            medicines = MedicineInventory.objects.filter(medicine_name=medicine_name)
            count = 0
            for medicine in medicines:
                # print(medicine)
                count += medicine.medicine_quantity
            if count < 10:
                low_stock[medicine_name] = count
        return Response({"medicine_details": low_stock}, status=status.HTTP_200_OK)
