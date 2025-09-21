from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Q, Max
from django.contrib.auth.models import User
from .models import DashboardMetrics, DashboardAlert
from assessments.models import UserAssessment, Questionnaire
from recommendations.models import Recommendation


def dashboard_home(request):
    """Main wellness dashboard home"""
    # Get recent metrics for quick overview
    recent_metrics = DashboardMetrics.objects.all()[:10]
    recent_alerts = DashboardAlert.objects.filter(is_resolved=False)[:5]
    
    context = {
        'recent_metrics': recent_metrics,
        'recent_alerts': recent_alerts
    }
    return render(request, 'wellness_dashboard/dashboard_home.html', context)


def analytics_view(request):
    """Detailed analytics view"""
    context = {}
    return render(request, 'wellness_dashboard/analytics.html', context)


def alerts_view(request):
    """Alerts management view"""
    alerts = DashboardAlert.objects.all().order_by('-triggered_at')
    
    context = {
        'alerts': alerts
    }
    return render(request, 'wellness_dashboard/alerts.html', context)


def reports_view(request):
    """Reports and export view"""
    context = {}
    return render(request, 'wellness_dashboard/reports.html', context)


def dashboard_api(request):
    """API endpoint for dashboard data"""
    try:
        # Get date range from parameters
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            # Default to last 30 days
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
        
        # Basic statistics
        total_users = User.objects.count()
        active_users = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Assessment statistics
        assessments_in_period = UserAssessment.objects.filter(
            completed_at__date__range=[start_date, end_date],
            completed_at__isnull=False
        )
        
        completed_assessments = assessments_in_period.count()
        total_started = UserAssessment.objects.filter(
            created_at__date__range=[start_date, end_date]
        ).count()
        
        completion_rate = round(
            (completed_assessments / total_started * 100) if total_started > 0 else 0, 1
        )
        
        # Severity analysis
        severity_counts = assessments_in_period.values('severity_level').annotate(
            count=Count('id')
        )
        
        # Risk analysis
        high_risk_users = assessments_in_period.filter(
            severity_level__in=['severe', 'moderately_severe']
        ).values('user').distinct().count()
        
        severe_cases = assessments_in_period.filter(
            severity_level='severe'
        ).values('user').distinct().count()
        
        users_needing_counselling = assessments_in_period.filter(
            severity_level__in=['moderate', 'moderately_severe', 'severe']
        ).values('user').distinct().count()
        
        # Assessment types breakdown
        assessments_by_type = {}
        for questionnaire in Questionnaire.objects.all():
            count = assessments_in_period.filter(
                questionnaire__questionnaire_type=questionnaire.questionnaire_type
            ).count()
            assessments_by_type[questionnaire.questionnaire_type] = count
        
        # Recent alerts
        recent_alerts = []
        alerts = DashboardAlert.objects.filter(
            triggered_at__date__range=[start_date, end_date],
            is_resolved=False
        ).order_by('-triggered_at')[:10]
        
        for alert in alerts:
            recent_alerts.append({
                'threshold': {
                    'name': alert.threshold_name or 'System Alert'
                },
                'message': alert.message,
                'severity': alert.severity,
                'triggered_at': alert.triggered_at.isoformat()
            })
        
        summary_data = {
            'total_users': total_users,
            'active_users': active_users,
            'completed_assessments': completed_assessments,
            'completion_rate': completion_rate,
            'high_risk_users': high_risk_users,
            'severe_cases': severe_cases,
            'users_needing_counselling': users_needing_counselling,
            'assessments_by_type': assessments_by_type
        }
        
        return JsonResponse({
            'summary': summary_data,
            'recent_alerts': recent_alerts,
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'summary': {
                'total_users': 0,
                'active_users': 0,
                'completed_assessments': 0,
                'completion_rate': 0,
                'high_risk_users': 0,
                'severe_cases': 0,
                'users_needing_counselling': 0,
                'assessments_by_type': {}
            },
            'recent_alerts': []
        }, status=500)


def severity_pie_chart_api(request):
    """API for severity distribution pie chart"""
    try:
        # Get completed assessments from last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        assessments = UserAssessment.objects.filter(
            completed_at__gte=thirty_days_ago,
            completed_at__isnull=False,
            severity_level__isnull=False
        )
        
        # Count by severity
        severity_counts = assessments.values('severity_level').annotate(
            count=Count('id')
        ).order_by('severity_level')
        
        # Prepare chart data
        labels = []
        data = []
        colors = {
            'minimal': '#10b981',  # green
            'mild': '#f59e0b',     # yellow
            'moderate': '#f97316', # orange
            'moderately_severe': '#ef4444',  # red
            'severe': '#dc2626'    # dark red
        }
        
        background_colors = []
        
        for item in severity_counts:
            severity = item['severity_level']
            count = item['count']
            
            labels.append(severity.replace('_', ' ').title())
            data.append(count)
            background_colors.append(colors.get(severity, '#6b7280'))
        
        return JsonResponse({
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': background_colors,
                'borderWidth': 2,
                'borderColor': '#ffffff'
            }]
        })
    
    except Exception as e:
        return JsonResponse({
            'labels': [],
            'datasets': [{'data': [], 'backgroundColor': []}]
        }, status=500)


def assessments_bar_chart_api(request):
    """API for assessments by type bar chart"""
    try:
        # Get assessments from last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        assessments = UserAssessment.objects.filter(
            completed_at__gte=thirty_days_ago,
            completed_at__isnull=False
        )
        
        # Count by assessment type
        type_counts = {}
        for questionnaire in Questionnaire.objects.all():
            count = assessments.filter(
                questionnaire__questionnaire_type=questionnaire.questionnaire_type
            ).count()
            type_counts[questionnaire.title] = count
        
        # Prepare chart data
        labels = list(type_counts.keys())
        data = list(type_counts.values())
        
        return JsonResponse({
            'labels': labels,
            'datasets': [{
                'label': 'Completed Assessments',
                'data': data,
                'backgroundColor': '#6366f1',
                'borderColor': '#4f46e5',
                'borderWidth': 1
            }]
        })
    
    except Exception as e:
        return JsonResponse({
            'labels': [],
            'datasets': [{'data': [], 'backgroundColor': '#6366f1'}]
        }, status=500)


def trends_line_chart_api(request):
    """API for daily trends line chart"""
    try:
        # Get last 30 days of data
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=29)  # 30 days total
        
        # Generate date range
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Get daily assessment counts
        daily_counts = []
        daily_labels = []
        
        for date in dates:
            count = UserAssessment.objects.filter(
                completed_at__date=date,
                completed_at__isnull=False
            ).count()
            daily_counts.append(count)
            daily_labels.append(date.strftime('%m/%d'))
        
        return JsonResponse({
            'labels': daily_labels,
            'datasets': [{
                'label': 'Daily Assessments',
                'data': daily_counts,
                'borderColor': '#6366f1',
                'backgroundColor': 'rgba(99, 102, 241, 0.1)',
                'tension': 0.4,
                'fill': True
            }]
        })
    
    except Exception as e:
        return JsonResponse({
            'labels': [],
            'datasets': [{'data': [], 'borderColor': '#6366f1'}]
        }, status=500)
