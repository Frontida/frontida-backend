from rest_framework.serializers import ModelSerializer
from ..models import MedicineInventory


class MedicineInventorySerializers(ModelSerializer):
    class Meta:
        model = MedicineInventory
        # fields = ['batch_number', 'medicine_name', 'mfd', 'expiry', 'purchase_price', 'sale_price', 'medicine_quantity', 'company_name']
        exclude = ["account", "HSNcode"]
