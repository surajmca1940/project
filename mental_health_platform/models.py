"""
Models for mental health assessment results
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AssessmentResult(models.Model):
    """Base model for assessment results"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, help_text="Session ID for anonymous users")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class PHQ9Result(AssessmentResult):
    """PHQ-9 Depression Assessment Results"""
    
    # PHQ-9 Questions (0-3 scale)
    q1_interest = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Little interest or pleasure in doing things")
    q2_mood = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Feeling down, depressed, or hopeless")
    q3_sleep = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Trouble falling/staying asleep or sleeping too much")
    q4_energy = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Feeling tired or having little energy")
    q5_appetite = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Poor appetite or overeating")
    q6_self_worth = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Feeling bad about yourself")
    q7_concentration = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Trouble concentrating")
    q8_movement = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Moving or speaking slowly/restlessly")
    q9_self_harm = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Thoughts of being better off dead or hurting yourself")
    
    # Calculated fields
    total_score = models.IntegerField(default=0)
    severity_level = models.CharField(max_length=20, choices=[
        ('minimal', 'Minimal (0-4)'),
        ('mild', 'Mild (5-9)'),
        ('moderate', 'Moderate (10-14)'),
        ('moderately_severe', 'Moderately Severe (15-19)'),
        ('severe', 'Severe (20-27)')
    ])
    
    def calculate_score(self):
        """Calculate total PHQ-9 score and determine severity"""
        self.total_score = sum([
            self.q1_interest, self.q2_mood, self.q3_sleep, self.q4_energy,
            self.q5_appetite, self.q6_self_worth, self.q7_concentration,
            self.q8_movement, self.q9_self_harm
        ])
        
        # Determine severity level
        if self.total_score <= 4:
            self.severity_level = 'minimal'
        elif self.total_score <= 9:
            self.severity_level = 'mild'
        elif self.total_score <= 14:
            self.severity_level = 'moderate'
        elif self.total_score <= 19:
            self.severity_level = 'moderately_severe'
        else:
            self.severity_level = 'severe'
    
    def save(self, *args, **kwargs):
        self.calculate_score()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "PHQ-9 Assessment Result"
        verbose_name_plural = "PHQ-9 Assessment Results"


class GAD7Result(AssessmentResult):
    """GAD-7 Anxiety Assessment Results"""
    
    # GAD-7 Questions (0-3 scale)
    q1_nervous = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Feeling nervous, anxious, or on edge")
    q2_control_worry = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Not being able to stop or control worrying")
    q3_worry_much = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Worrying too much about different things")
    q4_trouble_relaxing = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Trouble relaxing")
    q5_restless = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Being so restless that it's hard to sit still")
    q6_irritable = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Becoming easily annoyed or irritable")
    q7_afraid = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Feeling afraid as if something awful might happen")
    
    # Calculated fields
    total_score = models.IntegerField(default=0)
    severity_level = models.CharField(max_length=20, choices=[
        ('minimal', 'Minimal (0-4)'),
        ('mild', 'Mild (5-9)'),
        ('moderate', 'Moderate (10-14)'),
        ('severe', 'Severe (15-21)')
    ])
    
    def calculate_score(self):
        """Calculate total GAD-7 score and determine severity"""
        self.total_score = sum([
            self.q1_nervous, self.q2_control_worry, self.q3_worry_much,
            self.q4_trouble_relaxing, self.q5_restless, self.q6_irritable, self.q7_afraid
        ])
        
        # Determine severity level
        if self.total_score <= 4:
            self.severity_level = 'minimal'
        elif self.total_score <= 9:
            self.severity_level = 'mild'
        elif self.total_score <= 14:
            self.severity_level = 'moderate'
        else:
            self.severity_level = 'severe'
    
    def save(self, *args, **kwargs):
        self.calculate_score()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "GAD-7 Assessment Result"
        verbose_name_plural = "GAD-7 Assessment Results"


