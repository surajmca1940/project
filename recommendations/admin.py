from django.contrib import admin
from .models import (
    RecommendationCategory, Recommendation, 
    UserRecommendation, RecommendationTemplate
)


@admin.register(RecommendationCategory)
class RecommendationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'color', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('order', 'name')


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'recommendation_type', 'urgency', 'duration_minutes', 'is_active')
    list_filter = ('category', 'recommendation_type', 'urgency', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'instructions')
    filter_horizontal = ('applicable_questionnaires',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'recommendation_type', 'urgency')
        }),
        ('Content', {
            'fields': ('instructions', 'duration_minutes', 'external_url', 'video_url')
        }),
        ('Targeting', {
            'fields': ('applicable_questionnaires', 'min_score', 'max_score', 'severity_levels')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'status', 'rating', 'suggested_at', 'completed_at')
    list_filter = ('status', 'rating', 'suggested_at', 'recommendation__category')
    search_fields = ('user__username', 'recommendation__title')
    readonly_fields = ('suggested_at', 'viewed_at', 'started_at', 'completed_at')
    date_hierarchy = 'suggested_at'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user', 'recommendation', 'assessment')
        return self.readonly_fields


@admin.register(RecommendationTemplate)
class RecommendationTemplateAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'severity_level', 'is_active')
    list_filter = ('questionnaire', 'severity_level', 'is_active')
    search_fields = ('template_text', 'questionnaire__title')
