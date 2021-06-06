from django.db import models
from authentication.models import User

class Purchase(models.Model):
    distributor_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=200)
    bill_number = models.CharField(max_length=10)
    bill_date = models.DateField(null=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(decimal_places=2, max_digits=4)
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.distributor_name