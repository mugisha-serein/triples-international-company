from django.contrib.auth import get_user_model
from rest_framework import serializers
import re

User = get_user_model()

class UserService:
    @staticmethod
    def validate_phone_number(phone):
        """
        Validates the phone number format.
        """
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise serializers.ValidationError("Invalid phone number format. Use E.164 (e.g. +123456789).")
        return phone

    @staticmethod
    def register_user(validated_data):
        """
        Handles user registration logic.
        """
        UserService.validate_phone_number(validated_data.get('phone'))
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data.get('full_name', ''),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def update_user_profile(user, validated_data):
        """
        Handles profile update logic.
        """
        UserService.validate_phone_number(validated_data.get('phone'))
        
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()
        return user
