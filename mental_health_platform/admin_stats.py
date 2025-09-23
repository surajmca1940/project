from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from accounts.models import UserProfile, Institution
from admin_dashboard.models import UserActivity, Alert
from booking_system.models import Appointment
from ai_support.models import ChatSession


@staff_member_required
def admin_stats_api(request):
    """
    Simple API endpoint to provide admin dashboard statistics
    """
    try:
        stats = {
            'users': User.objects.count(),
            'profiles': UserProfile.objects.count(),
            'institutions': Institution.objects.count(),
            'alerts': Alert.objects.filter(is_resolved=False).count(),
            'activities': UserActivity.objects.count(),
            'appointments': Appointment.objects.count(),
            'chat_sessions': ChatSession.objects.count() if 'ChatSession' in globals() else 0,
        }
        
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'users': 0,
            'profiles': 0,
            'institutions': 0,
            'alerts': 0,
            'activities': 0,
            'appointments': 0,
            'chat_sessions': 0,
        })