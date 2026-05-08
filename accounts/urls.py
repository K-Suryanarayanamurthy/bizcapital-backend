from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UserListView, UpdateProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
]