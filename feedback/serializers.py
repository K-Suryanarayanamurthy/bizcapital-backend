from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()
    reviewee_name = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            'id',
            'reviewer',
            'reviewer_name',
            'reviewee',
            'reviewee_name',
            'rating',
            'comment',
            'created_at',
        ]
        read_only_fields = ['reviewer', 'created_at']

    def get_reviewer_name(self, obj):
        return obj.reviewer.username

    def get_reviewee_name(self, obj):
        return obj.reviewee.username

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5!")
        return value