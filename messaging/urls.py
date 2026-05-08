from django.urls import path
from .views import SendMessageView, InboxView, SentMessagesView, ConversationView, UnreadCountView, MarkAsReadView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('sent/', SentMessagesView.as_view(), name='sent-messages'),
    path('conversation/<int:user_id>/', ConversationView.as_view(), name='conversation'),
    path('unread-count/', UnreadCountView.as_view(), name='unread-count'),
    path('mark-read/<int:user_id>/', MarkAsReadView.as_view(), name='mark-read'),
]