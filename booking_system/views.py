from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Counselor, Appointment, AvailableSlot
import json
from datetime import datetime, timedelta

def appointment_list(request):
    """Enhanced appointment booking with all features"""
    counselors = Counselor.objects.filter(is_available=True)
    
    # Generate sample available slots for demo
    available_slots = []
    today = timezone.now().date()
    
    for i in range(7):  # Next 7 days
        date = today + timedelta(days=i)
        # Morning slots (9 AM - 12 PM)
        for hour in range(9, 12):
            available_slots.append({
                'date': date,
                'time': f"{hour:02d}:00",
                'period': 'morning',
                'status': 'available' if hour != 11 else 'limited'
            })
        # Afternoon slots (2 PM - 5 PM)
        for hour in range(14, 17):
            available_slots.append({
                'date': date,
                'time': f"{hour:02d}:00",
                'period': 'afternoon',
                'status': 'available' if hour != 15 else 'booked'
            })
        # Evening slots (6 PM - 8 PM)
        for hour in range(18, 20):
            available_slots.append({
                'date': date,
                'time': f"{hour:02d}:00",
                'period': 'evening',
                'status': 'available'
            })
    
    context = {
        'counselors': counselors,
        'available_slots': available_slots,
        'today': today
    }
    return render(request, 'booking_system/appointments_enhanced.html', context)

def book_appointment(request):
    """Book an appointment form"""
    return render(request, 'booking_system/book.html')

def counselor_list(request):
    """List of available counselors"""
    counselors = Counselor.objects.filter(is_available=True)
    return render(request, 'booking_system/counselors.html', {'counselors': counselors})

@login_required
def my_appointments(request):
    """User's booked appointments with reschedule/cancel options"""
    appointments = Appointment.objects.filter(
        student=request.user
    ).order_by('-created_at')
    
    context = {
        'appointments': appointments,
        'today': timezone.now().date()
    }
    return render(request, 'booking_system/my_appointments.html', context)

@login_required
def reschedule_appointment(request, appointment_id):
    """Reschedule an existing appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, student=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            new_time = datetime.strptime(data['time'], '%H:%M').time()
            
            # Update appointment
            appointment.date = new_date
            appointment.time = new_time
            appointment.status = 'pending'  # Reset to pending for approval
            appointment.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Appointment rescheduled successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error rescheduling appointment: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def cancel_appointment(request, appointment_id):
    """Cancel an existing appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, student=request.user)
    
    if request.method == 'POST':
        try:
            appointment.status = 'cancelled'
            appointment.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Appointment cancelled successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error cancelling appointment: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required 
def confirm_booking(request):
    """Confirm and create a new appointment booking"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get counselor
            counselor = get_object_or_404(Counselor, id=data['counselor_id'])
            
            # Create appointment
            appointment = Appointment.objects.create(
                student=request.user,
                counselor=counselor,
                date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                time=datetime.strptime(data['time'], '%H:%M').time(),
                notes=data.get('notes', ''),
                status='confirmed'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Appointment booked successfully!',
                'appointment_id': appointment.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error booking appointment: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_availability(request):
    """Get available slots for a specific date and filter"""
    date = request.GET.get('date')
    period_filter = request.GET.get('period', 'all')  # morning, afternoon, evening, all
    counselor_id = request.GET.get('counselor_id')
    
    # Mock availability data for demo
    slots = {
        'morning': [
            {'time': '09:00', 'status': 'available'},
            {'time': '10:00', 'status': 'available'},
            {'time': '11:00', 'status': 'limited'},
        ],
        'afternoon': [
            {'time': '14:00', 'status': 'available'},
            {'time': '15:00', 'status': 'booked'},
            {'time': '16:00', 'status': 'available'},
        ],
        'evening': [
            {'time': '18:00', 'status': 'available'},
            {'time': '19:00', 'status': 'available'},
        ]
    }
    
    if period_filter != 'all':
        filtered_slots = {period_filter: slots.get(period_filter, [])}
    else:
        filtered_slots = slots
    
    return JsonResponse({'slots': filtered_slots})
