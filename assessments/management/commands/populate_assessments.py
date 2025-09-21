from django.core.management.base import BaseCommand
from django.db import transaction
from assessments.models import Questionnaire, Question, Choice
from recommendations.models import RecommendationCategory, Recommendation


class Command(BaseCommand):
    help = 'Populate the database with sample questionnaires and recommendations'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample questionnaires and recommendations...')
        
        with transaction.atomic():
            # Create PHQ-9 Depression Assessment
            self.create_phq9()
            
            # Create GAD-7 Anxiety Assessment
            self.create_gad7()
            
            # Create Sleep Quality Index
            self.create_sleep_quality_index()
            
            # Create Recommendation Categories
            self.create_recommendation_categories()
            
            # Create Sample Recommendations
            self.create_sample_recommendations()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated assessment data!')
        )

    def create_phq9(self):
        """Create PHQ-9 Depression Assessment"""
        
        # Define scoring ranges for PHQ-9
        scoring_ranges = {
            'minimal': {'min': 0, 'max': 4},
            'mild': {'min': 5, 'max': 9},
            'moderate': {'min': 10, 'max': 14},
            'moderately_severe': {'min': 15, 'max': 19},
            'severe': {'min': 20, 'max': 27}
        }
        
        phq9, created = Questionnaire.objects.get_or_create(
            questionnaire_type='PHQ9',
            defaults={
                'title': 'PHQ-9 Depression Assessment',
                'description': 'A 9-question instrument used for screening, diagnosing, monitoring and measuring the severity of depression.',
                'instructions': 'Over the last 2 weeks, how often have you been bothered by any of the following problems?',
                'max_score': 27,
                'scoring_ranges': scoring_ranges,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created PHQ-9 questionnaire')
            
            # PHQ-9 Questions
            phq9_questions = [
                "Little interest or pleasure in doing things",
                "Feeling down, depressed, or hopeless",
                "Trouble falling or staying asleep, or sleeping too much",
                "Feeling tired or having little energy",
                "Poor appetite or overeating",
                "Feeling bad about yourself - or that you are a failure or have let yourself or your family down",
                "Trouble concentrating on things, such as reading the newspaper or watching television",
                "Moving or speaking so slowly that other people could have noticed. Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual",
                "Thoughts that you would be better off dead, or of hurting yourself"
            ]
            
            # Standard PHQ-9 response options
            response_options = [
                ("Not at all", 0),
                ("Several days", 1),
                ("More than half the days", 2),
                ("Nearly every day", 3)
            ]
            
            for i, question_text in enumerate(phq9_questions, 1):
                question = Question.objects.create(
                    questionnaire=phq9,
                    text=question_text,
                    question_type='likert',
                    order=i,
                    is_required=True
                )
                
                for j, (choice_text, score) in enumerate(response_options, 1):
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        score=score,
                        order=j
                    )

    def create_gad7(self):
        """Create GAD-7 Anxiety Assessment"""
        
        # Define scoring ranges for GAD-7
        scoring_ranges = {
            'minimal': {'min': 0, 'max': 4},
            'mild': {'min': 5, 'max': 9},
            'moderate': {'min': 10, 'max': 14},
            'severe': {'min': 15, 'max': 21}
        }
        
        gad7, created = Questionnaire.objects.get_or_create(
            questionnaire_type='GAD7',
            defaults={
                'title': 'GAD-7 Anxiety Assessment',
                'description': 'A 7-question screening tool used to assess the severity of generalized anxiety disorder.',
                'instructions': 'Over the last 2 weeks, how often have you been bothered by the following problems?',
                'max_score': 21,
                'scoring_ranges': scoring_ranges,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created GAD-7 questionnaire')
            
            # GAD-7 Questions
            gad7_questions = [
                "Feeling nervous, anxious, or on edge",
                "Not being able to stop or control worrying",
                "Worrying too much about different things",
                "Trouble relaxing",
                "Being so restless that it's hard to sit still",
                "Becoming easily annoyed or irritable",
                "Feeling afraid as if something awful might happen"
            ]
            
            # Standard GAD-7 response options
            response_options = [
                ("Not at all", 0),
                ("Several days", 1),
                ("More than half the days", 2),
                ("Nearly every day", 3)
            ]
            
            for i, question_text in enumerate(gad7_questions, 1):
                question = Question.objects.create(
                    questionnaire=gad7,
                    text=question_text,
                    question_type='likert',
                    order=i,
                    is_required=True
                )
                
                for j, (choice_text, score) in enumerate(response_options, 1):
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        score=score,
                        order=j
                    )

    def create_sleep_quality_index(self):
        """Create Sleep Quality Index Assessment"""
        
        # Define scoring ranges for Sleep Quality
        scoring_ranges = {
            'minimal': {'min': 0, 'max': 5},
            'mild': {'min': 6, 'max': 10},
            'moderate': {'min': 11, 'max': 15},
            'severe': {'min': 16, 'max': 21}
        }
        
        sqi, created = Questionnaire.objects.get_or_create(
            questionnaire_type='SQI',
            defaults={
                'title': 'Sleep Quality Index',
                'description': 'A brief assessment to evaluate sleep quality and disturbances.',
                'instructions': 'Over the past month, how would you rate the following aspects of your sleep?',
                'max_score': 21,
                'scoring_ranges': scoring_ranges,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f'Created Sleep Quality Index questionnaire')
            
            # Sleep Quality Questions
            sleep_questions = [
                "How would you rate your sleep quality overall?",
                "How long does it usually take you to fall asleep each night?",
                "How often do you wake up during the night?",
                "How rested do you feel when you wake up in the morning?",
                "How often does poor sleep affect your daily activities?",
                "How worried or distressed are you about your current sleep problems?",
                "How satisfied are you with your current sleep pattern?"
            ]
            
            # Custom response options for each sleep question
            sleep_responses = [
                [("Very good", 0), ("Fairly good", 1), ("Fairly bad", 2), ("Very bad", 3)],
                [("≤15 min", 0), ("16-30 min", 1), ("31-60 min", 2), (">60 min", 3)],
                [("Not during the past month", 0), ("Less than once a week", 1), ("Once or twice a week", 2), ("Three or more times a week", 3)],
                [("Very rested", 0), ("Fairly rested", 1), ("Fairly tired", 2), ("Very tired", 3)],
                [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3)],
                [("Not at all", 0), ("A little", 1), ("Somewhat", 2), ("Very much", 3)],
                [("Very satisfied", 0), ("Satisfied", 1), ("Dissatisfied", 2), ("Very dissatisfied", 3)]
            ]
            
            for i, (question_text, responses) in enumerate(zip(sleep_questions, sleep_responses), 1):
                question = Question.objects.create(
                    questionnaire=sqi,
                    text=question_text,
                    question_type='multiple_choice',
                    order=i,
                    is_required=True
                )
                
                for j, (choice_text, score) in enumerate(responses, 1):
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        score=score,
                        order=j
                    )

    def create_recommendation_categories(self):
        """Create recommendation categories"""
        categories_data = [
            ("Breathing & Relaxation", "🫁", "#10b981", 1),
            ("Physical Exercise", "🏃‍♀️", "#f59e0b", 2),
            ("Mindfulness & Meditation", "🧘‍♂️", "#8b5cf6", 3),
            ("Sleep Hygiene", "😴", "#06b6d4", 4),
            ("Social Support", "👥", "#ef4444", 5),
            ("Professional Help", "👨‍⚕️", "#dc2626", 6),
            ("Lifestyle Changes", "🌱", "#65a30d", 7),
            ("Educational Resources", "📚", "#3b82f6", 8)
        ]
        
        for name, icon, color, order in categories_data:
            category, created = RecommendationCategory.objects.get_or_create(
                name=name,
                defaults={
                    'description': f'Recommendations related to {name.lower()}',
                    'icon': icon,
                    'color': color,
                    'order': order,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created category: {name}')

    def create_sample_recommendations(self):
        """Create sample recommendations"""
        
        # Get categories
        breathing_cat = RecommendationCategory.objects.get(name="Breathing & Relaxation")
        exercise_cat = RecommendationCategory.objects.get(name="Physical Exercise")
        mindfulness_cat = RecommendationCategory.objects.get(name="Mindfulness & Meditation")
        sleep_cat = RecommendationCategory.objects.get(name="Sleep Hygiene")
        social_cat = RecommendationCategory.objects.get(name="Social Support")
        professional_cat = RecommendationCategory.objects.get(name="Professional Help")
        
        # Get questionnaires for targeting
        phq9 = Questionnaire.objects.get(questionnaire_type='PHQ9')
        gad7 = Questionnaire.objects.get(questionnaire_type='GAD7')
        sqi = Questionnaire.objects.get(questionnaire_type='SQI')
        
        recommendations_data = [
            {
                'title': '4-7-8 Breathing Exercise',
                'description': 'A simple breathing technique to reduce anxiety and promote relaxation.',
                'category': breathing_cat,
                'recommendation_type': 'breathing',
                'urgency': 'medium',
                'instructions': """1. Exhale completely through your mouth
2. Close your mouth and inhale through your nose for 4 counts
3. Hold your breath for 7 counts
4. Exhale completely through your mouth for 8 counts
5. Repeat 3-4 times""",
                'duration_minutes': 5,
                'severity_levels': ['mild', 'moderate'],
                'questionnaires': [phq9, gad7]
            },
            {
                'title': 'Daily 20-Minute Walk',
                'description': 'Regular walking can significantly improve mood and reduce symptoms of depression.',
                'category': exercise_cat,
                'recommendation_type': 'exercise',
                'urgency': 'medium',
                'instructions': """1. Choose a pleasant route in your neighborhood or local park
2. Start with 10 minutes if 20 feels too long
3. Walk at a comfortable pace
4. Focus on your surroundings and breathing
5. Try to walk at the same time each day to build a routine""",
                'duration_minutes': 20,
                'severity_levels': ['minimal', 'mild', 'moderate'],
                'questionnaires': [phq9]
            },
            {
                'title': 'Mindfulness Meditation',
                'description': 'Practice mindfulness to reduce anxiety and improve emotional regulation.',
                'category': mindfulness_cat,
                'recommendation_type': 'meditation',
                'urgency': 'medium',
                'instructions': """1. Find a quiet, comfortable place to sit
2. Close your eyes or soften your gaze
3. Focus on your breath, feeling each inhale and exhale
4. When your mind wanders, gently return attention to your breath
5. Start with 5-10 minutes and gradually increase""",
                'duration_minutes': 10,
                'severity_levels': ['mild', 'moderate'],
                'questionnaires': [phq9, gad7]
            },
            {
                'title': 'Sleep Hygiene Routine',
                'description': 'Establish healthy sleep habits to improve sleep quality and mental health.',
                'category': sleep_cat,
                'recommendation_type': 'sleep',
                'urgency': 'high',
                'instructions': """1. Go to bed and wake up at the same time every day
2. Create a relaxing bedtime routine (1 hour before sleep)
3. Avoid screens 1 hour before bedtime
4. Keep bedroom cool, dark, and quiet
5. Avoid caffeine 6 hours before bedtime
6. No large meals 2 hours before bed""",
                'duration_minutes': 60,
                'severity_levels': ['mild', 'moderate', 'severe'],
                'questionnaires': [sqi, phq9]
            },
            {
                'title': 'Connect with Support Network',
                'description': 'Reach out to friends, family, or support groups for emotional support.',
                'category': social_cat,
                'recommendation_type': 'social',
                'urgency': 'high',
                'instructions': """1. Make a list of people you trust and feel comfortable talking to
2. Choose someone who is a good listener
3. Share your feelings honestly
4. Ask for specific help if needed
5. Consider joining a support group
6. Schedule regular check-ins with supportive friends/family""",
                'duration_minutes': 30,
                'severity_levels': ['moderate', 'moderately_severe'],
                'questionnaires': [phq9, gad7]
            },
            {
                'title': 'Seek Professional Counseling',
                'description': 'Professional therapy can provide specialized help for managing mental health challenges.',
                'category': professional_cat,
                'recommendation_type': 'professional',
                'urgency': 'urgent',
                'instructions': """1. Contact your primary care physician for referrals
2. Check with your insurance for covered mental health providers
3. Research therapists who specialize in your specific concerns
4. Consider online therapy platforms if in-person isn't accessible
5. Don't hesitate to try different therapists to find the right fit
6. Be honest and open during sessions for best results""",
                'duration_minutes': 60,
                'severity_levels': ['moderately_severe', 'severe'],
                'questionnaires': [phq9, gad7]
            }
        ]
        
        for rec_data in recommendations_data:
            questionnaires = rec_data.pop('questionnaires', [])
            severity_levels = rec_data.pop('severity_levels', [])
            
            recommendation, created = Recommendation.objects.get_or_create(
                title=rec_data['title'],
                defaults={
                    **rec_data,
                    'severity_levels': severity_levels,
                    'is_active': True
                }
            )
            
            if created:
                # Add questionnaire relationships
                for questionnaire in questionnaires:
                    recommendation.applicable_questionnaires.add(questionnaire)
                
                self.stdout.write(f'Created recommendation: {rec_data["title"]}')