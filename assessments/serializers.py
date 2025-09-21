from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Questionnaire, Question, Choice, UserAssessment, AssessmentResponse


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'score', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'order', 'is_required', 'choices']


class QuestionnaireListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing questionnaires"""
    class Meta:
        model = Questionnaire
        fields = ['id', 'title', 'questionnaire_type', 'description', 'max_score', 'is_active']


class QuestionnaireDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with questions for taking assessments"""
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Questionnaire
        fields = [
            'id', 'title', 'questionnaire_type', 'description', 'instructions', 
            'max_score', 'scoring_ranges', 'questions', 'is_active'
        ]


class AssessmentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResponse
        fields = ['id', 'question', 'choice', 'answered_at']
        read_only_fields = ['answered_at']


class UserAssessmentSerializer(serializers.ModelSerializer):
    responses = AssessmentResponseSerializer(many=True, read_only=True)
    questionnaire = QuestionnaireListSerializer(read_only=True)
    
    class Meta:
        model = UserAssessment
        fields = [
            'id', 'questionnaire', 'status', 'started_at', 'completed_at',
            'total_score', 'severity_level', 'responses'
        ]
        read_only_fields = ['started_at', 'total_score', 'severity_level']


class UserAssessmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new assessment"""
    
    class Meta:
        model = UserAssessment
        fields = ['questionnaire']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SubmitAssessmentSerializer(serializers.Serializer):
    """Serializer for submitting assessment responses"""
    assessment_id = serializers.IntegerField()
    responses = serializers.ListSerializer(
        child=serializers.DictField(child=serializers.IntegerField())
    )
    
    def validate_assessment_id(self, value):
        """Ensure assessment belongs to current user"""
        try:
            assessment = UserAssessment.objects.get(
                id=value,
                user=self.context['request'].user,
                status='started'
            )
        except UserAssessment.DoesNotExist:
            raise serializers.ValidationError("Invalid assessment ID or assessment not found")
        return value
    
    def validate_responses(self, value):
        """Validate response format and choices"""
        for response in value:
            if 'question_id' not in response or 'choice_id' not in response:
                raise serializers.ValidationError("Each response must have question_id and choice_id")
        return value
    
    def save(self):
        """Process and save assessment responses"""
        assessment_id = self.validated_data['assessment_id']
        responses_data = self.validated_data['responses']
        
        assessment = UserAssessment.objects.get(id=assessment_id)
        
        # Clear existing responses
        AssessmentResponse.objects.filter(assessment=assessment).delete()
        
        # Create new responses
        for response_data in responses_data:
            question = Question.objects.get(id=response_data['question_id'])
            choice = Choice.objects.get(id=response_data['choice_id'])
            
            # Validate that choice belongs to question
            if choice.question != question:
                raise serializers.ValidationError(f"Choice {choice.id} does not belong to question {question.id}")
            
            AssessmentResponse.objects.create(
                assessment=assessment,
                question=question,
                choice=choice
            )
        
        # Calculate score and update assessment
        assessment.calculate_score()
        assessment.status = 'completed'
        assessment.completed_at = serializers.DateTimeField().to_representation(assessment.started_at)
        assessment.save()
        
        return assessment


class AssessmentStatsSerializer(serializers.Serializer):
    """Serializer for user's assessment statistics"""
    total_assessments = serializers.IntegerField()
    completed_assessments = serializers.IntegerField()
    latest_scores = serializers.DictField()
    improvement_trends = serializers.DictField()