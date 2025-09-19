from django.contrib import admin
from .models import ChatSession, ChatMessage, CopingStrategy


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['timestamp']
    fields = ['message_type', 'content', 'timestamp']
    

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['session_id', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    inlines = [ChatMessageInline]
    date_hierarchy = 'created_at'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content', 'session__session_id']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('session')


@admin.register(CopingStrategy)
class CopingStrategyAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'language', 'created_at']
    list_filter = ['category', 'language', 'created_at']
    search_fields = ['title', 'description', 'category']
    readonly_fields = ['created_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'category', 'language']
        }),
        ('Content', {
            'fields': ['description']
        }),
        ('Metadata', {
            'fields': ['created_at'],
            'classes': ['collapse']
        })
    ]
# Register your models here.
