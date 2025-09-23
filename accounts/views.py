from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import UserProfile, Institution

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # Create UserProfile with default institution
            try:
                # Try to get the first available institution or create a default one
                default_institution = Institution.objects.first()
                if not default_institution:
                    # Create a default institution if none exists
                    from .models import Region
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
                
                # Create the user profile
                UserProfile.objects.create(
                    user=user,
                    institution=default_institution
                )
                
            except Exception as e:
                # If profile creation fails, log the error but don't prevent registration
                messages.warning(request, 'User created successfully, but profile setup incomplete. Please contact admin.')
                print(f'UserProfile creation failed: {e}')
            
            messages.success(request, f'Account created for {username}! You can now log in.')
            
            # Automatically log in the user after registration
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def logout_success_view(request):
    """Simple logout success page"""
    return render(request, 'registration/logged_out.html')
