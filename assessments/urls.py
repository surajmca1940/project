from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import QuestionnaireViewSet, UserAssessmentViewSet, StartAssessmentView, SubmitAssessmentView

# API Router
router = DefaultRouter()
router.register(r'questionnaires', QuestionnaireViewSet, basename='questionnaire')
router.register(r'assessments', UserAssessmentViewSet, basename='userassessment')

app_name = 'assessments'

urlpatterns = [
    # Web views
    path('', views.assessment_list, name='list'),
    path('take/<int:questionnaire_id>/', views.take_assessment, name='take'),
    path('results/<int:assessment_id>/', views.assessment_results, name='results'),
    path('history/', views.assessment_history, name='history'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/start-assessment/', StartAssessmentView.as_view(), name='api-start-assessment'),
    path('api/submit-assessment/', SubmitAssessmentView.as_view(), name='api-submit-assessment'),
]