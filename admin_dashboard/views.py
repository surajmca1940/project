from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_home(request):
    """Admin dashboard homepage"""
    return render(request, 'admin_dashboard/dashboard.html')

@staff_member_required
def user_analytics(request):
    """User analytics and statistics"""
    return render(request, 'admin_dashboard/users.html')

@staff_member_required
def mental_health_metrics(request):
    """Mental health metrics and trends"""
    return render(request, 'admin_dashboard/metrics.html')

@staff_member_required
def alert_management(request):
    """Manage system alerts"""
    return render(request, 'admin_dashboard/alerts.html')
