from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
from assessments.models import UserAssessment
from .models import (
    RecommendationCategory, Recommendation, 
    UserRecommendation, RecommendationTemplate
)
from .serializers import (
    RecommendationCategorySerializer, RecommendationSerializer,
    UserRecommendationSerializer, UserRecommendationUpdateSerializer,
    RecommendationStatsSerializer
)


class RecommendationCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for browsing recommendation categories
    """
    queryset = RecommendationCategory.objects.filter(is_active=True)
    serializer_class = RecommendationCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for browsing recommendations
    """
    queryset = Recommendation.objects.filter(is_active=True).prefetch_related(
        'category', 'applicable_questionnaires'
    )
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category if provided
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by recommendation type if provided
        rec_type = self.request.query_params.get('type', None)
        if rec_type:
            queryset = queryset.filter(recommendation_type=rec_type)
        
        # Filter by urgency if provided
        urgency = self.request.query_params.get('urgency', None)
        if urgency:
            queryset = queryset.filter(urgency=urgency)
            
        return queryset.order_by('urgency', 'category__order', 'title')


class UserRecommendationViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing user recommendations
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserRecommendation.objects.filter(
            user=self.request.user
        ).select_related(
            'recommendation', 'recommendation__category', 'assessment'
        ).order_by('recommendation__urgency', '-suggested_at')
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserRecommendationUpdateSerializer
        return UserRecommendationSerializer
    
    @action(detail=False, methods=['get'])
    def for_assessment(self, request):
        """Get recommendations for a specific assessment"""
        assessment_id = request.query_params.get('assessment_id')
        
        if not assessment_id:
            return Response(
                {'error': 'assessment_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            assessment = UserAssessment.objects.get(
                id=assessment_id,
                user=request.user,
                status='completed'
            )
        except UserAssessment.DoesNotExist:
            return Response(
                {'error': 'Assessment not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get or create recommendations for this assessment
        self._generate_recommendations_for_assessment(assessment)
        
        # Return recommendations for this assessment
        recommendations = UserRecommendation.objects.filter(
            user=request.user,
            assessment=assessment
        ).select_related(
            'recommendation', 'recommendation__category'
        ).order_by('recommendation__urgency', '-suggested_at')
        
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def urgent(self, request):
        """Get urgent recommendations for the user"""
        urgent_recommendations = self.get_queryset().filter(
            recommendation__urgency='urgent',
            status__in=['suggested', 'viewed']
        )
        
        serializer = self.get_serializer(urgent_recommendations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get recommendation statistics for the user"""
        user = request.user
        
        # Basic counts
        total = UserRecommendation.objects.filter(user=user).count()
        viewed = UserRecommendation.objects.filter(user=user, status='viewed').count()
        started = UserRecommendation.objects.filter(user=user, status='started').count()
        completed = UserRecommendation.objects.filter(user=user, status='completed').count()
        
        # Average rating
        avg_rating_result = UserRecommendation.objects.filter(
            user=user,
            rating__isnull=False
        ).aggregate(avg_rating=Avg('rating'))
        avg_rating = avg_rating_result['avg_rating'] or 0.0
        
        # Recommendations by category
        categories = UserRecommendation.objects.filter(
            user=user
        ).values(
            'recommendation__category__name'
        ).annotate(
            count=Count('id')
        )
        
        recommendations_by_category = {
            item['recommendation__category__name']: item['count'] 
            for item in categories
        }
        
        # Urgent recommendations count
        urgent_count = UserRecommendation.objects.filter(
            user=user,
            recommendation__urgency='urgent',
            status__in=['suggested', 'viewed']
        ).count()
        
        data = {
            'total_recommendations': total,
            'viewed_count': viewed,
            'started_count': started,
            'completed_count': completed,
            'average_rating': round(avg_rating, 2),
            'recommendations_by_category': recommendations_by_category,
            'urgent_recommendations': urgent_count
        }
        
        serializer = RecommendationStatsSerializer(data)
        return Response(serializer.data)
    
    def _generate_recommendations_for_assessment(self, assessment):
        """Generate appropriate recommendations based on assessment results"""
        
        # Check if recommendations already exist for this assessment
        if UserRecommendation.objects.filter(
            user=assessment.user,
            assessment=assessment
        ).exists():
            return
        
        # Find applicable recommendations
        applicable_recommendations = Recommendation.objects.filter(
            is_active=True
        ).filter(
            Q(applicable_questionnaires__isnull=True) |
            Q(applicable_questionnaires=assessment.questionnaire)
        )
        
        # Filter by score range and severity level
        for recommendation in applicable_recommendations:
            if recommendation.is_applicable_for_assessment(assessment):
                UserRecommendation.objects.get_or_create(
                    user=assessment.user,
                    recommendation=recommendation,
                    assessment=assessment,
                    defaults={
                        'status': 'suggested',
                    }
                )