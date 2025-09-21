from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import DashboardMetricsViewSet, WellnessDashboardView, ChartDataView

# API Router
router = DefaultRouter()
router.register(r'metrics', DashboardMetricsViewSet, basename='metrics')

app_name = 'wellness_dashboard'

urlpatterns = [
    # Web views
    path('', views.dashboard_home, name='home'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('reports/', views.reports_view, name='reports'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/dashboard/', views.dashboard_api, name='dashboard_api'),
    path('api/charts/severity_pie/', views.severity_pie_chart_api, name='severity_pie_chart_api'),
    path('api/charts/assessments_bar/', views.assessments_bar_chart_api, name='assessments_bar_chart_api'),
    path('api/charts/trends_line/', views.trends_line_chart_api, name='trends_line_chart_api'),
    # Keep the old API endpoints for compatibility
    path('api/dashboard-old/', WellnessDashboardView.as_view(), name='api-dashboard'),
    path('api/charts/<str:chart_type>/', ChartDataView.as_view(), name='api-chart-data'),
]
