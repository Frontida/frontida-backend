from django.db import models
from .sales import Sales

class SalesInventory(models.Model):
    medicine_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    # prescription = models.CharField(max_length=)
    batch_number = models.CharField(max_length=20)
    price_of_each = models.PositiveIntegerField()
    sales_id = models.ForeignKey(
        Sales, on_delete=models.DO_NOTHING, related_name="salesinventory"
    )
    isexpired = models.BooleanField(default=False)

    class Meta:
        app_label = "medical_store"

    def __str__(self):
        return self.medicine_name