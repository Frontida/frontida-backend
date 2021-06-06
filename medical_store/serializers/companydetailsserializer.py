from rest_framework.serializers import ModelSerializer
from ..models import CompanyDetails

class CompanyDetailsSerializers(ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = [
            "company_name",
            "company_contact",
            "company_address",
            "company_email",
            "gst_number",
        ]