from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from assessments.models import Questionnaire, UserAssessment
from datetime import datetime, timedelta


class DashboardMetrics(models.Model):
    """Store aggregated metrics for the wellness dashboard"""
    date = models.DateField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    
    # Counts
    total_assessments = models.PositiveIntegerField(default=0)
    completed_assessments = models.PositiveIntegerField(default=0)
    
    # Severity distribution
    minimal_count = models.PositiveIntegerField(default=0)
    mild_count = models.PositiveIntegerField(default=0)
    moderate_count = models.PositiveIntegerField(default=0)
    moderately_severe_count = models.PositiveIntegerField(default=0)
    severe_count = models.PositiveIntegerField(default=0)
    
    # Statistics
    average_score = models.FloatField(null=True, blank=True)
    median_score = models.FloatField(null=True, blank=True)
    
    # Risk indicators
    high_risk_percentage = models.FloatField(default=0.0, help_text="Percentage needing professional help")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('date', 'questionnaire')
        ordering = ['-date', 'questionnaire']
        verbose_name_plural = "Dashboard Metrics"
    
    def __str__(self):
        return f"{self.date} - {self.questionnaire.title}"
    
    @classmethod
    def calculate_metrics_for_date(cls, date, questionnaire):
        """Calculate and store metrics for a specific date and questionnaire"""
        assessments = UserAssessment.objects.filter(
            questionnaire=questionnaire,
            started_at__date=date,
            status='completed'
        )
        
        if not assessments.exists():
            return None
            
        total_count = assessments.count()
        scores = [a.total_score for a in assessments if a.total_score is not None]
        
        if not scores:
            return None
            
        # Calculate severity distribution
        severity_counts = {
            'minimal': 0,
            'mild': 0,
            'moderate': 0,
            'moderately_severe': 0,
            'severe': 0
        }
        
        for assessment in assessments:
            if assessment.severity_level in severity_counts:
                severity_counts[assessment.severity_level] += 1
        
        # Calculate high risk percentage (moderate and above)
        high_risk_count = (
            severity_counts['moderate'] + 
            severity_counts['moderately_severe'] + 
            severity_counts['severe']
        )
        high_risk_percentage = (high_risk_count / total_count) * 100 if total_count > 0 else 0
        
        # Calculate average score
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Calculate median score
        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        if n % 2 == 0:
            median_score = (sorted_scores[n//2-1] + sorted_scores[n//2]) / 2
        else:
            median_score = sorted_scores[n//2]
        
        # Create or update metrics
        metrics, created = cls.objects.update_or_create(
            date=date,
            questionnaire=questionnaire,
            defaults={
                'total_assessments': total_count,
                'completed_assessments': total_count,
                'minimal_count': severity_counts['minimal'],
                'mild_count': severity_counts['mild'],
                'moderate_count': severity_counts['moderate'],
                'moderately_severe_count': severity_counts['moderately_severe'],
                'severe_count': severity_counts['severe'],
                'average_score': avg_score,
                'median_score': median_score,
                'high_risk_percentage': high_risk_percentage,
            }
        )
        
        return metrics


class InstitutionMetrics(models.Model):
    """Store aggregated metrics by institution (if applicable)"""
    date = models.DateField()
    institution_name = models.CharField(max_length=200, blank=True, help_text="Institution identifier")
    
    # Overall statistics
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0, help_text="Users who took assessment in last 30 days")
    total_assessments = models.PositiveIntegerField(default=0)
    
    # Risk categories
    users_needing_counselling = models.PositiveIntegerField(default=0)
    users_high_stress = models.PositiveIntegerField(default=0)
    users_poor_sleep = models.PositiveIntegerField(default=0)
    users_depression_risk = models.PositiveIntegerField(default=0)
    users_anxiety_risk = models.PositiveIntegerField(default=0)
    
    # Engagement metrics
    avg_assessments_per_user = models.FloatField(default=0.0)
    completion_rate = models.FloatField(default=0.0, help_text="Percentage of started assessments completed")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('date', 'institution_name')
        ordering = ['-date', 'institution_name']
        verbose_name_plural = "Institution Metrics"
    
    def __str__(self):
        return f"{self.date} - {self.institution_name or 'All Institutions'}"


class AlertThreshold(models.Model):
    """Define thresholds for dashboard alerts"""
    METRIC_CHOICES = (
        ('high_risk_percentage', 'High Risk Percentage'),
        ('severe_count', 'Severe Cases Count'),
        ('completion_rate', 'Assessment Completion Rate'),
        ('users_needing_counselling', 'Users Needing Counselling'),
    )
    
    COMPARISON_CHOICES = (
        ('gt', 'Greater Than'),
        ('lt', 'Less Than'),
        ('eq', 'Equals'),
    )
    
    name = models.CharField(max_length=200)
    metric = models.CharField(max_length=50, choices=METRIC_CHOICES)
    comparison = models.CharField(max_length=2, choices=COMPARISON_CHOICES)
    threshold_value = models.FloatField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Notification settings
    email_recipients = models.TextField(blank=True, help_text="Comma-separated email addresses")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Alert Thresholds"
    
    def __str__(self):
        return f"{self.name} ({self.metric} {self.comparison} {self.threshold_value})"
    
    def check_threshold(self, metrics):
        """Check if current metrics trigger this threshold"""
        if not self.is_active:
            return False
            
        if hasattr(metrics, self.metric):
            current_value = getattr(metrics, self.metric)
            
            if self.comparison == 'gt' and current_value > self.threshold_value:
                return True
            elif self.comparison == 'lt' and current_value < self.threshold_value:
                return True
            elif self.comparison == 'eq' and current_value == self.threshold_value:
                return True
                
        return False


class DashboardAlert(models.Model):
    """Store triggered dashboard alerts"""
    SEVERITY_CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    )
    
    threshold = models.ForeignKey(AlertThreshold, on_delete=models.CASCADE, related_name='alerts')
    triggered_at = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='warning')
    message = models.TextField()
    
    # Alert context
    current_value = models.FloatField()
    threshold_value = models.FloatField()
    date = models.DateField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, null=True, blank=True)
    
    # Resolution
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-triggered_at']
        verbose_name_plural = "Dashboard Alerts"
    
    def __str__(self):
        return f"{self.threshold.name} - {self.triggered_at.date()} ({self.severity})"
