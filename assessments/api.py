from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Max
from .models import (
    Questionnaire, Question, Choice, 
    UserAssessment, AssessmentResponse
)
from .serializers import (
    QuestionnaireListSerializer, QuestionnaireDetailSerializer,
    UserAssessmentSerializer, UserAssessmentCreateSerializer,
    SubmitAssessmentSerializer, AssessmentStatsSerializer
)


class QuestionnaireViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for browsing questionnaires
    """
    queryset = Questionnaire.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionnaireDetailSerializer
        return QuestionnaireListSerializer
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Get all questions for a questionnaire"""
        questionnaire = self.get_object()
        questions = questionnaire.questions.all().prefetch_related('choices')
        
        data = []
        for question in questions:
            question_data = {
                'id': question.id,
                'text': question.text,
                'type': question.question_type,
                'order': question.order,
                'required': question.is_required,
                'choices': [
                    {
                        'id': choice.id,
                        'text': choice.text,
                        'order': choice.order
                    }
                    for choice in question.choices.all()
                ]
            }
            data.append(question_data)
        
        return Response(data)


class UserAssessmentViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing user assessments
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAssessment.objects.filter(user=self.request.user).prefetch_related(
            'questionnaire', 'responses', 'responses__question', 'responses__choice'
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserAssessmentCreateSerializer
        return UserAssessmentSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            status='started',
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get assessment statistics for the user"""
        user = request.user
        
        # Get basic counts
        total = UserAssessment.objects.filter(user=user).count()
        completed = UserAssessment.objects.filter(user=user, status='completed').count()
        
        # Get latest scores by questionnaire type
        latest_scores = {}
        latest_assessments = UserAssessment.objects.filter(
            user=user, 
            status='completed'
        ).values(
            'questionnaire__questionnaire_type'
        ).annotate(
            latest_date=Max('completed_at')
        )
        
        for item in latest_assessments:
            q_type = item['questionnaire__questionnaire_type']
            latest = UserAssessment.objects.filter(
                user=user,
                questionnaire__questionnaire_type=q_type,
                completed_at=item['latest_date']
            ).first()
            
            if latest:
                latest_scores[q_type] = {
                    'score': latest.total_score,
                    'severity': latest.severity_level,
                    'date': latest.completed_at
                }
        
        # Get score improvement trends
        improvement_trends = {}
        for q_type, latest in latest_scores.items():
            # Get previous assessment to calculate improvement
            previous = UserAssessment.objects.filter(
                user=user,
                questionnaire__questionnaire_type=q_type,
                status='completed',
                completed_at__lt=latest['date']
            ).order_by('-completed_at').first()
            
            if previous:
                score_diff = previous.total_score - latest['score']
                improved = score_diff > 0  # Lower score is better for most assessments
                
                improvement_trends[q_type] = {
                    'previous_score': previous.total_score,
                    'current_score': latest['score'],
                    'difference': score_diff,
                    'improved': improved,
                    'previous_date': previous.completed_at
                }
        
        data = {
            'total_assessments': total,
            'completed_assessments': completed,
            'latest_scores': latest_scores,
            'improvement_trends': improvement_trends
        }
        
        serializer = AssessmentStatsSerializer(data)
        return Response(serializer.data)


class StartAssessmentView(generics.CreateAPIView):
    """Start a new assessment session"""
    serializer_class = UserAssessmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='started')


class SubmitAssessmentView(generics.GenericAPIView):
    """Submit assessment responses and calculate scores"""
    serializer_class = SubmitAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        assessment = serializer.save()
        
        # Return the updated assessment with score
        response_serializer = UserAssessmentSerializer(assessment)
        return Response(response_serializer.data, status=status.HTTP_200_OK)