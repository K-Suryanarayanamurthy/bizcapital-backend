from django.urls import path
from .views import ProposalCreateView, ProposalListView, ProposalDetailView

urlpatterns = [
    path('create/', ProposalCreateView.as_view(), name='proposal-create'),
    path('list/', ProposalListView.as_view(), name='proposal-list'),
    path('<int:pk>/', ProposalDetailView.as_view(), name='proposal-detail'),
]