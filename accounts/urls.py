from django.urls import path
from .views import UserRegistrationView, UserPromotionView, UserListView , UserRoleUpdateView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='user_signup'),
    path('promote/', UserPromotionView.as_view(), name='user_promote'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('update-role/', UserRoleUpdateView.as_view(), name='update-role'),
]
