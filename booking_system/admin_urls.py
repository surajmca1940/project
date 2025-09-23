"""
URL configuration for booking system admin views
"""

from django.urls import path
from . import admin_views

app_name = 'booking_system_admin'

urlpatterns = [
    # Dashboard views
    path('dashboard/', admin_views.booking_dashboard, name='dashboard'),
    path('dashboard/stats/', admin_views.get_dashboard_stats, name='dashboard_stats'),
    
    # Quick actions
    path('quick-action/', admin_views.quick_appointment_action, name='quick_action'),
    
    # Performance views
    path('counselors-performance/', admin_views.counselor_performance, name='counselors_performance'),
    path('counselor-performance/<int:counselor_id>/', admin_views.counselor_performance, name='counselor_performance'),
    
    # System health
    path('health/', admin_views.system_health_check, name='system_health'),
]