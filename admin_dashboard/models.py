from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Institution, Region

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
        ('counselor_overload', 'Counselor Overload'),
        ('regional_spike', 'Regional Activity Spike'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type}: {self.title}"


class RealTimeMetric(models.Model):
    """Store real-time metrics for live dashboard updates"""
    METRIC_TYPES = [
        ('active_users', 'Active Users'),
        ('ai_sessions', 'AI Chat Sessions'),
        ('appointments_today', 'Appointments Today'),
        ('crisis_interventions', 'Crisis Interventions'),
        ('resource_downloads', 'Resource Downloads'),
        ('peer_support_posts', 'Peer Support Posts'),
        ('counselor_availability', 'Counselor Availability'),
    ]
    
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    value = models.FloatField()
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metric_type', 'timestamp']),
            models.Index(fields=['institution', 'timestamp']),
            models.Index(fields=['region', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.metric_type}: {self.value} at {self.timestamp}"


class DashboardWidget(models.Model):
    """Configurable widgets for admin dashboard"""
    WIDGET_TYPES = [
        ('chart', 'Chart Widget'),
        ('stat', 'Statistics Widget'),
        ('alert', 'Alert Widget'),
        ('map', 'Regional Map Widget'),
        ('list', 'List Widget'),
    ]
    
    CHART_TYPES = [
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('area', 'Area Chart'),
    ]
    
    title = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPES, blank=True)
    position = models.IntegerField(default=0, help_text="Display order on dashboard")
    is_active = models.BooleanField(default=True)
    
    # Configuration
    config = models.JSONField(default=dict, help_text="Widget-specific configuration")
    refresh_interval = models.IntegerField(default=30, help_text="Refresh interval in seconds")
    
    # Filters
    institution_filter = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    region_filter = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.widget_type})"


class SystemHealth(models.Model):
    """Track system health metrics for monitoring"""
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    database_connections = models.IntegerField()
    response_time = models.FloatField(help_text="Average response time in milliseconds")
    error_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"System Health at {self.timestamp}"


class RegionalAnalytics(models.Model):
    """Regional-specific analytics for cultural context awareness"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField(default=timezone.now)
    
    # Usage metrics
    total_active_users = models.IntegerField(default=0)
    language_usage = models.JSONField(default=dict, help_text="Language preference distribution")
    cultural_resource_access = models.JSONField(default=dict, help_text="Cultural resource access patterns")
    peak_usage_hours = models.JSONField(default=list, help_text="Peak usage hours for the region")
    
    # Mental health indicators
    crisis_interventions = models.IntegerField(default=0)
    common_concerns = models.JSONField(default=list, help_text="Most common mental health concerns")
    resource_effectiveness = models.JSONField(default=dict, help_text="Effectiveness ratings of resources")
    
    class Meta:
        unique_together = ['region', 'date']
        ordering = ['-date', 'region']
    
    def __str__(self):
        return f"Analytics for {self.region.name} on {self.date}"
