from rest_framework import serializers
from ..models import User
# from rest_framework.serializers import ModelSerializer
# from rest_framework.response import Response

USER_TYPE = [("MEDICAL STORE", "MEDICAL STORE"), ("AMBULANCE", "AMBULANCE")]

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    user_type = serializers.ChoiceField(required=True, choices=USER_TYPE)
    password = serializers.CharField(
        max_length=68,
        min_length=8,
        write_only=True,
        required=True,
        style={"placeholder": "Password"},
    )

    class Meta:
        fields = ["email", "user_type", "password"]

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError(
                "User already registered with this email id"
            )
        except User.DoesNotExist:
            return email
