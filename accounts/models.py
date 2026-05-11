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
    
import random
from django.utils import timezone

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # OTP expires after 10 minutes
        expiry_time = self.created_at + timezone.timedelta(minutes=10)
        return timezone.now() < expiry_time and not self.is_used

    @classmethod
    def generate_otp(cls, user):
        # Delete old OTPs for this user
        cls.objects.filter(user=user).delete()
        # Generate new 6 digit OTP
        otp_code = str(random.randint(100000, 999999))
        return cls.objects.create(user=user, otp=otp_code)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"