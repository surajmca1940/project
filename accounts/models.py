from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Region(models.Model):
    """Model to store regional/cultural information"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=100, default='India')
    primary_language = models.CharField(max_length=50, default='English')
    cultural_context = models.JSONField(default=dict, help_text="Store cultural preferences, customs, festivals, etc.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        ordering = ['name']


class Institution(models.Model):
    """Model to store institution-specific configurations"""
    INSTITUTION_TYPES = [
        ('college', 'College'),
        ('university', 'University'),
        ('technical', 'Technical Institute'),
        ('medical', 'Medical College'),
        ('arts', 'Arts College'),
        ('commerce', 'Commerce College'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(r'^[A-Z0-9]+$', 'Code must contain only uppercase letters and numbers')
    ])
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPES)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    
    # Customization fields
    logo = models.ImageField(upload_to='institution_logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    secondary_color = models.CharField(max_length=7, default='#6c757d', help_text="Hex color code")
    custom_css = models.TextField(blank=True, help_text="Additional CSS for customization")
    
    # Feature toggles
    enable_ai_support = models.BooleanField(default=True)
    enable_peer_support = models.BooleanField(default=True)
    enable_offline_booking = models.BooleanField(default=True)
    enable_anonymous_mode = models.BooleanField(default=True)
    
    # Configuration
    working_hours_start = models.TimeField(default='09:00')
    working_hours_end = models.TimeField(default='17:00')
    timezone = models.CharField(max_length=50, default='UTC')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        ordering = ['name']


class LanguageSupport(models.Model):
    """Model to manage supported languages for different regions"""
    language_name = models.CharField(max_length=100)
    language_code = models.CharField(max_length=5, help_text="ISO language code (e.g., 'hi' for Hindi)")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='supported_languages')
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Translation resources
    ui_translations = models.JSONField(default=dict, help_text="UI text translations")
    content_translations = models.JSONField(default=dict, help_text="Content translations")
    
    def __str__(self):
        return f"{self.language_name} for {self.region.name}"
    
    class Meta:
        unique_together = ['language_code', 'region']
        ordering = ['language_name']


class UserProfile(models.Model):
    """Extended user profile with regional and institutional context"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    preferred_language = models.ForeignKey(LanguageSupport, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Privacy settings
    is_anonymous = models.BooleanField(default=True)
    show_in_peer_support = models.BooleanField(default=False)
    
    # Cultural preferences
    cultural_preferences = models.JSONField(default=dict, help_text="User's cultural preferences and sensitivities")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.institution.code}"
    
    class Meta:
        ordering = ['-created_at']


class Counselor(models.Model):
    """Counselor linked to an institution for offline support mapping"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='counselors')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='counselor_profile', null=True, blank=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    room_location = models.CharField(max_length=200, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    languages = models.ManyToManyField(LanguageSupport, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.institution.code}"

    class Meta:
        ordering = ['full_name']


class CounselorAvailability(models.Model):
    """Weekly availability slots for counselors"""
    WEEKDAYS = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ]
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='availabilities')
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    is_online = models.BooleanField(default=False)

    class Meta:
        unique_together = ['counselor', 'weekday', 'start_time', 'end_time']
        ordering = ['counselor', 'weekday', 'start_time']

    def __str__(self):
        return f"{self.counselor.full_name} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"


class OfflineSupportTicket(models.Model):
    """Links students/users to counselors for offline support, with status tracking"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_offline_tickets')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='offline_tickets')
    counselor = models.ForeignKey(Counselor, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    scheduled_for = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} ({self.status})"
