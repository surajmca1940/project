from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import RecommendationCategoryViewSet, RecommendationViewSet, UserRecommendationViewSet

# API Router
router = DefaultRouter()
router.register(r'categories', RecommendationCategoryViewSet, basename='category')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')
router.register(r'user-recommendations', UserRecommendationViewSet, basename='userrecommendation')

app_name = 'recommendations'

urlpatterns = [
    # Web views
    path('', views.recommendations_list, name='list'),
    path('my-recommendations/', views.my_recommendations, name='my'),
    path('recommendation/<int:recommendation_id>/', views.recommendation_detail, name='detail'),
    path('for-assessment/<int:assessment_id>/', views.recommendations_for_assessment, name='for_assessment'),
    
    # API endpoints
    path('api/', include(router.urls)),
]