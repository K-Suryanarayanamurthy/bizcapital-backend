from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    UserListView, UpdateProfileView, DeleteAccountView,
    SendOTPView, VerifyOTPView, ResetPasswordView, ChangePasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]