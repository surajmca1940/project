from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

from admin_dashboard.models import UserActivity, MentalHealthMetric, Alert, RealTimeMetric
from booking_system.models import Appointment, Counselor
from accounts.models import UserProfile, Institution, Region


class Command(BaseCommand):
    help = 'Populate sample data for admin dashboard testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days of historical data to generate (default: 30)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing dashboard data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing dashboard data...')
            UserActivity.objects.all().delete()
            Alert.objects.all().delete()
            MentalHealthMetric.objects.all().delete()
            RealTimeMetric.objects.all().delete()

        days = options['days']
        self.stdout.write(f'Generating {days} days of sample data...')

        # Create sample institutions and regions if they don't exist
        self.create_sample_infrastructure()
        
        # Create sample users if needed
        self.create_sample_users()
        
        # Generate historical data
        self.generate_user_activities(days)
        self.generate_mental_health_metrics(days)
        self.generate_alerts()
        self.generate_real_time_metrics()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated dashboard with {days} days of sample data'
            )
        )

    def create_sample_infrastructure(self):
        """Create sample institutions and regions"""
        # Create sample region
        region, created = Region.objects.get_or_create(
            name='Sample Region',
            defaults={
                'code': 'SR',
                'cultural_context': {
                    'primary_languages': ['English', 'Hindi'],
                    'cultural_values': ['Community support', 'Family oriented'],
                    'communication_style': 'Direct'
                }
            }
        )
        
        # Create sample institution
        institution, created = Institution.objects.get_or_create(
            name='Sample University',
            defaults={
                'code': 'SAMPLE',
                'institution_type': 'university',
                'region': region,
                'address': 'Sample Address',
                'contact_email': 'contact@sample.edu',
                'contact_phone': '+91-1234567890',
                'timezone': 'Asia/Kolkata',
                'enable_ai_support': True,
                'enable_peer_support': True,
                'enable_anonymous_mode': True
            }
        )

    def create_sample_users(self):
        """Create sample users if needed"""
        if User.objects.count() < 10:
            for i in range(10):
                username = f'testuser{i+1}'
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(
                        username=username,
                        email=f'testuser{i+1}@example.com',
                        first_name=f'Test{i+1}',
                        last_name='User'
                    )
                    # Set varying last login dates
                    days_ago = random.randint(0, 30)
                    user.last_login = timezone.now() - timedelta(days=days_ago)
                    user.save()

    def generate_user_activities(self, days):
        """Generate sample user activities"""
        users = list(User.objects.all())
        activity_types = ['login', 'ai_chat', 'appointment', 'resource_view', 'forum_post']
        
        for day in range(days):
            date = timezone.now() - timedelta(days=day)
            # Generate 10-50 activities per day
            activities_per_day = random.randint(10, 50)
            
            for _ in range(activities_per_day):
                UserActivity.objects.create(
                    user=random.choice(users) if random.random() > 0.1 else None,  # 10% anonymous
                    activity_type=random.choice(activity_types),
                    timestamp=date - timedelta(
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    ),
                    details={
                        'session_duration': random.randint(5, 120),
                        'source': random.choice(['web', 'mobile', 'api'])
                    }
                )

    def generate_mental_health_metrics(self, days):
        """Generate daily mental health metrics"""
        for day in range(days):
            date = (timezone.now() - timedelta(days=day)).date()
            
            # Don't create if already exists
            if not MentalHealthMetric.objects.filter(date=date).exists():
                MentalHealthMetric.objects.create(
                    date=date,
                    total_users=User.objects.count(),
                    active_sessions=random.randint(20, 100),
                    appointments_booked=random.randint(5, 25),
                    resources_accessed=random.randint(30, 150),
                    forum_posts=random.randint(10, 50),
                    crisis_indicators=random.randint(0, 5),
                )

    def generate_alerts(self):
        """Generate sample alerts"""
        alert_types = ['crisis', 'high_usage', 'system', 'counselor_overload', 'regional_spike']
        severities = ['low', 'medium', 'high', 'critical']
        
        # Create some resolved and unresolved alerts
        for _ in range(15):
            alert_type = random.choice(alert_types)
            severity = random.choice(severities)
            
            alert = Alert.objects.create(
                alert_type=alert_type,
                title=f"{alert_type.replace('_', ' ').title()} Alert",
                message=f"Sample alert message for {alert_type} with {severity} severity",
                severity=severity,
                is_resolved=random.choice([True, False]),
                created_at=timezone.now() - timedelta(
                    days=random.randint(0, 7),
                    hours=random.randint(0, 23)
                )
            )
            
            if alert.is_resolved:
                alert.resolved_at = alert.created_at + timedelta(
                    hours=random.randint(1, 24)
                )
                alert.save()

    def generate_real_time_metrics(self):
        """Generate real-time metrics"""
        metric_types = [
            'active_users',
            'ai_sessions',
            'appointments_today',
            'crisis_interventions',
            'resource_downloads',
            'peer_support_posts',
            'counselor_availability'
        ]
        
        for metric_type in metric_types:
            for hour in range(24):  # Generate hourly data for today
                timestamp = timezone.now().replace(hour=hour, minute=0, second=0, microsecond=0)
                
                if timestamp <= timezone.now():  # Only past and current hour
                    value = self.get_realistic_metric_value(metric_type, hour)
                    
                    RealTimeMetric.objects.create(
                        metric_type=metric_type,
                        value=value,
                        timestamp=timestamp,
                        metadata={
                            'source': 'generated',
                            'hour_of_day': hour
                        }
                    )

    def get_realistic_metric_value(self, metric_type, hour):
        """Generate realistic values based on metric type and time of day"""
        # Peak hours: 10-12, 14-16, 19-21
        peak_multiplier = 1.0
        if hour in [10, 11, 14, 15, 16, 19, 20, 21]:
            peak_multiplier = 1.5
        elif hour in [0, 1, 2, 3, 4, 5, 6]:
            peak_multiplier = 0.3
        
        base_values = {
            'active_users': 25,
            'ai_sessions': 15,
            'appointments_today': 3,
            'crisis_interventions': 1,
            'resource_downloads': 20,
            'peer_support_posts': 8,
            'counselor_availability': 85  # percentage
        }
        
        base_value = base_values.get(metric_type, 10)
        variance = random.uniform(0.7, 1.3)  # ±30% variance
        
        return max(0, int(base_value * peak_multiplier * variance))