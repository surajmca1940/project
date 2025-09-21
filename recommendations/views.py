from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recommendation, UserRecommendation
from assessments.models import UserAssessment


def recommendations_list(request):
    """List all available recommendations"""
    recommendations = Recommendation.objects.filter(is_active=True)
    context = {
        'recommendations': recommendations
    }
    return render(request, 'recommendations/recommendations_list.html', context)


def my_recommendations(request):
    """Show user's personalized recommendations"""
    if request.user.is_authenticated:
        user_recommendations = UserRecommendation.objects.filter(
            user=request.user
        ).select_related('recommendation', 'recommendation__category')
    else:
        # For demo purposes, show all user recommendations
        user_recommendations = UserRecommendation.objects.select_related('recommendation', 'recommendation__category')
    
    # Apply filters
    status_filter = request.GET.get('status')
    urgency_filter = request.GET.get('urgency')
    
    if status_filter and status_filter != 'all':
        user_recommendations = user_recommendations.filter(status=status_filter)
    
    if urgency_filter:
        user_recommendations = user_recommendations.filter(recommendation__urgency=urgency_filter)
    
    user_recommendations = user_recommendations.order_by('recommendation__urgency', '-suggested_at')
    
    # Calculate statistics
    completed_count = user_recommendations.filter(status='completed').count()
    
    context = {
        'user_recommendations': user_recommendations,
        'completed_count': completed_count,
    }
    return render(request, 'recommendations/my_recommendations.html', context)


def recommendation_detail(request, recommendation_id):
    """Show detailed view of a recommendation"""
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    
    context = {
        'recommendation': recommendation
    }
    return render(request, 'recommendations/recommendation_detail.html', context)


def recommendations_for_assessment(request, assessment_id):
    """Show recommendations for a specific assessment"""
    if request.user.is_authenticated:
        assessment = get_object_or_404(UserAssessment, id=assessment_id, user=request.user)
        user_recommendations = UserRecommendation.objects.filter(
            user=request.user,
            assessment=assessment
        ).select_related('recommendation', 'recommendation__category').order_by('recommendation__urgency', 'recommendation__category')
    else:
        # For demo purposes
        assessment = get_object_or_404(UserAssessment, id=assessment_id)
        user_recommendations = UserRecommendation.objects.filter(
            assessment=assessment
        ).select_related('recommendation', 'recommendation__category').order_by('recommendation__urgency', 'recommendation__category')
    
    # If no recommendations exist, generate them
    if not user_recommendations.exists():
        from recommendations.api import UserRecommendationViewSet
        viewset = UserRecommendationViewSet()
        viewset._generate_recommendations_for_assessment(assessment)
        # Refresh queryset
        if request.user.is_authenticated:
            user_recommendations = UserRecommendation.objects.filter(
                user=request.user,
                assessment=assessment
            ).select_related('recommendation', 'recommendation__category').order_by('recommendation__urgency', 'recommendation__category')
        else:
            user_recommendations = UserRecommendation.objects.filter(
                assessment=assessment
            ).select_related('recommendation', 'recommendation__category').order_by('recommendation__urgency', 'recommendation__category')
    
    # Calculate statistics
    urgent_count = user_recommendations.filter(recommendation__urgency='urgent').count()
    categories_count = user_recommendations.values('recommendation__category').distinct().count()
    total_duration = sum([rec.recommendation.duration_minutes for rec in user_recommendations if rec.recommendation.duration_minutes]) or 0
    
    context = {
        'assessment': assessment,
        'user_recommendations': user_recommendations,
        'urgent_count': urgent_count,
        'categories_count': categories_count,
        'total_duration': total_duration,
    }
    return render(request, 'recommendations/recommendations_for_assessment.html', context)
