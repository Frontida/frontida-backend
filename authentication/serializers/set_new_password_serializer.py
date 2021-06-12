from rest_framework import serializers


class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=8, required=True)
    password2 = serializers.CharField(min_length=8, required=True)

    class Meta:
        fields = ["password1", "password2"]
