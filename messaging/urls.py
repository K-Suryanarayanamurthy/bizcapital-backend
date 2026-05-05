from django.urls import path
from .views import SendMessageView, InboxView, SentMessagesView, ConversationView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('sent/', SentMessagesView.as_view(), name='sent-messages'),
    path('conversation/<int:user_id>/', ConversationView.as_view(), name='conversation'),
]