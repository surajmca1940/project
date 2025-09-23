from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.admin.models import LogEntry
from django.template.response import TemplateResponse
from django.urls import reverse


class CustomAdminSite(AdminSite):
    site_header = "Mental Health Platform Admin"
    site_title = "DPIS Admin"
    index_title = "Dashboard"
    
    def each_context(self, request):
        """
        Add custom context to all admin templates
        """
        context = super().each_context(request)
        
        # Add model admin URLs for sidebar
        model_admin_urls = []
        for model, model_admin in self._registry.items():
            # Skip built-in auth models for content section
            if model not in [User, Group, LogEntry]:
                app_label = model._meta.app_label
                model_name = model._meta.model_name
                
                # Get appropriate icon for the model
                icon = self.get_model_icon(model_name)
                
                # Get object count
                try:
                    count = model.objects.count()
                except:
                    count = 0
                
                model_admin_urls.append({
                    'name': model._meta.verbose_name_plural.title(),
                    'url': reverse(f'admin:{app_label}_{model_name}_changelist'),
                    'icon': icon,
                    'count': count,
                })
        
        # Get user count for the badge
        try:
            user_count = User.objects.count()
        except:
            user_count = 0
            
        # Get recent admin log entries
        try:
            admin_log_entries = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
        except:
            admin_log_entries = []
        
        context.update({
            'model_admin_urls': model_admin_urls,
            'user_count': user_count,
            'admin_log_entries': admin_log_entries,
        })
        
        return context
    
    def get_model_icon(self, model_name):
        """
        Get appropriate FontAwesome icon for model
        """
        icon_mapping = {
            'user': 'fas fa-users',
            'group': 'fas fa-users-cog',
            'chatsession': 'fas fa-comments',
            'chatmessage': 'fas fa-comment',
            'counselor': 'fas fa-user-md',
            'appointment': 'fas fa-calendar-check',
            'availableslot': 'fas fa-clock',
            'copingstrategy': 'fas fa-lightbulb',
            'resource': 'fas fa-book',
            'logentry': 'fas fa-history',
        }
        
        return icon_mapping.get(model_name.lower(), 'fas fa-database')

    def index(self, request, extra_context=None):
        """
        Custom admin index view with enhanced context
        """
        context = {
            'title': self.index_title,
        }
        if extra_context:
            context.update(extra_context)
            
        return super().index(request, context)


# Create an instance of our custom admin site
# admin_site = CustomAdminSite(name='customadmin')

# For now, let's just override the default admin site context
# We'll monkey patch the admin site to add our custom context
original_each_context = admin.site.each_context

def custom_each_context(request):
    context = original_each_context(request)
    
    # Add model admin URLs for sidebar
    model_admin_urls = []
    for model, model_admin in admin.site._registry.items():
        # Skip built-in auth models for content section
        if model not in [User, Group, LogEntry]:
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            
            # Get appropriate icon for the model
            icon_mapping = {
                'user': 'fas fa-users',
                'group': 'fas fa-users-cog',
                'chatsession': 'fas fa-comments',
                'chatmessage': 'fas fa-comment',
                'counselor': 'fas fa-user-md',
                'appointment': 'fas fa-calendar-check',
                'availableslot': 'fas fa-clock',
                'copingstrategy': 'fas fa-lightbulb',
                'resource': 'fas fa-book',
                'logentry': 'fas fa-history',
            }
            icon = icon_mapping.get(model_name.lower(), 'fas fa-database')
            
            # Get object count
            try:
                count = model.objects.count()
            except:
                count = 0
            
            model_admin_urls.append({
                'name': model._meta.verbose_name_plural.title(),
                'url': reverse(f'admin:{app_label}_{model_name}_changelist'),
                'icon': icon,
                'count': count,
            })
    
    # Get user count for the badge
    try:
        user_count = User.objects.count()
    except:
        user_count = 0
        
    # Get recent admin log entries
    try:
        admin_log_entries = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
    except:
        admin_log_entries = []
    
    context.update({
        'model_admin_urls': model_admin_urls,
        'user_count': user_count,
        'admin_log_entries': admin_log_entries,
    })
    
    return context

# Register LogEntry model in admin
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('action_time', 'content_type', 'action_flag')
    search_fields = ('object_repr', 'change_message')
    readonly_fields = ('action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# Register LogEntry model
admin.site.register(LogEntry, LogEntryAdmin)

# Monkey patch the admin site
admin.site.each_context = custom_each_context
admin.site.site_header = "Mental Health Platform Admin"
admin.site.site_title = "DPIS Admin" 
admin.site.index_title = "Dashboard"
