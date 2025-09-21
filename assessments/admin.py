from django.contrib import admin
from .models import Questionnaire, Question, Choice, UserAssessment, AssessmentResponse


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('title', 'questionnaire_type', 'max_score', 'is_active', 'created_at')
    list_filter = ('questionnaire_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'questionnaire_type', 'description', 'instructions', 'is_active')
        }),
        ('Scoring Configuration', {
            'fields': ('max_score', 'scoring_ranges')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ('text', 'score', 'order')
    ordering = ('order',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'order', 'text_preview', 'question_type', 'is_required')
    list_filter = ('questionnaire', 'question_type', 'is_required')
    search_fields = ('text', 'questionnaire__title')
    ordering = ('questionnaire', 'order')
    inlines = [ChoiceInline]
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question Text'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question_info', 'text', 'score', 'order')
    list_filter = ('question__questionnaire', 'score')
    search_fields = ('text', 'question__text')
    ordering = ('question__questionnaire', 'question__order', 'order')
    
    def question_info(self, obj):
        return f"{obj.question.questionnaire.title} - Q{obj.question.order}"
    question_info.short_description = 'Question'


@admin.register(UserAssessment)
class UserAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'questionnaire', 'status', 'total_score', 'severity_level', 'started_at', 'completed_at')
    list_filter = ('questionnaire', 'status', 'severity_level', 'started_at')
    search_fields = ('user__username', 'user__email', 'questionnaire__title')
    readonly_fields = ('started_at', 'total_score', 'severity_level')
    date_hierarchy = 'started_at'
    
    fieldsets = (
        ('Assessment Info', {
            'fields': ('user', 'questionnaire', 'status')
        }),
        ('Results', {
            'fields': ('total_score', 'severity_level', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('session_info', 'started_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user', 'questionnaire')
        return self.readonly_fields


class AssessmentResponseInline(admin.TabularInline):
    model = AssessmentResponse
    extra = 0
    readonly_fields = ('answered_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question', 'choice')


@admin.register(AssessmentResponse)
class AssessmentResponseAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'question_info', 'choice_text', 'choice_score', 'answered_at')
    list_filter = ('assessment__questionnaire', 'answered_at')
    search_fields = ('assessment__user__username', 'question__text', 'choice__text')
    readonly_fields = ('answered_at',)
    
    def user_info(self, obj):
        return f"{obj.assessment.user.username}"
    user_info.short_description = 'User'
    
    def question_info(self, obj):
        return f"Q{obj.question.order}: {obj.question.text[:50]}..."
    question_info.short_description = 'Question'
    
    def choice_text(self, obj):
        return obj.choice.text
    choice_text.short_description = 'Selected Choice'
    
    def choice_score(self, obj):
        return obj.choice.score
    choice_score.short_description = 'Score'
