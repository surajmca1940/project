from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import UserActivity, MentalHealthMetric, Alert, RealTimeMetric, SystemHealth
from booking_system.models import Appointment
from ai_support.models import ChatSession
from peer_support.models import ForumPost
from resources.models import Resource
import json

@staff_member_required
def dashboard_home(request):
    """Admin dashboard homepage with real data"""
    # Get current date and month range
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # User statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(last_login__gte=start_of_month).count()
    new_users_today = User.objects.filter(date_joined__date=now.date()).count()
    
    # Activity statistics
    ai_sessions_count = UserActivity.objects.filter(
        activity_type='ai_chat',
        timestamp__gte=start_of_month
    ).count()
    
    appointments_count = Appointment.objects.filter(
        created_at__gte=start_of_month
    ).count()
    
    resource_views = UserActivity.objects.filter(
        activity_type='resource_view',
        timestamp__gte=start_of_month
    ).count()
    
    forum_posts = UserActivity.objects.filter(
        activity_type='forum_post',
        timestamp__gte=start_of_month
    ).count()
    
    # Recent alerts
    recent_alerts = Alert.objects.filter(is_resolved=False)[:5]
    
    # Recent activities
    recent_activities = UserActivity.objects.select_related('user')[:10]
    
    # Feature usage statistics
    feature_usage = {
        'ai_support': ai_sessions_count,
        'appointments': appointments_count,
        'resources': resource_views,
        'forum': forum_posts,
    }
    
    total_activities = sum(feature_usage.values()) or 1  # Avoid division by zero
    feature_percentages = {
        key: (value / total_activities) * 100 for key, value in feature_usage.items()
    }
    
    # Weekly activity trend (last 7 days)
    weekly_data = []
    for i in range(7):
        date = now.date() - timedelta(days=i)
        day_activities = UserActivity.objects.filter(
            timestamp__date=date
        ).count()
        weekly_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'activities': day_activities
        })
    
    weekly_data.reverse()  # Show oldest to newest
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'new_users_today': new_users_today,
        'ai_sessions_count': ai_sessions_count,
        'appointments_count': appointments_count,
        'resource_views': resource_views,
        'forum_posts': forum_posts,
        'recent_alerts': recent_alerts,
        'recent_activities': recent_activities,
        'feature_percentages': feature_percentages,
        'weekly_data': json.dumps(weekly_data),
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)

@staff_member_required
def dashboard_api(request):
    """API endpoint for real-time dashboard data"""
    now = timezone.now()
    
    # Current active sessions (users active in last 10 minutes)
    active_sessions = User.objects.filter(
        last_login__gte=now - timedelta(minutes=10)
    ).count()
    
    # Today's statistics
    today_stats = {
        'active_sessions': active_sessions,
        'appointments_today': Appointment.objects.filter(
            appointment_date=now.date()
        ).count(),
        'ai_sessions_today': UserActivity.objects.filter(
            activity_type='ai_chat',
            timestamp__date=now.date()
        ).count(),
        'crisis_interventions': Alert.objects.filter(
            alert_type='crisis',
            created_at__date=now.date(),
            is_resolved=False
        ).count(),
    }
    
    return JsonResponse(today_stats)

@staff_member_required
def user_analytics(request):
    """User analytics and statistics"""
    # User registration trend (last 30 days)
    registration_data = []
    for i in range(30):
        date = timezone.now().date() - timedelta(days=i)
        registrations = User.objects.filter(date_joined__date=date).count()
        registration_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'registrations': registrations
        })
    
    registration_data.reverse()
    
    # User activity by type
    activity_stats = UserActivity.objects.values('activity_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'registration_data': json.dumps(registration_data),
        'activity_stats': activity_stats,
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=30)
        ).count(),
    }
    
    return render(request, 'admin_dashboard/users.html', context)

@staff_member_required
def mental_health_metrics(request):
    """Mental health metrics and trends"""
    # Get or create today's metrics
    today = timezone.now().date()
    metrics, created = MentalHealthMetric.objects.get_or_create(
        date=today,
        defaults={
            'total_users': User.objects.count(),
            'active_sessions': UserActivity.objects.filter(
                timestamp__date=today
            ).count(),
            'appointments_booked': Appointment.objects.filter(
                created_at__date=today
            ).count(),
            'resources_accessed': UserActivity.objects.filter(
                activity_type='resource_view',
                timestamp__date=today
            ).count(),
            'forum_posts': UserActivity.objects.filter(
                activity_type='forum_post',
                timestamp__date=today
            ).count(),
            'crisis_indicators': Alert.objects.filter(
                alert_type='crisis',
                created_at__date=today
            ).count(),
        }
    )
    
    # Historical metrics (last 30 days)
    historical_metrics = MentalHealthMetric.objects.filter(
        date__gte=today - timedelta(days=30)
    ).order_by('date')
    
    context = {
        'today_metrics': metrics,
        'historical_metrics': historical_metrics,
    }
    
    return render(request, 'admin_dashboard/metrics.html', context)

@staff_member_required
def alert_management(request):
    """Manage system alerts"""
    alerts = Alert.objects.all().order_by('-created_at')
    
    # Alert statistics
    alert_stats = {
        'total': alerts.count(),
        'unresolved': alerts.filter(is_resolved=False).count(),
        'critical': alerts.filter(severity='critical', is_resolved=False).count(),
        'high': alerts.filter(severity='high', is_resolved=False).count(),
    }
    
    context = {
        'alerts': alerts,
        'alert_stats': alert_stats,
    }
    
    return render(request, 'admin_dashboard/alerts.html', context)
