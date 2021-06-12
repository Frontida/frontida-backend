from rest_framework.serializers import ModelSerializer
from ..models import SalesInventory


class SalesInventorySerializers(ModelSerializer):
    class Meta:
        model = SalesInventory
        exclude = ["sales_id", "isexpired"]