class GHQResult(AssessmentResult):
    """GHQ-12 General Health Assessment Results"""
    
    # GHQ-12 Questions (0-3 scale: Better than usual, Same as usual, Worse than usual, Much worse than usual)
    q1_concentration = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Been able to concentrate on whatever you're doing")
    q2_sleep_loss = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Lost much sleep over worry")
    q3_useful_role = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Felt that you are playing a useful part in things")
    q4_decision_making = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Felt capable of making decisions about things")
    q5_strain = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Felt constantly under strain")
    q6_problems = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Felt you couldn't overcome your difficulties")
    q7_enjoyment = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Been able to enjoy your normal day-to-day activities")
    q8_face_problems = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Been able to face up to your problems")
    q9_unhappy = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Been feeling unhappy and depressed")
    q10_confidence = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Been losing confidence in yourself")
    q11_worthless = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Been thinking of yourself as a worthless person")
    q12_happiness = models.IntegerField(choices=[(i, i) for i in range(4)], help_text="Been feeling reasonably happy, all things considered")
    
    # Calculated fields
    total_score = models.IntegerField(default=0)
    severity_level = models.CharField(max_length=20, choices=[
        ('low_risk', 'Low Risk (0-15)'),
        ('moderate_risk', 'Moderate Risk (16-20)'),
        ('high_risk', 'High Risk (21-36)')
    ])
    
    def calculate_score(self):
        """Calculate total GHQ-12 score and determine risk level"""
        # GHQ scoring: positive items (1,3,4,7,8,12) are reverse scored
        positive_items = [self.q1_concentration, self.q3_useful_role, self.q4_decision_making, 
                         self.q7_enjoyment, self.q8_face_problems, self.q12_happiness]
        negative_items = [self.q2_sleep_loss, self.q5_strain, self.q6_problems, 
                         self.q9_unhappy, self.q10_confidence, self.q11_worthless]
        
        # Reverse score positive items (3-value)
        reversed_positive = [3 - item for item in positive_items]
        
        self.total_score = sum(reversed_positive + negative_items)
        
        # Determine risk level
        if self.total_score <= 15:
            self.severity_level = 'low_risk'
        elif self.total_score <= 20:
            self.severity_level = 'moderate_risk'
        else:
            self.severity_level = 'high_risk'
    
    def save(self, *args, **kwargs):
        self.calculate_score()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "GHQ-12 Assessment Result"
        verbose_name_plural = "GHQ-12 Assessment Results"


