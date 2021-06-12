from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from medical_store.models import MedicineInventory
from medical_store.serializers import MedicineInventorySerializers


class MedicineInventoryViewSets(ViewSet):
    queryset = MedicineInventory.objects.all()
    serializer_class = MedicineInventorySerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        medicine_inventory = MedicineInventory.objects.filter(
            account=request.user, isexpired=False
        )
        serializer = MedicineInventorySerializers(medicine_inventory, many=True)
        medicine_intventory = serializer.data
        return Response(
            {"medicine_inventory": medicine_intventory}, status=status.HTTP_200_OK
        )
