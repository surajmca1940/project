from django.contrib import admin
from .models import (
    DashboardMetrics, InstitutionMetrics, 
    AlertThreshold, DashboardAlert
)


@admin.register(DashboardMetrics)
class DashboardMetricsAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'questionnaire', 'total_assessments', 'completed_assessments', 
        'high_risk_percentage', 'average_score'
    )
    list_filter = ('date', 'questionnaire', 'questionnaire__questionnaire_type')
    search_fields = ('questionnaire__title',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ('-date', 'questionnaire')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('date', 'questionnaire')
        }),
        ('Assessment Counts', {
            'fields': ('total_assessments', 'completed_assessments')
        }),
        ('Severity Distribution', {
            'fields': (
                'minimal_count', 'mild_count', 'moderate_count', 
                'moderately_severe_count', 'severe_count'
            )
        }),
        ('Statistics', {
            'fields': ('average_score', 'median_score', 'high_risk_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(InstitutionMetrics)
class InstitutionMetricsAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'institution_name', 'total_users', 'active_users',
        'total_assessments', 'completion_rate'
    )
    list_filter = ('date', 'institution_name')
    search_fields = ('institution_name',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ('-date', 'institution_name')


@admin.register(AlertThreshold)
class AlertThresholdAdmin(admin.ModelAdmin):
    list_display = ('name', 'metric', 'comparison', 'threshold_value', 'questionnaire', 'is_active')
    list_filter = ('metric', 'comparison', 'is_active', 'questionnaire')
    search_fields = ('name', 'email_recipients')
    readonly_fields = ('created_at',)


@admin.register(DashboardAlert)
class DashboardAlertAdmin(admin.ModelAdmin):
    list_display = (
        'threshold', 'severity', 'current_value', 'threshold_value', 
        'date', 'is_resolved', 'triggered_at'
    )
    list_filter = ('severity', 'is_resolved', 'triggered_at', 'questionnaire')
    search_fields = ('message', 'threshold__name')
    readonly_fields = ('triggered_at',)
    date_hierarchy = 'triggered_at'
    ordering = ('-triggered_at',)
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('threshold', 'severity', 'message')
        }),
        ('Values', {
            'fields': ('current_value', 'threshold_value', 'date', 'questionnaire')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_at', 'resolved_by', 'resolution_notes')
        }),
        ('Timestamps', {
            'fields': ('triggered_at',),
            'classes': ('collapse',)
        })
    )
