from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, Institution, Region


class Command(BaseCommand):
    help = 'Create UserProfile for existing users who do not have one'

    def handle(self, *args, **options):
        # Get all users without UserProfile
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        
        if not users_without_profile.exists():
            self.stdout.write(self.style.SUCCESS('All users already have profiles'))
            return
        
        # Get or create default institution
        default_institution = Institution.objects.first()
        if not default_institution:
            # Create default region first
            default_region, created = Region.objects.get_or_create(
                name='Default Region',
                defaults={'code': 'DEF'}
            )
            
            default_institution = Institution.objects.create(
                name='Default Institution',
                code='DEFAULT',
                institution_type='other',
                region=default_region,
                address='Default Address',
                contact_email='admin@default.edu',
                contact_phone='+91-0000000000'
            )
            
            self.stdout.write(f'Created default institution: {default_institution.name}')
        
        created_count = 0
        for user in users_without_profile:
            try:
                UserProfile.objects.create(
                    user=user,
                    institution=default_institution
                )
                created_count += 1
                self.stdout.write(f'Created profile for user: {user.username}')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to create profile for {user.username}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} user profiles'
            )
        )