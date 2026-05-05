from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Feedback
from .serializers import FeedbackSerializer
from accounts.models import User

class GiveFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reviewee_id = request.data.get('reviewee')
        try:
            reviewee = User.objects.get(id=reviewee_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        if reviewee == request.user:
            return Response(
                {"error": "You cannot give feedback to yourself!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Feedback.objects.filter(
            reviewer=request.user,
            reviewee=reviewee
        ).exists():
            return Response(
                {"error": "You have already given feedback to this user!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reviewer=request.user)
            return Response(
                {"message": "Feedback submitted successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFeedbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        feedback = Feedback.objects.filter(reviewee=user)
        serializer = FeedbackSerializer(feedback, many=True)
        total = feedback.count()
        if total > 0:
            average = sum([f.rating for f in feedback]) / total
        else:
            average = 0
        return Response({
            "user": user.username,
            "total_reviews": total,
            "average_rating": round(average, 2),
            "feedback": serializer.data
        }, status=status.HTTP_200_OK)