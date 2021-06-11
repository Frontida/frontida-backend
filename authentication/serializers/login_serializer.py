from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, min_length=8)

    class Meta:
        fields = ["email", "password"]