class ComprehensiveAssessment(models.Model):
    """Combined assessment results"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, help_text="Session ID for anonymous users")
    phq9_result = models.OneToOneField(PHQ9Result, on_delete=models.CASCADE, null=True, blank=True)
    gad7_result = models.OneToOneField(GAD7Result, on_delete=models.CASCADE, null=True, blank=True)
    ghq_result = models.OneToOneField(GHQResult, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def get_overall_risk_level(self):
        """Determine overall risk level based on all assessments"""
        risk_levels = []
        
        if self.phq9_result:
            if self.phq9_result.severity_level in ['moderate', 'moderately_severe', 'severe']:
                risk_levels.append('high')
            elif self.phq9_result.severity_level == 'mild':
                risk_levels.append('moderate')
            else:
                risk_levels.append('low')
        
        if self.gad7_result:
            if self.gad7_result.severity_level in ['moderate', 'severe']:
                risk_levels.append('high')
            elif self.gad7_result.severity_level == 'mild':
                risk_levels.append('moderate')
            else:
                risk_levels.append('low')
        
        if self.ghq_result:
            if self.ghq_result.severity_level == 'high_risk':
                risk_levels.append('high')
            elif self.ghq_result.severity_level == 'moderate_risk':
                risk_levels.append('moderate')
            else:
                risk_levels.append('low')
        
        # Return highest risk level
        if 'high' in risk_levels:
            return 'high'
        elif 'moderate' in risk_levels:
            return 'moderate'
        else:
            return 'low'
    
    class Meta:
        verbose_name = "Comprehensive Assessment"
        verbose_name_plural = "Comprehensive Assessments"


class MoodEntry(models.Model):
    """Daily mood journal entries"""
    
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('sad', '😢 Sad'),
        ('angry', '😡 Angry'),
        ('tired', '😴 Tired'),
        ('anxious', '😨 Anxious'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, help_text="Session ID for anonymous users", null=True, blank=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(max_length=500, help_text="How are you feeling today?")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AI insights fields
    ai_analyzed = models.BooleanField(default=False)
    ai_insights = models.JSONField(null=True, blank=True, help_text="AI-generated insights about mood patterns")
    
    def get_mood_emoji(self):
        """Return the emoji for the selected mood"""
        mood_emojis = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😡',
            'tired': '😴',
            'anxious': '😨'
        }
        return mood_emojis.get(self.mood, '😐')
    
    def get_mood_label(self):
        """Return the label for the selected mood"""
        mood_labels = {
            'happy': 'Happy',
            'sad': 'Sad',
            'angry': 'Angry',
            'tired': 'Tired',
            'anxious': 'Anxious'
        }
        return mood_labels.get(self.mood, 'Unknown')
    
    @classmethod
    def get_user_mood_patterns(cls, user=None, session_id=None, days=30):
        """Analyze mood patterns for a user over specified days"""
        from django.utils import timezone
        from datetime import timedelta
        from collections import Counter
        import calendar
        
        # Filter entries
        entries_filter = {}
        if user and user.is_authenticated:
            entries_filter['user'] = user
        elif session_id:
            entries_filter['session_id'] = session_id
        else:
            return {}
        
        # Get recent entries
        since_date = timezone.now() - timedelta(days=days)
        entries = cls.objects.filter(
            created_at__gte=since_date,
            **entries_filter
        ).order_by('-created_at')
        
        if not entries.exists():
            return {}
        
        # Analyze patterns
        moods = [entry.mood for entry in entries]
        mood_counter = Counter(moods)
        
        # Day of week analysis
        weekday_moods = {}
        for entry in entries:
            weekday = calendar.day_name[entry.created_at.weekday()]
            if weekday not in weekday_moods:
                weekday_moods[weekday] = []
            weekday_moods[weekday].append(entry.mood)
        
        # Find patterns
        patterns = {
            'total_entries': entries.count(),
            'most_common_mood': mood_counter.most_common(1)[0] if mood_counter else None,
            'mood_distribution': dict(mood_counter),
            'weekday_patterns': {}
        }
        
        # Analyze weekday patterns
        for day, day_moods in weekday_moods.items():
            day_counter = Counter(day_moods)
            if day_counter:
                patterns['weekday_patterns'][day] = {
                    'most_common': day_counter.most_common(1)[0][0],
                    'count': len(day_moods)
                }
        
        return patterns
    
    class Meta:
        verbose_name = "Mood Journal Entry"
        verbose_name_plural = "Mood Journal Entries"
        ordering = ['-created_at']


class SleepEntry(models.Model):
    """Daily sleep tracking entries"""
    
    QUALITY_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Fair'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, help_text="Session ID for anonymous users", null=True, blank=True)
    
    # Sleep data
    sleep_date = models.DateField(help_text="Date of sleep (when you went to bed)")
    bedtime = models.TimeField(help_text="What time did you go to bed?")
    sleep_time = models.TimeField(help_text="What time did you fall asleep?", null=True, blank=True)
    wake_time = models.TimeField(help_text="What time did you wake up?")
    duration_hours = models.FloatField(help_text="Total sleep duration in hours")
    quality = models.IntegerField(choices=QUALITY_CHOICES, help_text="How would you rate your sleep quality?")
    
    # Additional sleep factors
    time_to_fall_asleep = models.IntegerField(help_text="Minutes it took to fall asleep", null=True, blank=True)
    times_woken = models.IntegerField(help_text="How many times did you wake up?", default=0)
    feeling_rested = models.BooleanField(default=True, help_text="Did you feel rested when you woke up?")
    
    # Optional notes
    notes = models.TextField(max_length=500, blank=True, help_text="Any additional notes about your sleep")
    
    # Sleep environment factors
    screen_time_before_bed = models.BooleanField(default=False, help_text="Did you use screens within 1 hour before bed?")
    caffeine_intake = models.BooleanField(default=False, help_text="Did you consume caffeine in the evening?")
    exercise_today = models.BooleanField(default=False, help_text="Did you exercise today?")
    stress_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True, help_text="Stress level (1-5)")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AI insights fields
    ai_analyzed = models.BooleanField(default=False)
    ai_insights = models.JSONField(null=True, blank=True, help_text="AI-generated sleep insights")
    
    def get_sleep_efficiency(self):
        """Calculate sleep efficiency percentage"""
        if self.time_to_fall_asleep and self.duration_hours:
            time_in_bed = self.duration_hours + (self.time_to_fall_asleep / 60.0)
            return min((self.duration_hours / time_in_bed) * 100, 100)
        return None
    
    def get_quality_label(self):
        """Return human readable quality label"""
        quality_labels = {
            1: 'Very Poor',
            2: 'Poor', 
            3: 'Fair',
            4: 'Good',
            5: 'Excellent'
        }
        return quality_labels.get(self.quality, 'Unknown')
    
    def get_quality_color(self):
        """Return color for quality visualization"""
        colors = {
            1: '#dc3545',  # Red
            2: '#fd7e14',  # Orange
            3: '#ffc107',  # Yellow
            4: '#28a745',  # Green
            5: '#007bff'   # Blue
        }
        return colors.get(self.quality, '#6c757d')
    
    @classmethod
    def get_user_sleep_patterns(cls, user=None, session_id=None, days=14):
        """Analyze sleep patterns for a user over specified days"""
        from django.utils import timezone
        from datetime import timedelta
        from collections import Counter
        import statistics
        
        # Filter entries
        entries_filter = {}
        if user and user.is_authenticated:
            entries_filter['user'] = user
        elif session_id:
            entries_filter['session_id'] = session_id
        else:
            return {}
        
        # Get recent entries
        since_date = timezone.now().date() - timedelta(days=days)
        entries = cls.objects.filter(
            sleep_date__gte=since_date,
            **entries_filter
        ).order_by('-sleep_date')
        
        if not entries.exists():
            return {}
        
        # Calculate patterns
        durations = [entry.duration_hours for entry in entries]
        qualities = [entry.quality for entry in entries]
        bedtimes = [entry.bedtime.hour + entry.bedtime.minute/60.0 for entry in entries]
        wake_times = [entry.wake_time.hour + entry.wake_time.minute/60.0 for entry in entries]
        
        # Sleep issues tracking
        screen_time_count = sum(1 for entry in entries if entry.screen_time_before_bed)
        caffeine_count = sum(1 for entry in entries if entry.caffeine_intake)
        poor_sleep_count = sum(1 for entry in entries if entry.quality <= 2)
        
        patterns = {
            'total_entries': entries.count(),
            'avg_duration': statistics.mean(durations) if durations else 0,
            'avg_quality': statistics.mean(qualities) if qualities else 0,
            'avg_bedtime': statistics.mean(bedtimes) if bedtimes else 0,
            'avg_wake_time': statistics.mean(wake_times) if wake_times else 0,
            'sleep_consistency': statistics.stdev(durations) if len(durations) > 1 else 0,
            'quality_distribution': dict(Counter(qualities)),
            'screen_time_frequency': screen_time_count / len(entries) if entries else 0,
            'caffeine_frequency': caffeine_count / len(entries) if entries else 0,
            'poor_sleep_frequency': poor_sleep_count / len(entries) if entries else 0,
            'recent_entries': list(entries[:7]),
        }
        
        return patterns
    
    def save(self, *args, **kwargs):
        """Calculate sleep time if not provided"""
        if not self.sleep_time and self.time_to_fall_asleep:
            # Calculate sleep time based on bedtime + time to fall asleep
            from datetime import datetime, timedelta
            bedtime_dt = datetime.combine(self.sleep_date, self.bedtime)
            sleep_dt = bedtime_dt + timedelta(minutes=self.time_to_fall_asleep)
            self.sleep_time = sleep_dt.time()
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Sleep Entry"
        verbose_name_plural = "Sleep Entries"
        ordering = ['-sleep_date', '-created_at']
        unique_together = ['user', 'sleep_date']  # One entry per user per date
