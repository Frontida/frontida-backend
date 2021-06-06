from django.db import models
from authentication.models import User

class Sales(models.Model):
    bill_number = models.CharField(max_length=10)
    customer_name = models.CharField(max_length=50)
    customer_contact = models.BigIntegerField()
    referred_by = models.CharField(max_length=50)
    bill_date = models.DateField()
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(decimal_places=2, max_digits=4)
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_name