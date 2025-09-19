from django.contrib import admin
from .models import ResourceCategory, Resource, ResourceView


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name', 'description']
    fieldsets = [
        ('Category Information', {
            'fields': ['name', 'description', 'icon']
        })
    ]


class ResourceViewInline(admin.TabularInline):
    model = ResourceView
    extra = 0
    readonly_fields = ['viewed_at', 'ip_address']
    fields = ['user', 'viewed_at', 'ip_address']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'category', 'language', 'created_by', 'is_active', 'created_at']
    list_filter = ['resource_type', 'category', 'language', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    inlines = [ResourceViewInline]
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'description', 'resource_type', 'category', 'language']
        }),
        ('Files & Links', {
            'fields': ['file_url', 'file_upload', 'duration']
        }),
        ('Metadata', {
            'fields': ['created_by', 'is_active', 'created_at'],
            'classes': ['collapse']
        })
    ]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('category', 'created_by')


@admin.register(ResourceView)
class ResourceViewAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'viewed_at', 'ip_address']
    list_filter = ['viewed_at', 'resource__category', 'resource__resource_type']
    search_fields = ['resource__title', 'user__username', 'ip_address']
    readonly_fields = ['viewed_at']
    date_hierarchy = 'viewed_at'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('resource', 'user')
# Register your models here.
