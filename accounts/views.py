# BizCapital API Views - Updated
from rest_framework import status
from .models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer,ProfileSerializer, UpdateProfileSerializer
import resend
from django.conf import settings


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "role": user.role,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.query_params.get('role', None)
        
        # Exclude the current logged in user and users with no role
        users = User.objects.exclude(id=request.user.id).exclude(role='')
        
        # Filter by role if provided
        if role:
            users = users.filter(role=role)
        
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated successfully!", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {"message": "Account deleted successfully!"},
            status=status.HTTP_200_OK
        )
    
from .models import OTP

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.filter(email=email.strip()).first()
            if not user:
                return Response(
                    {"error": "No account found with this email!"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        try:
            otp_obj = OTP.generate_otp(user)
            resend.api_key = settings.RESEND_API_KEY

            params = {
                "from": "onboarding@resend.dev",
                "to": [email],
                "subject": "BizCapital - Password Reset OTP",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #1a56db;">BizCapital Password Reset</h2>
                    <p>Hello <strong>{user.username}</strong>!</p>
                    <p>Your OTP for password reset is:</p>
                    <div style="background: #f0f4ff; padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0;">
                        <h1 style="color: #1a56db; font-size: 40px; letter-spacing: 10px;">{otp_obj.otp}</h1>
                    </div>
                    <p>This OTP is valid for <strong>10 minutes</strong> only.</p>
                    <p>If you did not request this, please ignore this email.</p>
                    <br>
                    <p>Best regards,<br><strong>BizCapital Team</strong></p>
                </div>
                """
            }

            email_response = resend.Emails.send(params)
            return Response(
                {"message": "OTP sent successfully!", "resend_id": str(email_response)},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')

        user = User.objects.filter(email=email.strip()).first()
        if not user:
            return Response(
                {"error": "No account found with this email!"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            otp_obj = OTP.objects.filter(
                user=user,
                otp=otp_code,
                is_used=False
            ).latest('created_at')
        except OTP.DoesNotExist:
            return Response(
                {"error": "Invalid OTP!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not otp_obj.is_valid():
            return Response(
                {"error": "OTP has expired! Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_obj.is_used = True
        otp_obj.save()

        return Response(
            {"message": "OTP verified successfully!"},
            status=status.HTTP_200_OK
        )

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        user = User.objects.filter(email=email.strip()).first()
        if not user:
            return Response(
                {"error": "No account found with this email!"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password reset successfully! Please login with your new password."},
            status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not request.user.check_password(old_password):
            return Response(
                {"error": "Current password is incorrect!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.set_password(new_password)
        request.user.save()

        return Response(
            {"message": "Password changed successfully! Please login again."},
            status=status.HTTP_200_OK
        )