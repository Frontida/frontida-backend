from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=200)
    company_contact = models.BigIntegerField(
        validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)]
    )
    company_address = models.CharField(max_length=200)
    company_email = models.EmailField()
    gst_number = models.CharField(max_length=15)

    class Meta:
        app_label = "medical_store"

    def __str__(self):
        return self.company_name