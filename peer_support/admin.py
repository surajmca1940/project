from django.contrib import admin
from .models import ForumCategory, ForumPost, ForumReply, PeerVolunteer


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
# Register your models here.
