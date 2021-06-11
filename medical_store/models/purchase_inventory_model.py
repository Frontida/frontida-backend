from django.db import models
from medical_store.models import Purchase


class PurchaseInventory(models.Model):
    medicine_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    batch_number = models.CharField(max_length=20)
    price_of_each = models.PositiveIntegerField()
    mrp = models.PositiveIntegerField()
    mfd = models.DateField(null=False)
    expiry = models.DateField(null=False)
    purchase = models.ForeignKey(
        Purchase, on_delete=models.DO_NOTHING, related_name="purchaseinventory"
    )
    isexpired = models.BooleanField(default=False)

    class Meta:
        app_label = "medical_store"

    def __str__(self):
        return self.medicine_name
