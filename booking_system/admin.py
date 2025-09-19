from django.contrib import admin
from .models import Counselor, Appointment, AvailableSlot


@admin.register(Counselor)
class BookingCounselorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'languages', 'is_available']
    list_filter = ['is_available', 'specialization']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialization']
    list_editable = ['is_available']
    fieldsets = [
        ('User Information', {
            'fields': ['user']
        }),
        ('Professional Details', {
            'fields': ['specialization', 'bio', 'languages']
        }),
        ('Availability', {
            'fields': ['is_available']
        })
    ]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'counselor', 'date', 'time', 'status', 'created_at']
    list_filter = ['status', 'date', 'counselor', 'created_at']
    search_fields = ['student__username', 'counselor__user__username', 'notes']
    list_editable = ['status']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Appointment Details', {
            'fields': ['student', 'counselor', 'date', 'time', 'status']
        }),
        ('Notes', {
            'fields': ['notes']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]


@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ['counselor', 'date', 'start_time', 'end_time', 'is_booked']
    list_filter = ['is_booked', 'date', 'counselor']
    search_fields = ['counselor__user__username']
    list_editable = ['is_booked']
    date_hierarchy = 'date'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('counselor__user')
# Register your models here.
