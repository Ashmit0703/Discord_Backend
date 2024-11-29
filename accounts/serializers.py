from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user

class UserPromotionSerializer(serializers.Serializer):
    """
    Serializer for user role promotion
    """
    user_id = serializers.IntegerField()
    new_role = serializers.ChoiceField(
        choices=['moderator', 'admin' , 'user'], 
        required=True
    )

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Registration serializer with role restriction
    """
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
    
    def create(self, validated_data):
        """
        Ensure users can only be created with 'user' role
        """
        # Override role to always be 'user' during registration
        validated_data['role'] = 'user'
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    User serializer with limited information
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['role']  # Prevent direct role modification

class UserRoleUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating user roles (promotion/demotion).
    """
    user_id = serializers.IntegerField()
    new_role = serializers.ChoiceField(
        choices=['admin', 'moderator', 'user'],  # Added 'user' for demotion
        required=True
    )
