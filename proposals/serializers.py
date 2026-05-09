from rest_framework import serializers
from .models import Proposal

class ProposalSerializer(serializers.ModelSerializer):
    entrepreneur_name = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = [
            'id',
            'entrepreneur',
            'entrepreneur_name',
            'title',
            'description',
            'industry',
            'funding_needed',
            'status',
            'founded_year',
            'team_size',
            'revenue_milestone',
            'achievements',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['entrepreneur', 'status', 'created_at', 'updated_at']

    def get_entrepreneur_name(self, obj):
        return obj.entrepreneur.username