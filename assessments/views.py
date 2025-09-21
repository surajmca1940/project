from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Questionnaire, UserAssessment


def assessment_list(request):
    """List all available assessments"""
    questionnaires = Questionnaire.objects.filter(is_active=True)
    context = {
        'questionnaires': questionnaires
    }
    return render(request, 'assessments/assessment_list.html', context)


def take_assessment(request, questionnaire_id):
    """Take a specific assessment"""
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, is_active=True)
    questions = questionnaire.questions.all().prefetch_related('choices')
    
    context = {
        'questionnaire': questionnaire,
        'questions': questions
    }
    return render(request, 'assessments/take_assessment.html', context)


def assessment_results(request, assessment_id):
    """Show results of a completed assessment"""
    if request.user.is_authenticated:
        assessment = get_object_or_404(UserAssessment, id=assessment_id, user=request.user)
    else:
        # For demo purposes, get any assessment
        assessment = get_object_or_404(UserAssessment, id=assessment_id)
    
    # Calculate additional metrics for the template
    score_percentage = (assessment.total_score / assessment.questionnaire.max_score * 100) if assessment.questionnaire.max_score > 0 else 0
    average_per_question = (assessment.total_score / assessment.responses.count()) if assessment.responses.count() > 0 else 0
    
    context = {
        'assessment': assessment,
        'score_percentage': score_percentage,
        'average_per_question': average_per_question,
    }
    return render(request, 'assessments/assessment_results.html', context)


def assessment_history(request):
    """Show user's assessment history"""
    from django.utils import timezone
    from datetime import timedelta
    
    if request.user.is_authenticated:
        assessments = UserAssessment.objects.filter(
            user=request.user
        ).select_related('questionnaire').order_by('-started_at')
    else:
        # For demo purposes, show all assessments
        assessments = UserAssessment.objects.select_related('questionnaire').order_by('-started_at')
    
    # Apply filters
    filter_type = request.GET.get('filter', 'all')
    if filter_type and filter_type != 'all':
        if filter_type == 'completed':
            assessments = assessments.filter(status='completed')
        else:
            assessments = assessments.filter(questionnaire__questionnaire_type=filter_type)
    
    # Calculate statistics
    completed_count = assessments.filter(status='completed').count()
    unique_types = assessments.values('questionnaire__questionnaire_type').distinct().count()
    
    # Calculate days since first assessment
    first_assessment = assessments.last()
    days_since_first = 0
    if first_assessment:
        days_since_first = (timezone.now().date() - first_assessment.started_at.date()).days
    
    context = {
        'assessments': assessments,
        'completed_count': completed_count,
        'unique_types': unique_types,
        'days_since_first': days_since_first,
    }
    return render(request, 'assessments/assessment_history.html', context)
