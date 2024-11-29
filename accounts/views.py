from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser
from .models import CustomUser
from .serializers import UserPromotionSerializer, UserSerializer, UserRegistrationSerializer , UserRoleUpdateSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPromotionView(APIView):
    """
    View to handle user role promotions by admin users
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        """
        Handle user role promotion
        
        Request payload should include:
        - user_id: ID of the user to promote
        - new_role: Role to promote the user to ('moderator' or 'admin')
        """
        serializer = UserPromotionSerializer(data=request.data)
        
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            new_role = serializer.validated_data['new_role']
            
            try:
                user = CustomUser.objects.get(id=user_id)
                
                # Prevent demoting or changing admin roles
                if request.user.role != 'admin':
                    return Response(
                        {"error": "Only admins can promote users"},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Validate new role
                if new_role not in ['moderator', 'admin']:
                    return Response(
                        {"error": "Invalid role. Choose 'moderator' or 'admin'"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Perform role promotion
                user.role = new_role
                user.save()
                
                return Response({
                    "message": f"User {user.username} promoted to {new_role}",
                    "user": UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    """
    View to list users with optional filtering
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        List users with optional role filtering
        Optional query param: role
        """
        role = request.query_params.get('role', None)
        
        if request.user.role != 'admin':
            # Non-admin users can only see limited user information
            users = CustomUser.objects.filter(id=request.user.id)
        else:
            # Admins can see all users, with optional role filtering
            users = CustomUser.objects.all()
            if role:
                users = users.filter(role=role)
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class UserRoleUpdateView(APIView):
    """
    API endpoint for updating user roles (promotion/demotion).
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = UserRoleUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            new_role = serializer.validated_data['new_role']

            try:
                user = CustomUser.objects.get(id=user_id)
                user.role = new_role
                user.save()
                return Response(
                    {"message": f"User {user.username} role updated to {new_role}."},
                    status=HTTP_200_OK
                )
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User not found."},
                    status=HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
