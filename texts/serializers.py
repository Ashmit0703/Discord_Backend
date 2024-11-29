from rest_framework import serializers
from .models import TextMessage
from accounts.serializers import UserSerializer

class TextMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TextMessage
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']