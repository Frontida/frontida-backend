from rest_framework.serializers import ModelSerializer
from ..Models.userdetails import UserDetails
from rest_framework.response import Response

class UserDetailsSerializers(ModelSerializer):
    class Meta:
        model = UserDetails
        exclude = [
            "account",
        ]

    def validate(self, attrs):
        if attrs.get("pincode") not in range(100000, 999999):
            return Response({"error": "Invalid pincode"})
        if attrs.get("contact") not in range(6000000000, 9999999999):
            return Response({"error": "Invalid contact number"})
        return super().validate(attrs)