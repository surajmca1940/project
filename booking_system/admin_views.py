"""
Custom admin views for the booking system dashboard
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib import messages
from datetime import datetime, timedelta
import json

from .models import Counselor, Appointment, AvailableSlot
from django.contrib.auth.models import User


@staff_member_required
@login_required
def booking_dashboard(request):
    """
    Enhanced booking system dashboard with statistics and widgets
    """
    today = timezone.now().date()
    current_week_start = today - timedelta(days=today.weekday())
    current_week_end = current_week_start + timedelta(days=6)
    
    # Basic statistics
    stats = {
        'total_counselors': Counselor.objects.count(),
        'active_counselors': Counselor.objects.filter(is_available=True).count(),
        'total_appointments': Appointment.objects.count(),
        'appointments_today': Appointment.objects.filter(date=today).count(),
        'appointments_this_week': Appointment.objects.filter(
            date__range=[current_week_start, current_week_end]
        ).count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'confirmed_appointments': Appointment.objects.filter(status='confirmed').count(),
        'cancelled_appointments': Appointment.objects.filter(status='cancelled').count(),
        'completed_appointments': Appointment.objects.filter(status='completed').count(),
    }
    
    # Upcoming appointments in next 24 hours
    tomorrow = today + timedelta(days=1)
    upcoming_appointments = Appointment.objects.filter(
        date__range=[today, tomorrow],
        status__in=['confirmed', 'pending']
    ).select_related('student', 'counselor__user').order_by('date', 'time')[:10]
    
    # Recent appointments
    recent_appointments = Appointment.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).select_related('student', 'counselor__user').order_by('-created_at')[:10]
    
    # Counselor performance data
    counselor_stats = Counselor.objects.annotate(
        total_appointments=Count('appointment'),
        pending_appointments=Count('appointment', filter=Q(appointment__status='pending')),
        confirmed_appointments=Count('appointment', filter=Q(appointment__status='confirmed')),
        completed_appointments=Count('appointment', filter=Q(appointment__status='completed')),
        cancelled_appointments=Count('appointment', filter=Q(appointment__status='cancelled')),
    ).filter(total_appointments__gt=0).order_by('-total_appointments')[:10]
    
    # Available slots today and tomorrow
    available_slots_today = AvailableSlot.objects.filter(
        date=today, is_booked=False
    ).select_related('counselor__user').count()
    
    available_slots_tomorrow = AvailableSlot.objects.filter(
        date=tomorrow, is_booked=False
    ).select_related('counselor__user').count()
    
    # Weekly appointment trends
    week_dates = [(current_week_start + timedelta(days=i)) for i in range(7)]
    weekly_appointments = []
    
    for date in week_dates:
        day_appointments = Appointment.objects.filter(date=date).count()
        weekly_appointments.append({
            'date': date.strftime('%a %m/%d'),
            'count': day_appointments
        })
    
    # Status distribution for charts
    status_distribution = [
        {'status': 'Confirmed', 'count': stats['confirmed_appointments'], 'color': '#5cb85c'},
        {'status': 'Pending', 'count': stats['pending_appointments'], 'color': '#f0ad4e'},
        {'status': 'Cancelled', 'count': stats['cancelled_appointments'], 'color': '#d9534f'},
        {'status': 'Completed', 'count': stats['completed_appointments'], 'color': '#5bc0de'},
    ]
    
    # Alerts and notifications
    alerts = []
    
    # Check for appointments needing attention
    if stats['pending_appointments'] > 5:
        alerts.append({
            'type': 'warning',
            'icon': '⚠️',
            'title': 'High Pending Appointments',
            'message': f'{stats["pending_appointments"]} appointments are still pending confirmation.',
            'action_url': '/admin/booking_system/appointment/?status_filter=pending'
        })
    
    if available_slots_today < 5:
        alerts.append({
            'type': 'danger',
            'icon': '🚨',
            'title': 'Low Available Slots Today',
            'message': f'Only {available_slots_today} slots available today. Consider adding more.',
            'action_url': '/admin/booking_system/availableslot/?date__exact=' + today.strftime('%Y-%m-%d')
        })
    
    if stats['appointments_today'] > 15:
        alerts.append({
            'type': 'info',
            'icon': '📈',
            'title': 'High Activity Today',
            'message': f'{stats["appointments_today"]} appointments scheduled today.',
            'action_url': '/admin/booking_system/appointment/?status_filter=today'
        })
    
    context = {
        'title': 'Booking System Dashboard',
        'stats': stats,
        'upcoming_appointments': upcoming_appointments,
        'recent_appointments': recent_appointments,
        'counselor_stats': counselor_stats,
        'available_slots_today': available_slots_today,
        'available_slots_tomorrow': available_slots_tomorrow,
        'weekly_appointments': json.dumps(weekly_appointments),
        'status_distribution': json.dumps(status_distribution),
        'alerts': alerts,
        'today': today,
        'current_week_start': current_week_start,
        'current_week_end': current_week_end,
    }
    
    return render(request, 'admin/booking_system/dashboard.html', context)


@staff_member_required
@login_required
def get_dashboard_stats(request):
    """
    AJAX endpoint for real-time dashboard statistics
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    today = timezone.now().date()
    
    stats = {
        'appointments_today': Appointment.objects.filter(date=today).count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'confirmed_appointments': Appointment.objects.filter(status='confirmed').count(),
        'available_counselors': Counselor.objects.filter(is_available=True).count(),
        'available_slots_today': AvailableSlot.objects.filter(
            date=today, is_booked=False
        ).count(),
        'last_updated': timezone.now().strftime('%H:%M:%S')
    }
    
    return JsonResponse(stats)


