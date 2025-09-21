from django.db import models
from django.contrib.auth.models import User
from assessments.models import Questionnaire, UserAssessment


class RecommendationCategory(models.Model):
    """Categories for different types of recommendations"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or emoji")
    color = models.CharField(max_length=7, default='#6366f1', help_text="Hex color code")
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Recommendation Categories"
    
    def __str__(self):
        return self.name


class Recommendation(models.Model):
    """Individual recommendations for users"""
    RECOMMENDATION_TYPES = (
        ('exercise', 'Exercise & Movement'),
        ('breathing', 'Breathing Exercise'),
        ('meditation', 'Meditation'),
        ('sleep', 'Sleep Hygiene'),
        ('nutrition', 'Nutrition'),
        ('social', 'Social Connection'),
        ('professional', 'Professional Help'),
        ('activity', 'Activity/Hobby'),
        ('mindfulness', 'Mindfulness'),
        ('education', 'Educational Resource'),
    )
    
    URGENCY_LEVELS = (
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent - Seek Professional Help'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(RecommendationCategory, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPES)
    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='medium')
    
    # Content
    instructions = models.TextField(blank=True, help_text="Step-by-step instructions")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, help_text="Estimated time in minutes")
    external_url = models.URLField(blank=True, help_text="Link to external resource")
    video_url = models.URLField(blank=True, help_text="YouTube or other video URL")
    
    # Targeting
    applicable_questionnaires = models.ManyToManyField(Questionnaire, blank=True)
    min_score = models.IntegerField(null=True, blank=True, help_text="Minimum score to show this recommendation")
    max_score = models.IntegerField(null=True, blank=True, help_text="Maximum score to show this recommendation")
    severity_levels = models.JSONField(default=list, help_text="List of severity levels this applies to")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['urgency', 'category', 'title']
    
    def __str__(self):
        return self.title
    
    def is_applicable_for_assessment(self, user_assessment):
        """Check if this recommendation applies to a specific assessment result"""
        # Check questionnaire type
        if self.applicable_questionnaires.exists():
            if user_assessment.questionnaire not in self.applicable_questionnaires.all():
                return False
        
        # Check score range
        if self.min_score is not None and user_assessment.total_score < self.min_score:
            return False
        if self.max_score is not None and user_assessment.total_score > self.max_score:
            return False
            
        # Check severity level
        if self.severity_levels and user_assessment.severity_level not in self.severity_levels:
            return False
            
        return True


class UserRecommendation(models.Model):
    """Track which recommendations have been shown to users"""
    STATUS_CHOICES = (
        ('suggested', 'Suggested'),
        ('viewed', 'Viewed'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('dismissed', 'Dismissed'),
        ('bookmarked', 'Bookmarked'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recommendations')
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    assessment = models.ForeignKey(UserAssessment, on_delete=models.CASCADE, related_name='recommendations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='suggested')
    
    # Interaction tracking
    suggested_at = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Feedback
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="1-5 star rating")
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user', 'recommendation', 'assessment')
        ordering = ['-suggested_at']
        verbose_name_plural = "User Recommendations"
    
    def __str__(self):
        return f"{self.user.username} - {self.recommendation.title} ({self.status})"


class RecommendationTemplate(models.Model):
    """Templates for generating personalized recommendation text"""
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    severity_level = models.CharField(max_length=20)
    template_text = models.TextField(help_text="Use {{username}}, {{score}}, etc. for personalization")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('questionnaire', 'severity_level')
        verbose_name_plural = "Recommendation Templates"
    
    def __str__(self):
        return f"{self.questionnaire.title} - {self.severity_level}"
