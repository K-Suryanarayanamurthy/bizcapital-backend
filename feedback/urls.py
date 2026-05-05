from django.urls import path
from .views import GiveFeedbackView, UserFeedbackView

urlpatterns = [
    path('give/', GiveFeedbackView.as_view(), name='give-feedback'),
    path('user/<int:user_id>/', UserFeedbackView.as_view(), name='user-feedback'),
]