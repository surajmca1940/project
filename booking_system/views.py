from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def appointment_list(request):
    """List available appointment slots"""
    return render(request, 'booking_system/appointments.html')

def book_appointment(request):
    """Book an appointment form"""
    return render(request, 'booking_system/book.html')

def counselor_list(request):
    """List of available counselors"""
    return render(request, 'booking_system/counselors.html')

@login_required
def my_appointments(request):
    """User's booked appointments"""
    return render(request, 'booking_system/my_appointments.html')
