"""
Views for assessment and recommendation pages
"""
import uuid
import json
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import PHQ9Result, GAD7Result, GHQResult, ComprehensiveAssessment, MoodEntry, SleepEntry


class AssessmentView(TemplateView):
    """Assessment page view with psychological screening tools"""
    template_name = 'assessment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Level of Problem through Standard Psychological Screening Tools'
        context['page_description'] = 'Complete standardized psychological assessments to identify your current mental health status.'
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle comprehensive assessment submission"""
        try:
            # Get or create session ID for anonymous users
            session_id = request.session.get('assessment_session')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['assessment_session'] = session_id
            
            # Process PHQ-9 data
            phq9_data = self.extract_phq9_data(request.POST)
            phq9_result = None
            if phq9_data:
                phq9_result = PHQ9Result.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_id=session_id,
                    **phq9_data
                )
            
            # Process GAD-7 data
            gad7_data = self.extract_gad7_data(request.POST)
            gad7_result = None
            if gad7_data:
                gad7_result = GAD7Result.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_id=session_id,
                    **gad7_data
                )
            
            # Process GHQ-12 data
            ghq_data = self.extract_ghq_data(request.POST)
            ghq_result = None
            if ghq_data:
                ghq_result = GHQResult.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_id=session_id,
                    **ghq_data
                )
            
            # Check if at least one assessment was completed
            if not any([phq9_result, gad7_result, ghq_result]):
                messages.error(request, 'Please complete at least one assessment before submitting.')
                return self.get(request, *args, **kwargs)
            
            # Create comprehensive assessment
            comprehensive = ComprehensiveAssessment.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id,
                phq9_result=phq9_result,
                gad7_result=gad7_result,
                ghq_result=ghq_result
            )
            
            # Store assessment ID in session for recommendations
            request.session['latest_assessment_id'] = comprehensive.id
            
            messages.success(request, 'Assessment completed successfully! Redirecting to your personalized recommendations.')
            return redirect('recommendation')
            
        except Exception as e:
            messages.error(request, f'Error processing assessment: {str(e)}')
            return self.get(request, *args, **kwargs)
    
    def extract_phq9_data(self, post_data):
        """Extract PHQ-9 responses from POST data"""
        field_mapping = {
            'phq9_q1': 'q1_interest',
            'phq9_q2': 'q2_mood', 
            'phq9_q3': 'q3_sleep',
            'phq9_q4': 'q4_energy',
            'phq9_q5': 'q5_appetite',
            'phq9_q6': 'q6_self_worth',
            'phq9_q7': 'q7_concentration',
            'phq9_q8': 'q8_movement',
            'phq9_q9': 'q9_self_harm'
        }
        data = {}
        
        for form_field, model_field in field_mapping.items():
            if form_field in post_data:
                data[model_field] = int(post_data[form_field])
        
        return data if len(data) == 9 else None
    
    def extract_gad7_data(self, post_data):
        """Extract GAD-7 responses from POST data"""
        field_mapping = {
            'gad7_q1': 'q1_nervous',
            'gad7_q2': 'q2_control_worry',
            'gad7_q3': 'q3_worry_much',
            'gad7_q4': 'q4_trouble_relaxing',
            'gad7_q5': 'q5_restless',
            'gad7_q6': 'q6_irritable',
            'gad7_q7': 'q7_afraid'
        }
        data = {}
        
        for form_field, model_field in field_mapping.items():
            if form_field in post_data:
                data[model_field] = int(post_data[form_field])
        
        return data if len(data) == 7 else None
    
    def extract_ghq_data(self, post_data):
        """Extract GHQ-12 responses from POST data"""
        field_mapping = {
            'ghq_q1': 'q1_concentration',
            'ghq_q2': 'q2_sleep_loss',
            'ghq_q3': 'q3_useful_role',
            'ghq_q4': 'q4_decision_making',
            'ghq_q5': 'q5_strain',
            'ghq_q6': 'q6_problems',
            'ghq_q7': 'q7_enjoyment',
            'ghq_q8': 'q8_face_problems',
            'ghq_q9': 'q9_unhappy',
            'ghq_q10': 'q10_confidence',
            'ghq_q11': 'q11_worthless',
            'ghq_q12': 'q12_happiness'
        }
        data = {}
        
        for form_field, model_field in field_mapping.items():
            if form_field in post_data:
                data[model_field] = int(post_data[form_field])
        
        return data if len(data) == 12 else None


class RecommendationView(TemplateView):
    """Recommendation page view with score-based suggestions"""
    template_name = 'recommendation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Personalized Recommendations'
        context['page_description'] = 'Based on your assessment, here are personalized recommendations for your mental health journey.'
        
        # Get latest assessment results
        assessment_id = self.request.session.get('latest_assessment_id')
        if assessment_id:
            try:
                assessment = ComprehensiveAssessment.objects.get(id=assessment_id)
                context['assessment'] = assessment
                context['phq9_result'] = assessment.phq9_result
                context['gad7_result'] = assessment.gad7_result
                context['ghq_result'] = assessment.ghq_result
                context['overall_risk'] = assessment.get_overall_risk_level()
                
                # Generate personalized recommendations based on scores
                context['recommendations'] = self.generate_recommendations(assessment)
                
            except ComprehensiveAssessment.DoesNotExist:
                context['assessment'] = None
        else:
            context['assessment'] = None
            
        return context
    
    def generate_recommendations(self, assessment):
        """Generate personalized recommendations based on assessment scores"""
        recommendations = {
            'immediate_actions': [],
            'long_term_strategies': [],
            'professional_help': [],
            'resources': [],
            'emergency_level': False
        }
        
        # PHQ-9 based recommendations
        if assessment.phq9_result:
            phq9_score = assessment.phq9_result.total_score
            phq9_severity = assessment.phq9_result.severity_level
            
            if phq9_severity == 'minimal':
                recommendations['immediate_actions'].append({
                    'title': 'Maintain Mental Wellness',
                    'description': 'Continue your current positive mental health practices.',
                    'icon': 'bi-heart'
                })
            elif phq9_severity == 'mild':
                recommendations['immediate_actions'].append({
                    'title': 'Lifestyle Adjustments',
                    'description': 'Focus on regular exercise, healthy sleep, and stress management.',
                    'icon': 'bi-activity'
                })
                recommendations['long_term_strategies'].append({
                    'title': 'Monitor Mood',
                    'description': 'Keep a daily mood journal to track patterns.',
                    'icon': 'bi-journal-text'
                })
            elif phq9_severity in ['moderate', 'moderately_severe']:
                recommendations['professional_help'].append({
                    'title': 'Counseling Recommended',
                    'description': 'Consider speaking with a mental health professional.',
                    'icon': 'bi-person-heart',
                    'priority': 'high'
                })
                recommendations['immediate_actions'].append({
                    'title': 'Crisis Support Plan',
                    'description': 'Develop a plan for managing difficult moments.',
                    'icon': 'bi-shield-check'
                })
            elif phq9_severity == 'severe':
                recommendations['emergency_level'] = True
                recommendations['professional_help'].append({
                    'title': 'Immediate Professional Help',
                    'description': 'Please contact a mental health professional immediately.',
                    'icon': 'bi-exclamation-triangle',
                    'priority': 'urgent'
                })
            
            # Check for self-harm indicators
            if assessment.phq9_result.q9_self_harm > 0:
                recommendations['emergency_level'] = True
                recommendations['professional_help'].insert(0, {
                    'title': 'Crisis Intervention',
                    'description': 'Please seek immediate help if you are having thoughts of self-harm.',
                    'icon': 'bi-telephone',
                    'priority': 'emergency'
                })
        
        # GAD-7 based recommendations
        if assessment.gad7_result:
            gad7_severity = assessment.gad7_result.severity_level
            
            if gad7_severity in ['moderate', 'severe']:
                recommendations['immediate_actions'].append({
                    'title': 'Anxiety Management Techniques',
                    'description': 'Practice deep breathing, progressive muscle relaxation, and mindfulness.',
                    'icon': 'bi-lungs'
                })
                recommendations['long_term_strategies'].append({
                    'title': 'Anxiety Therapy',
                    'description': 'Consider Cognitive Behavioral Therapy (CBT) for anxiety.',
                    'icon': 'bi-brain'
                })
        
        # GHQ-12 based recommendations
        if assessment.ghq_result:
            ghq_risk = assessment.ghq_result.severity_level
            
            if ghq_risk in ['moderate_risk', 'high_risk']:
                recommendations['long_term_strategies'].append({
                    'title': 'Holistic Health Approach',
                    'description': 'Address both physical and mental health through integrated care.',
                    'icon': 'bi-heart-pulse'
                })
        
        # Add general resources
        recommendations['resources'] = [
            {
                'title': 'Mental Health Toolkit',
                'description': 'Comprehensive guide to managing mental health.',
                'type': 'guide'
            },
            {
                'title': 'Meditation App',
                'description': '5-minute guided meditations for daily practice.',
                'type': 'app'
            },
            {
                'title': 'Support Groups',
                'description': 'Connect with others who understand your experience.',
                'type': 'community'
            }
        ]
        
        return recommendations


class GamesView(TemplateView):
    """Games page view for mental health and wellness games"""
    template_name = 'games.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Mental Health & Wellness Games'
        context['page_description'] = 'Interactive games and activities to support your mental health journey.'
        return context


class MoodJournalView(TemplateView):
    """Mood Journal page view with AI insights"""
    template_name = 'mood_journal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Mood Journal'
        context['page_description'] = 'Track your daily moods and discover patterns with AI-powered insights.'
        
        # Get user's recent mood entries
        session_id = self.request.session.get('mood_journal_session')
        if not session_id:
            session_id = str(uuid.uuid4())
            self.request.session['mood_journal_session'] = session_id
        
        # Filter entries based on user or session
        entries_filter = {}
        if self.request.user.is_authenticated:
            entries_filter['user'] = self.request.user
        else:
            entries_filter['session_id'] = session_id
        
        # Get recent entries (last 30 days)
        recent_entries = MoodEntry.objects.filter(**entries_filter).order_by('-created_at')[:30]
        context['recent_entries'] = recent_entries
        
        # Generate AI insights
        context['ai_insights'] = self.generate_ai_insights(self.request.user, session_id)
        
        # Mood choices for the form
        context['mood_choices'] = MoodEntry.MOOD_CHOICES
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle mood journal entry submission"""
        try:
            mood = request.POST.get('mood')
            note = request.POST.get('note', '')
            
            if not mood:
                messages.error(request, 'Please select a mood before submitting.')
                return self.get(request, *args, **kwargs)
            
            # Get or create session ID for anonymous users
            session_id = request.session.get('mood_journal_session')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['mood_journal_session'] = session_id
            
            # Create mood entry
            mood_entry = MoodEntry.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id if not request.user.is_authenticated else None,
                mood=mood,
                note=note
            )
            
            messages.success(request, f'Mood entry saved! Feeling {mood_entry.get_mood_emoji()} {mood_entry.get_mood_label()} today.')
            return redirect('mood_journal')
            
        except Exception as e:
            messages.error(request, f'Error saving mood entry: {str(e)}')
            return self.get(request, *args, **kwargs)
    
    def generate_ai_insights(self, user, session_id):
        """Generate AI-powered insights from mood patterns"""
        import random
        from datetime import datetime, timedelta
        
        # Get mood patterns
        patterns = MoodEntry.get_user_mood_patterns(user, session_id, days=30)
        
        if not patterns or patterns.get('total_entries', 0) < 3:
            return {
                'status': 'insufficient_data',
                'message': 'Keep tracking your mood for a few more days to unlock AI insights!',
                'suggestions': [
                    'Track your mood daily for better insights',
                    'Add detailed notes to help understand your feelings',
                    'Try our breathing exercises when feeling stressed'
                ]
            }
        
        insights = {
            'status': 'ready',
            'patterns': [],
            'suggestions': [],
            'positive_notes': []
        }
        
        # Analyze most common mood
        if patterns.get('most_common_mood'):
            most_common, count = patterns['most_common_mood']
            percentage = (count / patterns['total_entries']) * 100
            
            mood_labels = {
                'happy': 'happy',
                'sad': 'sad', 
                'angry': 'frustrated',
                'tired': 'tired',
                'anxious': 'anxious'
            }
            
            mood_label = mood_labels.get(most_common, most_common)
            insights['patterns'].append(
                f"You've been feeling {mood_label} {percentage:.0f}% of the time over the past month."
            )
            
            # Generate mood-specific suggestions
            if most_common == 'anxious':
                insights['suggestions'].extend([
                    'Try our breathing exercises when feeling anxious',
                    'Consider practicing mindfulness meditation',
                    'Regular physical exercise can help reduce anxiety'
                ])
            elif most_common == 'sad':
                insights['suggestions'].extend([
                    'Connect with friends or family when feeling down',
                    'Try gratitude journaling to shift focus to positive aspects',
                    'Consider talking to a mental health professional'
                ])
            elif most_common == 'angry':
                insights['suggestions'].extend([
                    'Practice deep breathing when feeling frustrated',
                    'Try physical exercise to release tension',
                    'Consider what triggers your anger and plan responses'
                ])
            elif most_common == 'tired':
                insights['suggestions'].extend([
                    'Ensure you\'re getting 7-9 hours of sleep',
                    'Check if stress might be affecting your energy',
                    'Consider your nutrition and hydration habits'
                ])
            elif most_common == 'happy':
                insights['positive_notes'].extend([
                    'Great to see you\'re feeling happy most of the time!',
                    'You\'re doing something right - keep it up!'
                ])
        
        # Analyze weekday patterns
        weekday_patterns = patterns.get('weekday_patterns', {})
        if weekday_patterns:
            # Find days with consistent patterns
            problematic_days = []
            good_days = []
            
            for day, day_data in weekday_patterns.items():
                if day_data['count'] >= 2:  # At least 2 entries for this day
                    if day_data['most_common'] in ['sad', 'anxious', 'angry']:
                        problematic_days.append(day)
                    elif day_data['most_common'] == 'happy':
                        good_days.append(day)
            
            if problematic_days:
                if len(problematic_days) == 1:
                    insights['patterns'].append(
                        f"You often feel stressed on {problematic_days[0]}s. "
                        "Consider what happens on this day that might affect your mood."
                    )
                else:
                    day_list = ', '.join(problematic_days[:-1]) + f" and {problematic_days[-1]}s"
                    insights['patterns'].append(
                        f"You tend to feel more stressed on {day_list}. "
                        "Think about what these days have in common."
                    )
                
                insights['suggestions'].append(
                    'Plan self-care activities on your challenging days'
                )
            
            if good_days:
                insights['positive_notes'].append(
                    f"You consistently feel good on {good_days[0] if len(good_days) == 1 else 'several days'}!"
                )
        
        # Add general suggestions based on entry count
        if patterns['total_entries'] >= 7:
            insights['positive_notes'].append('Great job maintaining your mood journal!')
        
        # Always include some helpful suggestions
        general_suggestions = [
            'Try 5 minutes of mindful breathing daily',
            'Regular physical activity can boost mood',
            'Maintain a consistent sleep schedule',
            'Connect with supportive people in your life',
            'Practice gratitude by noting 3 good things daily'
        ]
        
        # Add random general suggestions if we don't have enough specific ones
        while len(insights['suggestions']) < 3:
            suggestion = random.choice(general_suggestions)
            if suggestion not in insights['suggestions']:
                insights['suggestions'].append(suggestion)
        
        return insights


