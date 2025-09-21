from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DashboardMetrics, InstitutionMetrics, AlertThreshold, DashboardAlert
from assessments.serializers import QuestionnaireListSerializer


class DashboardMetricsSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireListSerializer(read_only=True)
    
    class Meta:
        model = DashboardMetrics
        fields = [
            'id', 'date', 'questionnaire', 'total_assessments', 'completed_assessments',
            'minimal_count', 'mild_count', 'moderate_count', 'moderately_severe_count',
            'severe_count', 'average_score', 'median_score', 'high_risk_percentage'
        ]


class InstitutionMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionMetrics
        fields = [
            'id', 'date', 'institution_name', 'total_users', 'active_users',
            'total_assessments', 'users_needing_counselling', 'users_high_stress',
            'users_poor_sleep', 'users_depression_risk', 'users_anxiety_risk',
            'avg_assessments_per_user', 'completion_rate'
        ]


class DashboardSummarySerializer(serializers.Serializer):
    """Serializer for dashboard summary statistics"""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_assessments = serializers.IntegerField()
    completed_assessments = serializers.IntegerField()
    completion_rate = serializers.FloatField()
    
    # Risk indicators
    high_risk_users = serializers.IntegerField()
    users_needing_counselling = serializers.IntegerField()
    severe_cases = serializers.IntegerField()
    
    # By questionnaire type
    assessments_by_type = serializers.DictField()
    risk_distribution = serializers.DictField()


class SeverityDistributionSerializer(serializers.Serializer):
    """Serializer for severity level distribution"""
    questionnaire_type = serializers.CharField()
    minimal = serializers.IntegerField()
    mild = serializers.IntegerField()
    moderate = serializers.IntegerField()
    moderately_severe = serializers.IntegerField()
    severe = serializers.IntegerField()
    total = serializers.IntegerField()


class TrendDataSerializer(serializers.Serializer):
    """Serializer for trend analysis data"""
    date = serializers.DateField()
    value = serializers.FloatField()
    questionnaire_type = serializers.CharField()


class AlertThresholdSerializer(serializers.ModelSerializer):
    questionnaire = QuestionnaireListSerializer(read_only=True)
    
    class Meta:
        model = AlertThreshold
        fields = [
            'id', 'name', 'metric', 'comparison', 'threshold_value',
            'questionnaire', 'is_active', 'email_recipients'
        ]


class DashboardAlertSerializer(serializers.ModelSerializer):
    threshold = AlertThresholdSerializer(read_only=True)
    questionnaire = QuestionnaireListSerializer(read_only=True)
    
    class Meta:
        model = DashboardAlert
        fields = [
            'id', 'threshold', 'triggered_at', 'severity', 'message',
            'current_value', 'threshold_value', 'date', 'questionnaire',
            'is_resolved', 'resolved_at', 'resolved_by', 'resolution_notes'
        ]
        read_only_fields = ['triggered_at']


class ChartDataSerializer(serializers.Serializer):
    """Generic serializer for chart data"""
    labels = serializers.ListField(child=serializers.CharField())
    datasets = serializers.ListField(
        child=serializers.DictField()
    )
    title = serializers.CharField()
    type = serializers.CharField()  # chart type: bar, line, pie, doughnut