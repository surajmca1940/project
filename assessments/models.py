from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class Questionnaire(models.Model):
    """Model for different types of psychological assessments"""
    QUESTIONNAIRE_TYPES = (
        ('PHQ9', 'PHQ-9 (Depression)'),
        ('GAD7', 'GAD-7 (Anxiety)'),
        ('SQI', 'Sleep Quality Index'),
        ('PSS', 'Perceived Stress Scale'),
        ('DASS21', 'DASS-21 (Depression, Anxiety, Stress)'),
    )
    
    SEVERITY_LEVELS = (
        ('minimal', 'Minimal'),
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('moderately_severe', 'Moderately Severe'),
        ('severe', 'Severe'),
    )
    
    title = models.CharField(max_length=200)
    questionnaire_type = models.CharField(max_length=10, choices=QUESTIONNAIRE_TYPES)
    description = models.TextField()
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Scoring configuration
    max_score = models.IntegerField(default=0)
    scoring_ranges = models.JSONField(default=dict, help_text="JSON field storing score ranges for each severity level")
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Questionnaires"
    
    def __str__(self):
        return self.title
    
    def get_severity_level(self, score):
        """Determine severity level based on score"""
        for level, range_info in self.scoring_ranges.items():
            if range_info['min'] <= score <= range_info['max']:
                return level
        return 'unknown'


class Question(models.Model):
    """Individual questions within a questionnaire"""
    QUESTION_TYPES = (
        ('likert', 'Likert Scale (0-3 or 0-4)'),
        ('boolean', 'Yes/No'),
        ('multiple_choice', 'Multiple Choice'),
        ('rating', 'Rating Scale'),
    )
    
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='likert')
    order = models.PositiveIntegerField(default=1)
    is_required = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['questionnaire', 'order']
        unique_together = ('questionnaire', 'order')
    
    def __str__(self):
        return f"{self.questionnaire.title} - Q{self.order}: {self.text[:50]}..."


class Choice(models.Model):
    """Answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['question', 'order']
        unique_together = ('question', 'order')
    
    def __str__(self):
        return f"{self.question.questionnaire.title} - Q{self.question.order} - {self.text}"


class UserAssessment(models.Model):
    """Record of a user taking an assessment"""
    STATUS_CHOICES = (
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments')
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Results
    total_score = models.IntegerField(null=True, blank=True)
    severity_level = models.CharField(max_length=20, blank=True)
    
    # Metadata
    session_info = models.JSONField(default=dict, blank=True, help_text="Browser, IP, etc.")
    
    class Meta:
        ordering = ['-started_at']
        verbose_name_plural = "User Assessments"
    
    def __str__(self):
        return f"{self.user.username} - {self.questionnaire.title} ({self.status})"
    
    def calculate_score(self):
        """Calculate total score from all responses"""
        total = sum(response.choice.score for response in self.responses.all())
        self.total_score = total
        self.severity_level = self.questionnaire.get_severity_level(total)
        self.save()
        return total


class AssessmentResponse(models.Model):
    """Individual responses to assessment questions"""
    assessment = models.ForeignKey(UserAssessment, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('assessment', 'question')
        ordering = ['assessment', 'question__order']
    
    def __str__(self):
        return f"{self.assessment.user.username} - Q{self.question.order}: {self.choice.text}"
