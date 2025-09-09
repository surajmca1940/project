from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointments'),
    path('book/', views.book_appointment, name='book'),
    path('counselors/', views.counselor_list, name='counselors'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
]
