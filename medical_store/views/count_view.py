from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from collections import Counter
from medical_store.models import Purchase, MedicineInventory, Sales


class CountAPI(APIView):
    queryset = Purchase.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        medicine_names = [
            medicine.medicine_name
            for medicine in MedicineInventory.objects.filter(account=request.user)
        ]
        sales_names = [sales.id for sales in Sales.objects.filter(account=request.user)]
        purchase_names = [
            purchase.id for purchase in Purchase.objects.filter(account=request.user)
        ]

        medicine_count = len(Counter(medicine_names).keys())
        sales_count = len(Counter(sales_names).keys())
        purchase_count = len(Counter(purchase_names).keys())

        return Response(
            {
                "medicine_count": medicine_count,
                "sales_count": sales_count,
                "purchase_count": purchase_count,
            },
            status=status.HTTP_200_OK,
        )
