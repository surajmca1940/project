from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action, permission_classes as perm_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Sum, Q, Max
from django.utils import timezone
from datetime import datetime, timedelta
from assessments.models import UserAssessment, Questionnaire
from .models import DashboardMetrics, InstitutionMetrics, AlertThreshold, DashboardAlert
from .serializers import (
    DashboardMetricsSerializer, InstitutionMetricsSerializer,
    DashboardSummarySerializer, SeverityDistributionSerializer,
    TrendDataSerializer, AlertThresholdSerializer,
    DashboardAlertSerializer, ChartDataSerializer
)


class DashboardMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for dashboard metrics (admin only)
    """
    queryset = DashboardMetrics.objects.all().select_related('questionnaire')
    serializer_class = DashboardMetricsSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Filter by questionnaire
        questionnaire_id = self.request.query_params.get('questionnaire')
        if questionnaire_id:
            queryset = queryset.filter(questionnaire_id=questionnaire_id)
        
        return queryset.order_by('-date', 'questionnaire__title')


class WellnessDashboardView(generics.GenericAPIView):
    """
    Main wellness dashboard API endpoint
    """
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        """Get comprehensive dashboard data"""
        
        # Date range for analysis (default to last 30 days)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Override with query params if provided
        if request.query_params.get('start_date'):
            start_date = datetime.strptime(request.query_params['start_date'], '%Y-%m-%d').date()
        if request.query_params.get('end_date'):
            end_date = datetime.strptime(request.query_params['end_date'], '%Y-%m-%d').date()
        
        # Calculate summary statistics
        summary_data = self._get_summary_statistics(start_date, end_date)
        
        # Get severity distribution by questionnaire type
        severity_distribution = self._get_severity_distribution(start_date, end_date)
        
        # Get trend data
        trend_data = self._get_trend_data(start_date, end_date)
        
        # Get recent alerts
        recent_alerts = DashboardAlert.objects.filter(
            triggered_at__gte=start_date,
            is_resolved=False
        ).select_related('threshold', 'questionnaire')[:10]
        
        response_data = {
            'summary': DashboardSummarySerializer(summary_data).data,
            'severity_distribution': SeverityDistributionSerializer(severity_distribution, many=True).data,
            'trends': TrendDataSerializer(trend_data, many=True).data,
            'recent_alerts': DashboardAlertSerializer(recent_alerts, many=True).data,
            'date_range': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
        
        return Response(response_data)
    
    def _get_summary_statistics(self, start_date, end_date):
        """Calculate summary statistics for the dashboard"""
        
        # Total and active users
        total_users = User.objects.filter(is_active=True).count()
        active_users = User.objects.filter(
            assessments__started_at__date__gte=start_date,
            assessments__started_at__date__lte=end_date
        ).distinct().count()
        
        # Assessment statistics
        total_assessments = UserAssessment.objects.filter(
            started_at__date__gte=start_date,
            started_at__date__lte=end_date
        ).count()
        
        completed_assessments = UserAssessment.objects.filter(
            started_at__date__gte=start_date,
            started_at__date__lte=end_date,
            status='completed'
        ).count()
        
        completion_rate = (completed_assessments / total_assessments * 100) if total_assessments > 0 else 0
        
        # Risk indicators
        high_risk_users = UserAssessment.objects.filter(
            completed_at__date__gte=start_date,
            completed_at__date__lte=end_date,
            status='completed',
            severity_level__in=['moderate', 'moderately_severe', 'severe']
        ).values('user').distinct().count()
        
        users_needing_counselling = UserAssessment.objects.filter(
            completed_at__date__gte=start_date,
            completed_at__date__lte=end_date,
            status='completed',
            severity_level__in=['moderately_severe', 'severe']
        ).values('user').distinct().count()
        
        severe_cases = UserAssessment.objects.filter(
            completed_at__date__gte=start_date,
            completed_at__date__lte=end_date,
            status='completed',
            severity_level='severe'
        ).count()
        
        # Assessments by type
        assessments_by_type = UserAssessment.objects.filter(
            completed_at__date__gte=start_date,
            completed_at__date__lte=end_date,
            status='completed'
        ).values(
            'questionnaire__questionnaire_type'
        ).annotate(
            count=Count('id')
        )
        
        assessments_by_type_dict = {
            item['questionnaire__questionnaire_type']: item['count']
            for item in assessments_by_type
        }
        
        # Risk distribution by severity
        risk_distribution = UserAssessment.objects.filter(
            completed_at__date__gte=start_date,
            completed_at__date__lte=end_date,
            status='completed'
        ).values(
            'severity_level'
        ).annotate(
            count=Count('id')
        )
        
        risk_distribution_dict = {
            item['severity_level']: item['count']
            for item in risk_distribution
        }
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_assessments': total_assessments,
            'completed_assessments': completed_assessments,
            'completion_rate': round(completion_rate, 2),
            'high_risk_users': high_risk_users,
            'users_needing_counselling': users_needing_counselling,
            'severe_cases': severe_cases,
            'assessments_by_type': assessments_by_type_dict,
            'risk_distribution': risk_distribution_dict
        }
    
    def _get_severity_distribution(self, start_date, end_date):
        """Get severity level distribution by questionnaire type"""
        
        questionnaire_types = Questionnaire.objects.values_list(
            'questionnaire_type', flat=True
        ).distinct()
        
        distribution_data = []
        
        for q_type in questionnaire_types:
            assessments = UserAssessment.objects.filter(
                questionnaire__questionnaire_type=q_type,
                completed_at__date__gte=start_date,
                completed_at__date__lte=end_date,
                status='completed'
            )
            
            severity_counts = assessments.values('severity_level').annotate(
                count=Count('id')
            )
            
            # Initialize counts
            counts = {
                'minimal': 0,
                'mild': 0,
                'moderate': 0,
                'moderately_severe': 0,
                'severe': 0
            }
            
            # Update with actual counts
            for item in severity_counts:
                if item['severity_level'] in counts:
                    counts[item['severity_level']] = item['count']
            
            total = sum(counts.values())
            
            if total > 0:  # Only include if there are assessments
                distribution_data.append({
                    'questionnaire_type': q_type,
                    'minimal': counts['minimal'],
                    'mild': counts['mild'],
                    'moderate': counts['moderate'],
                    'moderately_severe': counts['moderately_severe'],
                    'severe': counts['severe'],
                    'total': total
                })
        
        return distribution_data
    
    def _get_trend_data(self, start_date, end_date):
        """Get trend data for charts"""
        
        # Generate date range
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        
        trend_data = []
        
        # Get daily completion rates
        for date in date_range:
            total_day = UserAssessment.objects.filter(
                started_at__date=date
            ).count()
            
            completed_day = UserAssessment.objects.filter(
                started_at__date=date,
                status='completed'
            ).count()
            
            completion_rate = (completed_day / total_day * 100) if total_day > 0 else 0
            
            if total_day > 0:  # Only include days with assessments
                trend_data.append({
                    'date': date,
                    'value': completion_rate,
                    'questionnaire_type': 'completion_rate'
                })
        
        return trend_data


@perm_classes([permissions.IsAdminUser])
class ChartDataView(generics.GenericAPIView):
    """Generate chart data for various dashboard visualizations"""
    
    def get(self, request, chart_type, *args, **kwargs):
        """Get chart data based on chart type"""
        
        if chart_type == 'severity_pie':
            return self._get_severity_pie_chart()
        elif chart_type == 'assessments_bar':
            return self._get_assessments_bar_chart()
        elif chart_type == 'trends_line':
            return self._get_trends_line_chart()
        else:
            return Response(
                {'error': 'Invalid chart type'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _get_severity_pie_chart(self):
        """Generate pie chart data for severity distribution"""
        
        # Get severity counts for last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        severity_counts = UserAssessment.objects.filter(
            completed_at__date__gte=start_date,
            completed_at__date__lte=end_date,
            status='completed'
        ).values('severity_level').annotate(
            count=Count('id')
        )
        
        labels = []
        data = []
        colors = {
            'minimal': '#10b981',
            'mild': '#f59e0b',
            'moderate': '#f97316',
            'moderately_severe': '#ef4444',
            'severe': '#dc2626'
        }
        
        background_colors = []
        
        for item in severity_counts:
            severity = item['severity_level']
            labels.append(severity.replace('_', ' ').title())
            data.append(item['count'])
            background_colors.append(colors.get(severity, '#6b7280'))
        
        chart_data = {
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': background_colors,
                'borderWidth': 1
            }],
            'title': 'Mental Health Severity Distribution (Last 30 Days)',
            'type': 'pie'
        }
        
        serializer = ChartDataSerializer(chart_data)
        return Response(serializer.data)
    
    def _get_assessments_bar_chart(self):
        """Generate bar chart data for assessments by type"""
        
        # Get assessment counts by questionnaire type for last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        assessment_counts = UserAssessment.objects.filter(
            completed_at__date__gte=start_date,
            completed_at__date__lte=end_date,
            status='completed'
        ).values(
            'questionnaire__questionnaire_type',
            'questionnaire__title'
        ).annotate(
            count=Count('id')
        )
        
        labels = []
        data = []
        
        for item in assessment_counts:
            labels.append(item['questionnaire__title'])
            data.append(item['count'])
        
        chart_data = {
            'labels': labels,
            'datasets': [{
                'label': 'Completed Assessments',
                'data': data,
                'backgroundColor': '#6366f1',
                'borderColor': '#4f46e5',
                'borderWidth': 1
            }],
            'title': 'Assessments by Type (Last 30 Days)',
            'type': 'bar'
        }
        
        serializer = ChartDataSerializer(chart_data)
        return Response(serializer.data)
    
    def _get_trends_line_chart(self):
        """Generate line chart data for daily assessment trends"""
        
        # Get daily assessment counts for last 14 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=14)
        
        daily_counts = []
        labels = []
        
        current_date = start_date
        while current_date <= end_date:
            count = UserAssessment.objects.filter(
                started_at__date=current_date,
                status='completed'
            ).count()
            
            daily_counts.append(count)
            labels.append(current_date.strftime('%m/%d'))
            current_date += timedelta(days=1)
        
        chart_data = {
            'labels': labels,
            'datasets': [{
                'label': 'Daily Completed Assessments',
                'data': daily_counts,
                'borderColor': '#06b6d4',
                'backgroundColor': 'rgba(6, 182, 212, 0.1)',
                'fill': True,
                'tension': 0.4
            }],
            'title': 'Daily Assessment Trends (Last 14 Days)',
            'type': 'line'
        }
        
        serializer = ChartDataSerializer(chart_data)
        return Response(serializer.data)