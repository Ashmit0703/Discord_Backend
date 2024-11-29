from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import TextMessage
from .serializers import TextMessageSerializer

from django.utils import timezone
from accounts.permissions import IsAdminUser

class TextMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Send a new text message
        """
        serializer = TextMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Retrieve recent text messages
        """
        messages = TextMessage.objects.all()[:50]  # Limit to last 50 messages
        serializer = TextMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
class TextMessageDeletionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def delete(self, request, message_id):
        try:
            message = TextMessage.objects.get(id=message_id)
            message.delete()
            
            return Response(
                {"message": "Message successfully deleted"},
                status=status.HTTP_200_OK
            )
        
        except TextMessage.DoesNotExist:
            return Response(
                {"error": "Message not found"},
                status=status.HTTP_404_NOT_FOUND
            )