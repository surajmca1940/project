from django.urls import path
from . import views

app_name = 'booking_system'

urlpatterns = [
    # Main booking pages
    path('', views.appointment_list, name='appointments'),
    path('book/', views.book_appointment, name='book'),
    path('counselors/', views.counselor_list, name='counselors'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    
    # API endpoints for enhanced booking
    path('confirm/', views.confirm_booking, name='confirm_booking'),
    path('availability/', views.get_availability, name='get_availability'),
    
    # Appointment management
    path('reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel'),
]
