from django.db import models
from accounts.models import User

class Feedback(models.Model):
    RATING_CHOICES = (
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_feedback'
    )
    reviewee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_feedback'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['reviewer', 'reviewee']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewee.username} ({self.rating}⭐)"