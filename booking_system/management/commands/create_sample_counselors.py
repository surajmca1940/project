"""
Management command to create sample counselors for testing
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking_system.models import Counselor, AvailableSlot
from datetime import date, time, timedelta
import random

class Command(BaseCommand):
    help = 'Create sample counselors with basic information for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of sample counselors to create (default: 5)'
        )
        parser.add_argument(
            '--with-slots',
            action='store_true',
            help='Also create sample available slots for each counselor'
        )

    def handle(self, *args, **options):
        count = options['count']
        create_slots = options['with_slots']
        
        # Sample counselor data
        sample_counselors = [
            {
                'first_name': 'Sarah', 'last_name': 'Johnson',
                'email': 'sarah.johnson@mentalhealth.com',
                'specialization': 'Anxiety and Depression',
                'languages': 'English, Spanish'
            },
            {
                'first_name': 'Dr. Rajesh', 'last_name': 'Kumar',
                'email': 'rajesh.kumar@mentalhealth.com', 
                'specialization': 'Stress Management, Academic Pressure',
                'languages': 'English, Hindi, Tamil'
            },
            {
                'first_name': 'Dr. Priya', 'last_name': 'Sharma',
                'email': 'priya.sharma@mentalhealth.com',
                'specialization': 'Relationship Issues, Family Counseling',
                'languages': 'English, Hindi, Marathi'
            },
            {
                'first_name': 'Michael', 'last_name': 'Chen',
                'email': 'michael.chen@mentalhealth.com',
                'specialization': 'Career Counseling, Life Transitions',
                'languages': 'English, Mandarin'
            },
            {
                'first_name': 'Dr. Anita', 'last_name': 'Patel',
                'email': 'anita.patel@mentalhealth.com',
                'specialization': 'Trauma Therapy, PTSD',
                'languages': 'English, Hindi, Gujarati'
            },
            {
                'first_name': 'James', 'last_name': 'Wilson',
                'email': 'james.wilson@mentalhealth.com',
                'specialization': 'Addiction Counseling, Recovery',
                'languages': 'English'
            },
            {
                'first_name': 'Dr. Kavita', 'last_name': 'Reddy',
                'email': 'kavita.reddy@mentalhealth.com',
                'specialization': 'Adolescent Psychology, Teen Issues',
                'languages': 'English, Telugu, Hindi'
            },
            {
                'first_name': 'Robert', 'last_name': 'Brown',
                'email': 'robert.brown@mentalhealth.com',
                'specialization': 'Cognitive Behavioral Therapy',
                'languages': 'English'
            }
        ]

        created_count = 0
        
        for i in range(min(count, len(sample_counselors))):
            counselor_data = sample_counselors[i]
            
            try:
                # Create or get user
                user, user_created = User.objects.get_or_create(
                    username=f"counselor_{counselor_data['first_name'].lower()}_{counselor_data['last_name'].lower()}",
                    defaults={
                        'first_name': counselor_data['first_name'],
                        'last_name': counselor_data['last_name'],
                        'email': counselor_data['email'],
                        'is_staff': True,  # Allow access to admin
                        'password': 'pbkdf2_sha256$320000$temporary$password'  # Temporary password
                    }
                )
                
                # Create counselor profile
                counselor, counselor_created = Counselor.objects.get_or_create(
                    user=user,
                    defaults={
                        'specialization': counselor_data['specialization'],
                        'bio': f"Experienced mental health counselor specializing in {counselor_data['specialization'].lower()}. "
                               f"Committed to providing compassionate and effective therapy to help students achieve better mental wellness.",
                        'languages': counselor_data['languages'],
                        'is_available': True
                    }
                )
                
                if counselor_created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Created counselor: {counselor.user.get_full_name()} - {counselor.specialization}")
                    )
                    
                    # Create sample available slots if requested
                    if create_slots:
                        self.create_sample_slots(counselor)
                        
                else:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️  Counselor already exists: {counselor.user.get_full_name()}")
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error creating counselor {counselor_data['first_name']} {counselor_data['last_name']}: {e}")
                )
        
        # If we need more counselors than sample data, create generic ones
        if count > len(sample_counselors):
            for i in range(len(sample_counselors), count):
                try:
                    user, user_created = User.objects.get_or_create(
                        username=f"counselor_sample_{i+1}",
                        defaults={
                            'first_name': f"Counselor",
                            'last_name': f"Sample{i+1}",
                            'email': f"counselor{i+1}@mentalhealth.com",
                            'is_staff': True,
                            'password': 'pbkdf2_sha256$320000$temporary$password'
                        }
                    )
                    
                    specializations = [
                        'General Counseling', 'Stress Management', 'Academic Support',
                        'Anxiety Disorders', 'Depression Therapy', 'Mindfulness Training'
                    ]
                    
                    counselor, counselor_created = Counselor.objects.get_or_create(
                        user=user,
                        defaults={
                            'specialization': random.choice(specializations),
                            'bio': 'Professional mental health counselor dedicated to student wellness.',
                            'languages': random.choice(['English', 'English, Hindi', 'English, Spanish']),
                            'is_available': True
                        }
                    )
                    
                    if counselor_created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ Created generic counselor: {counselor.user.get_full_name()}")
                        )
                        
                        if create_slots:
                            self.create_sample_slots(counselor)
                            
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Error creating generic counselor {i+1}: {e}")
                    )
        
        # Summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"🎉 Successfully created {created_count} new counselors!"))
        self.stdout.write(f"📊 Total counselors in system: {Counselor.objects.count()}")
        
        if create_slots:
            total_slots = AvailableSlot.objects.count()
            self.stdout.write(f"⏰ Total available slots: {total_slots}")
        
        self.stdout.write("\n💡 Tips:")
        self.stdout.write("   - All counselors have temporary passwords and are marked as staff")
        self.stdout.write("   - You can edit their details in the admin panel")
        self.stdout.write("   - Use --with-slots to create sample availability schedules")
        self.stdout.write("   - Access admin at: http://localhost:8000/admin/")

    def create_sample_slots(self, counselor):
        """Create sample available slots for a counselor"""
        today = date.today()
        
        # Create slots for the next 14 days
        for day_offset in range(1, 15):
            slot_date = today + timedelta(days=day_offset)
            
            # Skip weekends for some variety
            if slot_date.weekday() >= 5 and random.choice([True, False]):
                continue
                
            # Create 2-4 slots per day
            num_slots = random.randint(2, 4)
            start_hour = 9  # 9 AM
            
            for slot in range(num_slots):
                slot_start_hour = start_hour + (slot * 2)  # 2-hour gaps
                
                if slot_start_hour >= 17:  # Don't go past 5 PM
                    break
                
                try:
                    AvailableSlot.objects.get_or_create(
                        counselor=counselor,
                        date=slot_date,
                        start_time=time(slot_start_hour, 0),
                        defaults={
                            'end_time': time(slot_start_hour + 1, 0),
                            'is_booked': False
                        }
                    )
                except Exception:
                    # Skip if slot already exists or has conflicts
                    pass