from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    RecommendationCategory, Recommendation, 
    UserRecommendation, RecommendationTemplate
)
from assessments.serializers import QuestionnaireListSerializer


class RecommendationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationCategory
        fields = ['id', 'name', 'description', 'icon', 'color', 'order']


class RecommendationSerializer(serializers.ModelSerializer):
    category = RecommendationCategorySerializer(read_only=True)
    applicable_questionnaires = QuestionnaireListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'title', 'description', 'category', 'recommendation_type', 
            'urgency', 'instructions', 'duration_minutes', 'external_url', 
            'video_url', 'applicable_questionnaires', 'min_score', 'max_score',
            'severity_levels'
        ]


class UserRecommendationSerializer(serializers.ModelSerializer):
    recommendation = RecommendationSerializer(read_only=True)
    assessment_date = serializers.DateTimeField(source='assessment.completed_at', read_only=True)
    
    class Meta:
        model = UserRecommendation
        fields = [
            'id', 'recommendation', 'status', 'suggested_at', 'viewed_at', 
            'started_at', 'completed_at', 'rating', 'feedback', 'assessment_date'
        ]
        read_only_fields = ['suggested_at']


class UserRecommendationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating recommendation status and feedback"""
    
    class Meta:
        model = UserRecommendation
        fields = ['status', 'rating', 'feedback']
    
    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        
        # Update timestamps based on status changes
        from django.utils import timezone
        now = timezone.now()
        
        if status == 'viewed' and not instance.viewed_at:
            validated_data['viewed_at'] = now
        elif status == 'started' and not instance.started_at:
            validated_data['started_at'] = now
        elif status == 'completed' and not instance.completed_at:
            validated_data['completed_at'] = now
            
        return super().update(instance, validated_data)


class RecommendationStatsSerializer(serializers.Serializer):
    """Serializer for recommendation statistics"""
    total_recommendations = serializers.IntegerField()
    viewed_count = serializers.IntegerField()
    started_count = serializers.IntegerField()
    completed_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    recommendations_by_category = serializers.DictField()
    urgent_recommendations = serializers.IntegerField()