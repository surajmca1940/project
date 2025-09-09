from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('users/', views.user_analytics, name='users'),
    path('metrics/', views.mental_health_metrics, name='metrics'),
    path('alerts/', views.alert_management, name='alerts'),
]
