from rest_framework import serializers
from .models import User,UserDetails
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

USER_TYPE=[
    ('MEDICAL STORE','MEDICAL STORE'),
    ('AMBULANCE','AMBULANCE')
]

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    user_type = serializers.ChoiceField(required=True, choices=USER_TYPE)
    password = serializers.CharField(
        max_length=68,min_length=8,
        write_only=True,
        required=True,
        style={'placeholder': 'Password'}
    )
    
    class Meta:
        fields=['email','user_type','password']
    
    def validate_email(self, email):
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError("User already registered with this email id")
        except User.DoesNotExist:
            return email

class LoginSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=255)
    password=serializers.CharField(max_length=68,min_length=8)
    class Meta:
        fields=['email','password']


class PasswordResetEmailRequestSerializer(serializers.Serializer):
    email=serializers.EmailField()

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length = 8, required=True)
    password2 = serializers.CharField(min_length = 8, required=True)

    class Meta:
        fields = ['password1', 'password2']


class UserDetailsSerializers(ModelSerializer):
    class Meta:
        model=UserDetails
        exclude=['account',]
    
    def validate(self,attrs):
        if attrs.get('pincode') not in range(100000, 999999):
            return Response({'error': 'Invalid pincode'})
        if attrs.get('contact') not in range(6000000000, 9999999999):
            return Response({'error': 'Invalid contact number'})
        return super().validate(attrs)