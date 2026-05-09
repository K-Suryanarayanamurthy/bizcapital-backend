from django.db import models
from accounts.models import User

class Proposal(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('funded', 'Funded'),
    )

    INDUSTRY_CHOICES = (
        ('tech', 'Technology'),
        ('health', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('other', 'Other'),
    )

    entrepreneur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='proposals'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    funding_needed = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    # New entrepreneur fields
    founded_year = models.IntegerField(blank=True, null=True)
    team_size = models.IntegerField(blank=True, null=True)
    revenue_milestone = models.CharField(max_length=255, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.entrepreneur.username}"