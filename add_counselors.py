#!/usr/bin/env python
"""
Script to add sample counselors to the booking system
"""
import os
import sys
import django
from datetime import datetime, timedelta, time

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_platform.settings')
django.setup()

from django.contrib.auth.models import User
from booking_system.models import Counselor, AvailableSlot

def create_admin_user():
    """Create admin user if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("✅ Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        return admin_user
    else:
        print("ℹ️  Admin user already exists")
        return User.objects.get(username='admin')

def create_sample_counselors():
    """Create sample counselors with different specializations"""
    
    counselors_data = [
        {
            'username': 'dr_sarah',
            'email': 'sarah.johnson@college.edu',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'specialization': 'Anxiety and Stress Management',
            'bio': 'Dr. Sarah Johnson has over 8 years of experience in treating anxiety disorders and stress-related issues. She specializes in cognitive behavioral therapy and mindfulness techniques.',
            'languages': 'English, Hindi'
        },
        {
            'username': 'dr_michael',
            'email': 'michael.chen@college.edu',
            'first_name': 'Michael',
            'last_name': 'Chen',
            'specialization': 'Depression and Mood Disorders',
            'bio': 'Dr. Michael Chen is a licensed clinical psychologist with expertise in treating depression, bipolar disorder, and other mood-related conditions. He uses evidence-based approaches including CBT and DBT.',
            'languages': 'English, Mandarin, Tamil'
        },
        {
            'username': 'dr_priya',
            'email': 'priya.sharma@college.edu',
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'specialization': 'Academic Stress and Study Issues',
            'bio': 'Dr. Priya Sharma specializes in helping students overcome academic challenges, test anxiety, and study-related stress. She has worked extensively with college students for over 6 years.',
            'languages': 'Hindi, English, Gujarati'
        },
        {
            'username': 'dr_james',
            'email': 'james.wilson@college.edu',
            'first_name': 'James',
            'last_name': 'Wilson',
            'specialization': 'Relationship and Social Issues',
            'bio': 'Dr. James Wilson focuses on interpersonal relationships, social anxiety, and communication skills. He helps students build healthy relationships and overcome social challenges.',
            'languages': 'English'
        },
        {
            'username': 'dr_anita',
            'email': 'anita.reddy@college.edu',
            'first_name': 'Anita',
            'last_name': 'Reddy',
            'specialization': 'Sleep Disorders and Wellness',
            'bio': 'Dr. Anita Reddy specializes in sleep disorders, wellness coaching, and lifestyle management. She helps students develop healthy sleep patterns and overall wellness strategies.',
            'languages': 'English, Telugu, Kannada'
        }
    ]
    
    created_counselors = []
    
    for counselor_data in counselors_data:
        # Create user if doesn't exist
        user, created = User.objects.get_or_create(
            username=counselor_data['username'],
            defaults={
                'email': counselor_data['email'],
                'first_name': counselor_data['first_name'],
                'last_name': counselor_data['last_name'],
                'is_staff': True  # Allow them to access admin if needed
            }
        )
        
        # Create counselor profile if doesn't exist
        counselor, created = Counselor.objects.get_or_create(
            user=user,
            defaults={
                'specialization': counselor_data['specialization'],
                'bio': counselor_data['bio'],
                'languages': counselor_data['languages'],
                'is_available': True
            }
        )
        
        if created:
            print(f"✅ Created counselor: Dr. {user.get_full_name()} - {counselor.specialization}")
            created_counselors.append(counselor)
        else:
            print(f"ℹ️  Counselor already exists: Dr. {user.get_full_name()}")
    
    return created_counselors

def create_available_slots(counselors):
    """Create available time slots for counselors"""
    
    # Define time slots (9 AM to 5 PM, 1-hour slots)
    time_slots = [
        (time(9, 0), time(10, 0)),
        (time(10, 0), time(11, 0)),
        (time(11, 0), time(12, 0)),
        (time(14, 0), time(15, 0)),  # 2 PM to 3 PM (after lunch)
        (time(15, 0), time(16, 0)),
        (time(16, 0), time(17, 0)),
    ]
    
    # Create slots for next 7 days
    today = datetime.now().date()
    
    for counselor in counselors:
        slots_created = 0
        for day_offset in range(1, 8):  # Next 7 days
            slot_date = today + timedelta(days=day_offset)
            
            # Skip weekends for some variety
            if slot_date.weekday() < 5:  # Monday to Friday
                for start_time, end_time in time_slots:
                    slot, created = AvailableSlot.objects.get_or_create(
                        counselor=counselor,
                        date=slot_date,
                        start_time=start_time,
                        defaults={
                            'end_time': end_time,
                            'is_booked': False
                        }
                    )
                    if created:
                        slots_created += 1
        
        if slots_created > 0:
            print(f"✅ Created {slots_created} available slots for Dr. {counselor.user.get_full_name()}")

def main():
    print("🏥 Setting up counselors for IndAid - Mental Health Support Platform")
    print("="*70)
    
    # Create admin user
    admin_user = create_admin_user()
    
    print("\n👩‍⚕️ Creating sample counselors...")
    counselors = create_sample_counselors()
    
    print("\n📅 Creating available time slots...")
    all_counselors = list(Counselor.objects.all())
    create_available_slots(all_counselors)
    
    print("\n🎉 Setup completed successfully!")
    print(f"   Total counselors: {Counselor.objects.count()}")
    print(f"   Total available slots: {AvailableSlot.objects.count()}")
    print("\n🌐 You can now:")
    print("   1. Visit http://127.0.0.1:8000/admin/ to manage counselors")
    print("   2. Visit http://127.0.0.1:8000/booking/ to book appointments")
    print("   3. Login credentials - Username: admin, Password: admin123")

if __name__ == '__main__':
    main()