@staff_member_required
@login_required
def quick_appointment_action(request):
    """
    Handle quick actions for appointments (confirm, cancel, complete)
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')
        
        if not appointment_id or not action:
            return JsonResponse({'error': 'Missing parameters'}, status=400)
        
        appointment = Appointment.objects.get(id=appointment_id)
        
        if action == 'confirm' and appointment.status == 'pending':
            appointment.status = 'confirmed'
            appointment.save()
            message = f'Appointment with {appointment.counselor} confirmed successfully.'
            messages.success(request, message)
            
        elif action == 'cancel' and appointment.status in ['pending', 'confirmed']:
            appointment.status = 'cancelled'
            appointment.save()
            message = f'Appointment with {appointment.counselor} cancelled successfully.'
            messages.warning(request, message)
            
        elif action == 'complete' and appointment.status == 'confirmed':
            appointment.status = 'completed'
            appointment.save()
            message = f'Appointment with {appointment.counselor} marked as completed.'
            messages.success(request, message)
            
        else:
            return JsonResponse({'error': 'Invalid action for current status'}, status=400)
        
        return JsonResponse({
            'success': True,
            'message': message,
            'new_status': appointment.status
        })
        
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@login_required
def counselor_performance(request, counselor_id=None):
    """
    Detailed performance view for counselors
    """
    if counselor_id:
        try:
            counselor = Counselor.objects.get(id=counselor_id)
            
            # Last 30 days performance
            thirty_days_ago = timezone.now().date() - timedelta(days=30)
            
            performance_data = {
                'counselor': counselor,
                'total_appointments': counselor.appointment_set.count(),
                'appointments_last_30_days': counselor.appointment_set.filter(
                    date__gte=thirty_days_ago
                ).count(),
                'completed_appointments': counselor.appointment_set.filter(
                    status='completed'
                ).count(),
                'cancelled_appointments': counselor.appointment_set.filter(
                    status='cancelled'
                ).count(),
                'pending_appointments': counselor.appointment_set.filter(
                    status='pending'
                ).count(),
                'confirmed_appointments': counselor.appointment_set.filter(
                    status='confirmed'
                ).count(),
            }
            
            # Calculate completion rate
            total_finished = performance_data['completed_appointments'] + performance_data['cancelled_appointments']
            completion_rate = (performance_data['completed_appointments'] / max(total_finished, 1)) * 100
            performance_data['completion_rate'] = round(completion_rate, 1)
            
            # Recent appointments
            recent_appointments = counselor.appointment_set.select_related(
                'student'
            ).order_by('-date', '-time')[:20]
            
            performance_data['recent_appointments'] = recent_appointments
            
            return render(request, 'admin/booking_system/counselor_performance.html', performance_data)
            
        except Counselor.DoesNotExist:
            messages.error(request, 'Counselor not found.')
            return redirect('/admin/booking_system/counselor/')
    
    # Show all counselors performance overview
    counselors_performance = Counselor.objects.annotate(
        total_appointments=Count('appointment'),
        completed_appointments=Count('appointment', filter=Q(appointment__status='completed')),
        cancelled_appointments=Count('appointment', filter=Q(appointment__status='cancelled')),
        pending_appointments=Count('appointment', filter=Q(appointment__status='pending')),
    ).order_by('-total_appointments')
    
    return render(request, 'admin/booking_system/counselors_performance.html', {
        'counselors_performance': counselors_performance
    })


@staff_member_required
@login_required
def system_health_check(request):
    """
    System health check for the booking system
    """
    health_data = {
        'timestamp': timezone.now(),
        'status': 'healthy',
        'checks': []
    }
    
    try:
        # Check database connectivity
        total_appointments = Appointment.objects.count()
        health_data['checks'].append({
            'name': 'Database Connectivity',
            'status': 'healthy',
            'message': f'Connected successfully. {total_appointments} appointments in database.',
            'icon': '✅'
        })
        
        # Check for counselor availability
        available_counselors = Counselor.objects.filter(is_available=True).count()
        if available_counselors < 3:
            health_data['checks'].append({
                'name': 'Counselor Availability',
                'status': 'warning',
                'message': f'Only {available_counselors} counselors available. Consider adding more.',
                'icon': '⚠️'
            })
            health_data['status'] = 'warning'
        else:
            health_data['checks'].append({
                'name': 'Counselor Availability',
                'status': 'healthy',
                'message': f'{available_counselors} counselors are available.',
                'icon': '✅'
            })
        
        # Check for pending appointments
        pending_count = Appointment.objects.filter(status='pending').count()
        if pending_count > 10:
            health_data['checks'].append({
                'name': 'Pending Appointments',
                'status': 'warning',
                'message': f'{pending_count} appointments are pending confirmation.',
                'icon': '⚠️'
            })
            health_data['status'] = 'warning'
        else:
            health_data['checks'].append({
                'name': 'Pending Appointments',
                'status': 'healthy',
                'message': f'{pending_count} pending appointments (within normal range).',
                'icon': '✅'
            })
        
        # Check available slots for next 7 days
        next_week = timezone.now().date() + timedelta(days=7)
        available_slots = AvailableSlot.objects.filter(
            date__lte=next_week,
            is_booked=False
        ).count()
        
        if available_slots < 20:
            health_data['checks'].append({
                'name': 'Available Slots',
                'status': 'warning',
                'message': f'Only {available_slots} slots available in the next 7 days.',
                'icon': '⚠️'
            })
            health_data['status'] = 'warning'
        else:
            health_data['checks'].append({
                'name': 'Available Slots',
                'status': 'healthy',
                'message': f'{available_slots} slots available in the next 7 days.',
                'icon': '✅'
            })
        
    except Exception as e:
        health_data['status'] = 'critical'
        health_data['checks'].append({
            'name': 'System Error',
            'status': 'critical',
            'message': f'System error: {str(e)}',
            'icon': '❌'
        })
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse(health_data)
    
    return render(request, 'admin/booking_system/system_health.html', health_data)