from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Institution, Region


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile when a new User is created
    """
    if created:
        try:
            # Get or create default institution
            default_institution = Institution.objects.first()
            if not default_institution:
                # Create default region first
                default_region, region_created = Region.objects.get_or_create(
                    name='Default Region',
                    defaults={'code': 'DEF'}
                )
                # Create default institution
                default_institution, inst_created = Institution.objects.get_or_create(
                    name='Default Institution',
                    defaults={
                        'code': 'DEFAULT',
                        'institution_type': 'other',
                        'region': default_region,
                        'address': 'Default Address',
                        'contact_email': 'admin@default.edu',
                        'contact_phone': '+91-0000000000'
                    }
                )
            
            # Use get_or_create to avoid duplicates
            user_profile, profile_created = UserProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'institution': default_institution
                }
            )
            
            if profile_created:
                print(f'Created UserProfile for user {instance.username}')
            else:
                print(f'UserProfile already exists for user {instance.username}')
                
        except Exception as e:
            # Log error but don't prevent user creation
            print(f'Failed to create UserProfile for user {instance.username}: {e}')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """
    Save the UserProfile when the User is saved (but not on creation to avoid conflicts)
    """
    if not created and hasattr(instance, 'userprofile'):
        try:
            instance.userprofile.save()
        except Exception as e:
            print(f'Failed to save UserProfile for user {instance.username}: {e}')
