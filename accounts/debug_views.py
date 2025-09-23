from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def auth_debug_view(request):
    """Debug view to check authentication status"""
    context = {
        'user_authenticated': request.user.is_authenticated,
        'user_username': getattr(request.user, 'username', 'Anonymous'),
        'user_is_staff': getattr(request.user, 'is_staff', False),
        'user_is_superuser': getattr(request.user, 'is_superuser', False),
        'session_key': request.session.session_key,
        'session_data': dict(request.session),
    }
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse(context)
    
    return render(request, 'debug/auth_status.html', context)


@login_required
def protected_view(request):
    """Test protected view"""
    return render(request, 'debug/protected.html', {
        'user': request.user
    })