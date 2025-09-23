"""
Custom forms for booking system admin
"""

from django import forms
from django.contrib.auth.models import User
from .models import Counselor

class SimpleCounselorForm(forms.ModelForm):
    """Simplified form for creating counselors with minimal required fields"""
    
    # User creation fields
    first_name = forms.CharField(
        max_length=150,
        help_text="First name of the counselor"
    )
    last_name = forms.CharField(
        max_length=150,
        help_text="Last name of the counselor"
    )
    email = forms.EmailField(
        help_text="Email address for the counselor"
    )
    username = forms.CharField(
        max_length=150,
        required=False,
        help_text="Leave blank to auto-generate from name"
    )

    class Meta:
        model = Counselor
        fields = ['specialization', 'bio', 'languages', 'is_available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief description of the counselor (optional)'}),
            'specialization': forms.TextInput(attrs={'placeholder': 'e.g., Anxiety, Depression, Stress Management'}),
            'languages': forms.TextInput(attrs={'placeholder': 'e.g., English, Hindi, Tamil'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing counselor, populate user fields
        if self.instance and self.instance.pk and self.instance.user:
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Auto-generate username if not provided
        if not username:
            first_name = self.cleaned_data.get('first_name', '').lower()
            last_name = self.cleaned_data.get('last_name', '').lower()
            username = f"counselor_{first_name}_{last_name}".replace(' ', '_')
        
        # Check if username exists (excluding current user if editing)
        existing_user = User.objects.filter(username=username).first()
        if existing_user and (not self.instance.pk or existing_user != self.instance.user):
            raise forms.ValidationError(f"Username '{username}' already exists. Please choose a different one.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email exists (excluding current user if editing)
        existing_user = User.objects.filter(email=email).first()
        if existing_user and (not self.instance.pk or existing_user != self.instance.user):
            raise forms.ValidationError(f"Email '{email}' is already registered. Please use a different email.")
        
        return email
    
    def save(self, commit=True):
        counselor = super().save(commit=False)
        
        # Create or update user
        if counselor.user:
            # Update existing user
            user = counselor.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['username']
        else:
            # Create new user
            user = User(
                username=self.cleaned_data['username'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                is_staff=True,  # Allow admin access
            )
            # Set a temporary password
            user.set_password('temporary123')  # They can change this later
        
        if commit:
            user.save()
            counselor.user = user
            counselor.save()
            self.save_m2m()
        
        return counselor


class QuickCounselorForm(forms.Form):
    """Ultra-simple form for quick counselor creation"""
    
    full_name = forms.CharField(
        max_length=150,
        help_text="Full name of the counselor (e.g., Dr. Sarah Johnson)"
    )
    email = forms.EmailField(
        help_text="Email address"
    )
    specialization = forms.CharField(
        max_length=200,
        required=False,
        initial="General Counseling",
        help_text="Area of expertise (optional)"
    )
    languages = forms.CharField(
        max_length=200,
        required=False,
        initial="English",
        help_text="Languages spoken (optional)"
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self):
        """Create user and counselor from the form data"""
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email']
        specialization = self.cleaned_data['specialization'] or "General Counseling"
        languages = self.cleaned_data['languages'] or "English"
        
        # Parse full name
        name_parts = full_name.strip().split(' ')
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
        else:
            first_name = full_name
            last_name = ''
        
        # Generate username
        username = f"counselor_{first_name.lower()}_{last_name.lower()}".replace(' ', '_')
        
        # Ensure unique username
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1
        
        # Create user
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=True
        )
        user.set_password('temporary123')  # Temporary password
        user.save()
        
        # Create counselor
        counselor = Counselor.objects.create(
            user=user,
            specialization=specialization,
            bio=f"Professional mental health counselor specializing in {specialization.lower()}.",
            languages=languages,
            is_available=True
        )
        
        return counselor