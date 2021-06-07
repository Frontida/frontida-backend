from django.db import models
from authentication.models import User

class MedicineInventory(models.Model):
    HSNcode = models.CharField(max_length=6, default="3004", blank=True)
    batch_number = models.CharField(max_length=20)
    medicine_name = models.CharField(max_length=200)
    company_name = models.ForeignKey(
        "CompanyDetails", max_length=200, on_delete=models.DO_NOTHING
    )
    mfd = models.DateField(null=False)
    expiry = models.DateField(null=False)
    purchase_price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField()
    medicine_quantity = models.PositiveIntegerField()
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    isexpired = models.BooleanField(default=False)

    class Meta:
        app_label = "medical_store"

    def __str__(self):
        return self.medicine_name