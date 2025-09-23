"""
Custom Django Admin Configuration
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.template.response import TemplateResponse
from django.urls import path
from django.db.models import Count
from django.contrib.admin.models import LogEntry
from django.apps import apps


class CustomAdminSite(AdminSite):
    """Custom Admin Site with Dashboard"""
    
    site_header = "Custom Admin Dashboard"
    site_title = "Admin Portal"
    index_title = "Dashboard Overview"
    
    def __init__(self, name='custom_admin'):
        super().__init__(name)
    
    def get_urls(self):
        """Override to add custom dashboard URL"""
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Custom dashboard view with widgets"""
        context = {
            'title': 'Dashboard',
            'site_title': self.site_title,
            'site_header': self.site_header,
            'has_permission': request.user.is_active and request.user.is_staff,
        }
        
        if request.user.is_active and request.user.is_staff:
            # Get statistics for registered models
            model_stats = []
            for model, model_admin in self._registry.items():
                try:
                    count = model.objects.count()
                    model_stats.append({
                        'name': model._meta.verbose_name_plural.title(),
                        'count': count,
                        'model_name': model._meta.model_name,
                        'app_label': model._meta.app_label,
                        'icon': self.get_model_icon(model),
                    })
                except Exception:
                    continue
            
            # Get recent actions
            recent_actions = LogEntry.objects.select_related('content_type', 'user').order_by('-action_time')[:10]
            
            # Get user statistics
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            staff_users = User.objects.filter(is_staff=True).count()
            superusers = User.objects.filter(is_superuser=True).count()
            
            context.update({
                'model_stats': model_stats,
                'recent_actions': recent_actions,
                'user_stats': {
                    'total': total_users,
                    'active': active_users,
                    'staff': staff_users,
                    'superusers': superusers,
                },
                'total_models': len(model_stats),
            })
        
        return TemplateResponse(request, 'admin/custom_dashboard.html', context)
    
    def get_model_icon(self, model):
        """Get appropriate icon for model based on name"""
        model_name = model._meta.model_name.lower()
        icons = {
            'user': 'fas fa-users',
            'group': 'fas fa-users-cog',
            'logentry': 'fas fa-history',
            'session': 'fas fa-clock',
            'contenttype': 'fas fa-cog',
            'permission': 'fas fa-key',
            'counselor': 'fas fa-user-md',
            'appointment': 'fas fa-calendar-alt',
            'availableslot': 'fas fa-calendar-check',
            'chatsession': 'fas fa-comments',
            'chatmessage': 'fas fa-comment',
            'copingstrategy': 'fas fa-lightbulb',
            'resource': 'fas fa-book',
            'resourcecategory': 'fas fa-folder',
            'forumpost': 'fas fa-comments',
            'forumreply': 'fas fa-reply',
            'forumcategory': 'fas fa-tags',
            'alert': 'fas fa-bell',
            'systemhealth': 'fas fa-heartbeat',
            'moodentry': 'fas fa-smile',
            'sleepentry': 'fas fa-bed',
            'institution': 'fas fa-building',
            'region': 'fas fa-globe',
        }
        return icons.get(model_name, 'fas fa-database')
    
    def index(self, request, extra_context=None):
        """Override default admin index to redirect to custom dashboard"""
        if request.user.is_authenticated and request.user.is_staff:
            return self.dashboard_view(request)
        return super().index(request, extra_context)


# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register all models that are registered with the default admin
def register_all_models():
    """Register all models from default admin to custom admin"""
    from django.contrib import admin as default_admin
    
    # Copy registrations from default admin
    for model, model_admin in default_admin.site._registry.items():
        if not custom_admin_site.is_registered(model):
            # Create a new admin class instance or use the existing one
            try:
                custom_admin_site.register(model, model_admin.__class__)
            except:
                custom_admin_site.register(model)

# Auto-register models when this module is imported
register_all_models()