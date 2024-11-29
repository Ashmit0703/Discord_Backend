from django.urls import path
from .views import TextMessageView, TextMessageDeletionView

urlpatterns = [
    path('', TextMessageView.as_view(), name='text-messages'),
    path('delete/<int:message_id>/', TextMessageDeletionView.as_view(), name='delete-message'),
]