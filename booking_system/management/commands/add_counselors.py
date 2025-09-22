from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking_system.models import Counselor
from django.db import transaction


class Command(BaseCommand):
    help = 'Add sample counselors to the booking system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing counselors before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing counselors...')
            Counselor.objects.all().delete()
            # Also delete the associated users that were created for counselors
            User.objects.filter(username__startswith='counselor_').delete()

        sample_counselors = [
            {
                'username': 'counselor_sarah',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah.johnson@clinic.com',
                'specialization': 'Clinical Psychologist',
                'bio': 'Dr. Sarah Johnson has over 8 years of experience in clinical psychology, specializing in anxiety disorders, depression, and PTSD treatment. She uses evidence-based therapies including CBT and EMDR.',
                'languages': 'English, Hindi, Spanish',
                'is_available': True
            },
            {
                'username': 'counselor_michael',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'email': 'michael.chen@clinic.com',
                'specialization': 'Licensed Therapist',
                'bio': 'Dr. Michael Chen is a licensed therapist with 6 years of experience in stress management, relationship counseling, and mindfulness-based therapy. He specializes in helping young adults navigate life transitions.',
                'languages': 'English, Mandarin',
                'is_available': True
            },
            {
                'username': 'counselor_lisa',
                'first_name': 'Lisa',
                'last_name': 'Rodriguez',
                'email': 'lisa.rodriguez@clinic.com',
                'specialization': 'Student Support Specialist',
                'bio': 'Dr. Lisa Rodriguez has 10 years of experience working with students in academic settings. She specializes in academic stress, life transitions, and student mental health support.',
                'languages': 'English, Spanish, Portuguese',
                'is_available': True
            },
            {
                'username': 'counselor_james',
                'first_name': 'James',
                'last_name': 'Wilson',
                'email': 'james.wilson@clinic.com',
                'specialization': 'Marriage & Family Therapist',
                'bio': 'Dr. James Wilson is a licensed marriage and family therapist with 12 years of experience. He specializes in relationship counseling, family dynamics, and communication skills.',
                'languages': 'English, French',
                'is_available': True
            },
            {
                'username': 'counselor_priya',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'email': 'priya.sharma@clinic.com',
                'specialization': 'Trauma Specialist',
                'bio': 'Dr. Priya Sharma is a trauma specialist with 9 years of experience in treating PTSD, trauma recovery, and crisis intervention. She is trained in EMDR and trauma-informed care.',
                'languages': 'English, Hindi, Bengali',
                'is_available': True
            },
            {
                'username': 'counselor_david',
                'first_name': 'David',
                'last_name': 'Thompson',
                'email': 'david.thompson@clinic.com',
                'specialization': 'Addiction Counselor',
                'bio': 'Dr. David Thompson has 7 years of experience in addiction counseling and substance abuse treatment. He specializes in recovery support, relapse prevention, and behavioral therapy.',
                'languages': 'English',
                'is_available': True
            }
        ]

        created_count = 0
        
        with transaction.atomic():
            for counselor_data in sample_counselors:
                try:
                    # Create user first
                    user, user_created = User.objects.get_or_create(
                        username=counselor_data['username'],
                        defaults={
                            'first_name': counselor_data['first_name'],
                            'last_name': counselor_data['last_name'],
                            'email': counselor_data['email'],
                            'is_staff': True,  # Give them staff access
                        }
                    )
                    
                    if user_created:
                        user.set_password('counselor123')  # Set a default password
                        user.save()
                    
                    # Create or update counselor
                    counselor, counselor_created = Counselor.objects.get_or_create(
                        user=user,
                        defaults={
                            'specialization': counselor_data['specialization'],
                            'bio': counselor_data['bio'],
                            'languages': counselor_data['languages'],
                            'is_available': counselor_data['is_available']
                        }
                    )
                    
                    if counselor_created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Created counselor: Dr. {counselor_data["first_name"]} {counselor_data["last_name"]}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'• Counselor already exists: Dr. {counselor_data["first_name"]} {counselor_data["last_name"]}'
                            )
                        )
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'✗ Error creating counselor {counselor_data["first_name"]} {counselor_data["last_name"]}: {e}'
                        )
                    )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'🎉 Successfully created {created_count} new counselors!'
            )
        )
        self.stdout.write('')
        self.stdout.write('📋 Summary:')
        self.stdout.write(f'   Total counselors in system: {Counselor.objects.count()}')
        self.stdout.write(f'   Available counselors: {Counselor.objects.filter(is_available=True).count()}')
        self.stdout.write('')
        self.stdout.write('💡 Tips:')
        self.stdout.write('   • Visit /admin/ to manage counselors')
        self.stdout.write('   • Visit /booking/ to see them in the booking system')
        self.stdout.write('   • Default password for counselor accounts: counselor123')