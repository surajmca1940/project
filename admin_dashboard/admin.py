from django.contrib import admin
from .models import (
    UserActivity, MentalHealthMetric, Alert, RealTimeMetric, 
    DashboardWidget, SystemHealth, RegionalAnalytics
)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(MentalHealthMetric)
class MentalHealthMetricAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_users', 'active_sessions', 'appointments_booked', 'crisis_indicators']
    list_filter = ['date']
    date_hierarchy = 'date'


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['alert_type', 'title', 'institution', 'region', 'severity', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_resolved', 'institution', 'region', 'created_at']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_resolved=True, resolved_at=timezone.now())
    mark_resolved.short_description = "Mark selected alerts as resolved"


@admin.register(RealTimeMetric)
class RealTimeMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'institution', 'region', 'value', 'timestamp']
    list_filter = ['metric_type', 'institution', 'region', 'timestamp']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'widget_type', 'chart_type', 'position', 'is_active', 'refresh_interval']
    list_filter = ['widget_type', 'chart_type', 'is_active', 'institution_filter', 'region_filter']
    search_fields = ['title']
    list_editable = ['position', 'is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SystemHealth)
class SystemHealthAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'cpu_usage', 'memory_usage', 'database_connections', 'response_time', 'error_count']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(RegionalAnalytics)
class RegionalAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['region', 'date', 'total_active_users', 'crisis_interventions']
    list_filter = ['region', 'date']
    readonly_fields = ['date']
    date_hierarchy = 'date'
