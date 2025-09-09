from django.db import models
from django.contrib.auth.models import User

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('ai_chat', 'AI Chat Session'),
        ('appointment', 'Appointment Booking'),
        ('resource_view', 'Resource Viewed'),
        ('forum_post', 'Forum Post'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"{username} - {self.activity_type}"

class MentalHealthMetric(models.Model):
    date = models.DateField()
    total_users = models.IntegerField(default=0)
    active_sessions = models.IntegerField(default=0)
    appointments_booked = models.IntegerField(default=0)
    resources_accessed = models.IntegerField(default=0)
    forum_posts = models.IntegerField(default=0)
    crisis_indicators = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['date']
        ordering = ['-date']
    
    def __str__(self):
        return f"Metrics for {self.date}"

class Alert(models.Model):
    ALERT_TYPES = [
        ('crisis', 'Crisis Alert'),
        ('high_usage', 'High Usage'),
        ('system', 'System Alert'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type}: {self.title}"
