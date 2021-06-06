from django.db import models
from .purchase import Purchase

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

    def __str__(self):
        return self.medicine_name