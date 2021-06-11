from rest_framework import serializers


class PasswordResetEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ["email"]
