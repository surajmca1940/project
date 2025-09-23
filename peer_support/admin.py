from django.contrib import admin
from .models import (
    ForumCategory, ForumPost, ForumReply, PeerVolunteer,
    Tag, ForumThread, Reply, Vote
)


class ForumReplyInline(admin.TabularInline):
    model = ForumReply
    extra = 0
    readonly_fields = ['created_at']
    fields = ['author', 'content', 'is_anonymous', 'is_moderated', 'created_at']


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_anonymous', 'is_moderated', 'created_at']
    list_filter = ['category', 'is_anonymous', 'is_moderated', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['is_moderated']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [ForumReplyInline]
    fieldsets = [
        ('Post Information', {
            'fields': ['title', 'content', 'author', 'category']
        }),
        ('Settings', {
            'fields': ['is_anonymous', 'is_moderated']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content_preview', 'is_anonymous', 'is_moderated', 'created_at']
    list_filter = ['is_anonymous', 'is_moderated', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    list_editable = ['is_moderated']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('post', 'author')


@admin.register(PeerVolunteer)
class PeerVolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_trained', 'training_date', 'is_active']
    list_filter = ['is_trained', 'is_active', 'training_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialties']
    list_editable = ['is_active', 'is_trained']
    date_hierarchy = 'training_date'
    fieldsets = [
        ('Volunteer Information', {
            'fields': ['user']
        }),
        ('Training', {
            'fields': ['is_trained', 'training_date', 'specialties']
        }),
        ('Status', {
            'fields': ['is_active']
        })
    ]
# New enhanced models
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'get_thread_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    list_per_page = 50
    
    def get_thread_count(self, obj):
        return obj.get_thread_count()
    get_thread_count.short_description = 'Thread Count'

@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'get_display_author', 'is_pinned', 'is_locked', 'is_active', 'view_count', 'get_reply_count', 'created_at']
    list_filter = ['is_anonymous', 'is_pinned', 'is_locked', 'is_active', 'created_at', 'tags']
    search_fields = ['title', 'content', 'author__username']
    raw_id_fields = ['author']
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'last_activity']
    filter_horizontal = ['tags']
    list_editable = ['is_pinned', 'is_locked', 'is_active']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = [
        ('Thread Information', {
            'fields': ['title', 'content', 'author', 'tags']
        }),
        ('Settings', {
            'fields': ['is_anonymous', 'is_pinned', 'is_locked', 'is_active']
        }),
        ('Statistics', {
            'fields': ['view_count', 'created_at', 'updated_at', 'last_activity'],
            'classes': ['collapse']
        })
    ]
    
    def get_reply_count(self, obj):
        return obj.get_reply_count()
    get_reply_count.short_description = 'Replies'

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'get_display_author', 'content_preview', 'is_anonymous', 'is_active', 'created_at']
    list_filter = ['is_anonymous', 'is_active', 'created_at']
    search_fields = ['content', 'author__username', 'thread__title']
    raw_id_fields = ['author', 'thread', 'parent']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 100
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    fieldsets = [
        ('Reply Information', {
            'fields': ['thread', 'content', 'author', 'parent']
        }),
        ('Settings', {
            'fields': ['is_anonymous', 'is_active']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'vote_type', 'get_target', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'thread__title', 'reply__content']
    raw_id_fields = ['user', 'thread', 'reply']
    readonly_fields = ['created_at']
    list_per_page = 100
    date_hierarchy = 'created_at'
    
    def get_target(self, obj):
        if obj.thread:
            return f'Thread: {obj.thread.title}'
        elif obj.reply:
            return f'Reply to: {obj.reply.thread.title}'
        return 'Unknown'
    get_target.short_description = 'Target'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'thread', 'reply')
