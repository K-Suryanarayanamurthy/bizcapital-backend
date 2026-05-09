from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('investor', 'Investor'),
        ('entrepreneur', 'Entrepreneur'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Investor specific fields
    investment_min = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    investment_max = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    investment_industries = models.CharField(
        max_length=255, blank=True, null=True
    )
    portfolio_companies = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"