class SleepTrackerView(TemplateView):
    """Sleep Tracker page view with AI insights"""
    template_name = 'sleep_tracker.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sleep Tracker'
        context['page_description'] = 'Track your sleep patterns and improve your rest with AI-powered insights.'
        
        # Get user's recent sleep entries
        session_id = self.request.session.get('sleep_tracker_session')
        if not session_id:
            session_id = str(uuid.uuid4())
            self.request.session['sleep_tracker_session'] = session_id
        
        # Filter entries based on user or session
        entries_filter = {}
        if self.request.user.is_authenticated:
            entries_filter['user'] = self.request.user
        else:
            entries_filter['session_id'] = session_id
        
        # Get recent entries (last 14 days)
        recent_entries = SleepEntry.objects.filter(**entries_filter).order_by('-sleep_date')[:14]
        context['recent_entries'] = recent_entries
        
        # Generate AI insights
        context['ai_insights'] = self.generate_ai_sleep_insights(self.request.user, session_id)
        
        # Sleep quality choices for the form
        context['quality_choices'] = SleepEntry.QUALITY_CHOICES
        
        # Prepare chart data
        context['chart_data'] = self.prepare_chart_data(recent_entries)
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle sleep entry submission"""
        try:
            # Extract form data
            sleep_date = request.POST.get('sleep_date')
            bedtime = request.POST.get('bedtime')
            wake_time = request.POST.get('wake_time')
            quality = request.POST.get('quality')
            time_to_fall_asleep = request.POST.get('time_to_fall_asleep')
            times_woken = request.POST.get('times_woken', 0)
            feeling_rested = request.POST.get('feeling_rested') == 'on'
            notes = request.POST.get('notes', '')
            
            # Sleep factors
            screen_time_before_bed = request.POST.get('screen_time_before_bed') == 'on'
            caffeine_intake = request.POST.get('caffeine_intake') == 'on'
            exercise_today = request.POST.get('exercise_today') == 'on'
            stress_level = request.POST.get('stress_level')
            
            # Validate required fields
            if not all([sleep_date, bedtime, wake_time, quality]):
                messages.error(request, 'Please fill in all required fields.')
                return self.get(request, *args, **kwargs)
            
            # Calculate duration
            from datetime import datetime, timedelta
            bedtime_dt = datetime.strptime(bedtime, '%H:%M').time()
            wake_time_dt = datetime.strptime(wake_time, '%H:%M').time()
            
            # Handle sleep across midnight
            bedtime_datetime = datetime.combine(datetime.strptime(sleep_date, '%Y-%m-%d').date(), bedtime_dt)
            wake_time_datetime = datetime.combine(datetime.strptime(sleep_date, '%Y-%m-%d').date(), wake_time_dt)
            
            if wake_time_dt < bedtime_dt:
                # Sleep went past midnight
                wake_time_datetime += timedelta(days=1)
            
            duration_hours = (wake_time_datetime - bedtime_datetime).total_seconds() / 3600
            
            # Get or create session ID for anonymous users
            session_id = request.session.get('sleep_tracker_session')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['sleep_tracker_session'] = session_id
            
            # Create or update sleep entry
            sleep_entry, created = SleepEntry.objects.update_or_create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id if not request.user.is_authenticated else None,
                sleep_date=sleep_date,
                defaults={
                    'bedtime': bedtime_dt,
                    'wake_time': wake_time_dt,
                    'duration_hours': duration_hours,
                    'quality': int(quality),
                    'time_to_fall_asleep': int(time_to_fall_asleep) if time_to_fall_asleep else None,
                    'times_woken': int(times_woken),
                    'feeling_rested': feeling_rested,
                    'notes': notes,
                    'screen_time_before_bed': screen_time_before_bed,
                    'caffeine_intake': caffeine_intake,
                    'exercise_today': exercise_today,
                    'stress_level': int(stress_level) if stress_level else None,
                }
            )
            
            action = "updated" if not created else "saved"
            messages.success(request, f'Sleep entry {action} successfully! Duration: {duration_hours:.1f} hours, Quality: {sleep_entry.get_quality_label()}')
            return redirect('sleep_tracker')
            
        except ValueError as e:
            messages.error(request, f'Invalid data format: {str(e)}')
            return self.get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Error saving sleep entry: {str(e)}')
            return self.get(request, *args, **kwargs)
    
    def prepare_chart_data(self, entries):
        """Prepare data for sleep charts"""
        chart_data = {
            'labels': [],
            'duration_data': [],
            'quality_data': [],
            'bedtime_data': [],
            'efficiency_data': []
        }
        
        for entry in reversed(entries):  # Show oldest to newest in chart
            chart_data['labels'].append(entry.sleep_date.strftime('%m/%d'))
            chart_data['duration_data'].append(entry.duration_hours)
            chart_data['quality_data'].append(entry.quality)
            
            # Convert bedtime to decimal hours for charting
            bedtime_decimal = entry.bedtime.hour + entry.bedtime.minute / 60.0
            chart_data['bedtime_data'].append(bedtime_decimal)
            
            # Sleep efficiency
            efficiency = entry.get_sleep_efficiency()
            chart_data['efficiency_data'].append(efficiency if efficiency else 0)
        
        return chart_data
    
    def generate_ai_sleep_insights(self, user, session_id):
        """Generate AI-powered sleep insights and tips"""
        import random
        
        # Get sleep patterns
        patterns = SleepEntry.get_user_sleep_patterns(user, session_id, days=14)
        
        if not patterns or patterns.get('total_entries', 0) < 3:
            return {
                'status': 'insufficient_data',
                'message': 'Track your sleep for a few more nights to unlock personalized AI insights!',
                'general_tips': [
                    'Aim for 7-9 hours of sleep each night',
                    'Keep a consistent sleep schedule',
                    'Create a relaxing bedtime routine',
                    'Keep your bedroom cool and dark'
                ]
            }
        
        insights = {
            'status': 'ready',
            'patterns': [],
            'recommendations': [],
            'positive_notes': [],
            'sleep_score': self.calculate_sleep_score(patterns)
        }
        
        # Analyze sleep duration
        avg_duration = patterns.get('avg_duration', 0)
        if avg_duration < 7:
            insights['patterns'].append(f"You're averaging {avg_duration:.1f} hours of sleep. Most adults need 7-9 hours.")
            insights['recommendations'].extend([
                'Try going to bed 30 minutes earlier',
                'Limit screen time 1 hour before bed',
                'Avoid large meals close to bedtime'
            ])
        elif avg_duration > 9:
            insights['patterns'].append(f"You're sleeping {avg_duration:.1f} hours on average - quite a bit!")
            insights['recommendations'].append('Consider if you might be oversleeping due to poor sleep quality')
        else:
            insights['positive_notes'].append(f"Great job! You're averaging {avg_duration:.1f} hours of sleep.")
        
        # Analyze sleep quality
        avg_quality = patterns.get('avg_quality', 0)
        if avg_quality < 3:
            insights['patterns'].append('Your sleep quality has been below average recently.')
            insights['recommendations'].extend([
                'Try a relaxing bedtime routine',
                'Consider meditation or deep breathing exercises',
                'Keep a cool, comfortable sleep environment'
            ])
        elif avg_quality >= 4:
            insights['positive_notes'].append('Your sleep quality has been consistently good!')
        
        # Analyze sleep consistency
        consistency = patterns.get('sleep_consistency', 0)
        if consistency > 1.5:
            insights['patterns'].append('Your sleep duration varies quite a bit night to night.')
            insights['recommendations'].extend([
                'Try to maintain a consistent bedtime and wake time',
                'Set a phone reminder for your target bedtime'
            ])
        elif consistency < 0.5:
            insights['positive_notes'].append('You have very consistent sleep patterns!')
        
        # Analyze behavioral factors
        screen_frequency = patterns.get('screen_time_frequency', 0)
        if screen_frequency > 0.5:
            insights['patterns'].append(f"You use screens before bed {screen_frequency*100:.0f}% of the time.")
            insights['recommendations'].append('Try reading a book or practicing relaxation instead of screen time before bed')
        
        caffeine_frequency = patterns.get('caffeine_frequency', 0)
        if caffeine_frequency > 0.3:
            insights['patterns'].append(f"You consume caffeine in the evening {caffeine_frequency*100:.0f}% of the time.")
            insights['recommendations'].append('Try to avoid caffeine after 2 PM for better sleep')
        
        # Analyze bedtime patterns
        avg_bedtime = patterns.get('avg_bedtime', 0)
        if avg_bedtime > 24:  # After midnight
            bedtime_hour = int(avg_bedtime - 24)
            insights['patterns'].append(f"You typically go to bed around {bedtime_hour}:{'00' if avg_bedtime % 1 == 0 else '30'} AM.")
            insights['recommendations'].append('Consider gradually shifting your bedtime earlier by 15 minutes each night')
        elif avg_bedtime > 23:  # Late evening
            bedtime_hour = int(avg_bedtime)
            insights['patterns'].append(f"You're a night owl, typically going to bed around {bedtime_hour}:{'00' if avg_bedtime % 1 == 0 else '30'} PM.")
        
        # Add general recommendations if we don't have enough specific ones
        general_recommendations = [
            'Try progressive muscle relaxation before bed',
            'Use blackout curtains or an eye mask',
            'Keep your bedroom temperature between 65-68°F',
            'Try a warm bath or shower before bed',
            'Listen to calming sleep sounds or white noise',
            'Practice gratitude or journaling before sleep'
        ]
        
        while len(insights['recommendations']) < 3:
            rec = random.choice(general_recommendations)
            if rec not in insights['recommendations']:
                insights['recommendations'].append(rec)
        
        return insights
    
    def calculate_sleep_score(self, patterns):
        """Calculate overall sleep score (0-100)"""
        if not patterns:
            return 0
        
        score = 0
        
        # Duration score (40 points max)
        avg_duration = patterns.get('avg_duration', 0)
        if 7 <= avg_duration <= 9:
            duration_score = 40
        elif 6.5 <= avg_duration < 7 or 9 < avg_duration <= 9.5:
            duration_score = 30
        elif 6 <= avg_duration < 6.5 or 9.5 < avg_duration <= 10:
            duration_score = 20
        else:
            duration_score = 10
        score += duration_score
        
        # Quality score (30 points max)
        avg_quality = patterns.get('avg_quality', 0)
        quality_score = min((avg_quality / 5) * 30, 30)
        score += quality_score
        
        # Consistency score (20 points max)
        consistency = patterns.get('sleep_consistency', 0)
        if consistency < 0.5:
            consistency_score = 20
        elif consistency < 1:
            consistency_score = 15
        elif consistency < 1.5:
            consistency_score = 10
        else:
            consistency_score = 5
        score += consistency_score
        
        # Sleep hygiene score (10 points max)
        screen_penalty = patterns.get('screen_time_frequency', 0) * 5
        caffeine_penalty = patterns.get('caffeine_frequency', 0) * 5
        hygiene_score = max(10 - screen_penalty - caffeine_penalty, 0)
        score += hygiene_score
        
        return min(int(score), 100)


def mood_journal_entries_api(request):
    """API endpoint to return mood journal entries as JSON"""
    try:
        # Get user's session info
        session_id = request.session.get('mood_journal_session')
        
        # Filter entries based on user or session
        entries_filter = {}
        if request.user.is_authenticated:
            entries_filter['user'] = request.user
        elif session_id:
            entries_filter['session_id'] = session_id
        else:
            return JsonResponse({'entries': []})
        
        # Get all entries ordered by newest first
        entries = MoodEntry.objects.filter(**entries_filter).order_by('-created_at')
        
        # Convert to JSON-serializable format
        entries_data = []
        for entry in entries:
            # Check if there's a sleep entry for the same date
            sleep_data = None
            try:
                from datetime import date
                entry_date = entry.created_at.date()
                sleep_entry = SleepEntry.objects.filter(
                    **entries_filter,
                    sleep_date=entry_date
                ).first()
                
                if sleep_entry:
                    sleep_data = {
                        'duration': f"{sleep_entry.duration_hours:.1f}h",
                        'quality': sleep_entry.quality,
                        'efficiency': sleep_entry.get_sleep_efficiency()
                    }
            except:
                pass
                
            entries_data.append({
                'id': entry.id,
                'mood': entry.mood,
                'mood_emoji': entry.get_mood_emoji(),
                'mood_label': entry.get_mood_label(),
                'note': entry.note,
                'created_at': entry.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'created_date': entry.created_at.strftime('%B %d, %Y'),
                'created_time': entry.created_at.strftime('%I:%M %p'),
                'entry_date': entry.created_at.strftime('%Y-%m-%d'),  # For calendar mapping
                'relative_time': get_relative_time(entry.created_at),
                'sleep_data': sleep_data,
                'emotions': []  # Could be expanded to include emotion tags
            })
        
        return JsonResponse({
            'entries': entries_data,
            'total_count': len(entries_data)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def sleep_journal_entries_api(request):
    """API endpoint to return sleep journal entries as JSON"""
    try:
        # Get user's session info
        session_id = request.session.get('sleep_tracker_session')
        
        # Filter entries based on user or session
        entries_filter = {}
        if request.user.is_authenticated:
            entries_filter['user'] = request.user
        elif session_id:
            entries_filter['session_id'] = session_id
        else:
            return JsonResponse({'entries': []})
        
        # Get all entries ordered by newest first
        entries = SleepEntry.objects.filter(**entries_filter).order_by('-sleep_date', '-created_at')
        
        # Convert to JSON-serializable format
        entries_data = []
        for entry in entries:
            # Prepare sleep factors
            factors = []
            if entry.screen_time_before_bed:
                factors.append({'name': '📱 Screen time', 'type': 'negative'})
            if entry.caffeine_intake:
                factors.append({'name': '☕ Evening caffeine', 'type': 'negative'})
            if entry.exercise_today:
                factors.append({'name': '🏃 Exercised', 'type': 'positive'})
            
            # Check if there's a mood entry for the same date
            mood_data = None
            try:
                mood_entry = MoodEntry.objects.filter(
                    **entries_filter,
                    created_at__date=entry.sleep_date
                ).first()
                
                if mood_entry:
                    mood_data = {
                        'emoji': mood_entry.get_mood_emoji(),
                        'label': mood_entry.get_mood_label(),
                        'mood': mood_entry.mood
                    }
            except:
                pass
            
            entries_data.append({
                'id': entry.id,
                'sleep_date': entry.sleep_date.strftime('%Y-%m-%d'),
                'sleep_date_formatted': entry.sleep_date.strftime('%B %d, %Y'),
                'bedtime': entry.bedtime.strftime('%I:%M %p'),
                'wake_time': entry.wake_time.strftime('%I:%M %p'),
                'duration_hours': float(entry.duration_hours),
                'duration_formatted': f"{entry.duration_hours:.1f} hours",
                'quality': entry.quality,
                'quality_label': entry.get_quality_label(),
                'quality_stars': [i <= entry.quality for i in range(1, 6)],
                'feeling_rested': entry.feeling_rested,
                'time_to_fall_asleep': entry.time_to_fall_asleep,
                'times_woken': entry.times_woken,
                'stress_level': entry.stress_level,
                'notes': entry.notes,
                'sleep_factors': factors,
                'created_at': entry.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'relative_time': get_relative_time(entry.created_at),
                'sleep_efficiency': entry.get_sleep_efficiency(),
                'mood_data': mood_data
            })
        
        return JsonResponse({
            'entries': entries_data,
            'total_count': len(entries_data)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_relative_time(datetime_obj):
    """Get human-readable relative time"""
    from django.utils import timezone
    from datetime import timedelta
    
    now = timezone.now()
    diff = now - datetime_obj
    
    if diff.days > 7:
        return datetime_obj.strftime('%B %d, %Y')
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"
