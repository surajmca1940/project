from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Counselor, Appointment, AvailableSlot
from .forms import SimpleCounselorForm
import datetime


class AvailableSlotInline(admin.TabularInline):
    model = AvailableSlot
    extra = 3
    fields = ['date', 'start_time', 'end_time', 'is_booked']
    readonly_fields = ['is_booked']
    ordering = ['date', 'start_time']
    
    class Media:
        css = {
            'all': ('admin/css/booking-admin.css',)
        }
        js = ('admin/js/booking-admin.js',)


class AppointmentStatusFilter(SimpleListFilter):
    title = 'appointment status'
    parameter_name = 'status_filter'
    
    def lookups(self, request, model_admin):
        return [
            ('confirmed', 'Confirmed Appointments'),
            ('pending', 'Pending Appointments'),
            ('cancelled', 'Cancelled Appointments'),
            ('completed', 'Completed Appointments'),
            ('today', 'Today\'s Appointments'),
            ('upcoming', 'Upcoming Appointments'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(date=timezone.now().date())
        elif self.value() == 'upcoming':
            return queryset.filter(date__gt=timezone.now().date())
        elif self.value() in ['confirmed', 'pending', 'cancelled', 'completed']:
            return queryset.filter(status=self.value())
        return queryset


@admin.register(Counselor)
class BookingCounselorAdmin(admin.ModelAdmin):
    form = SimpleCounselorForm
    list_display = ['get_counselor_name', 'get_specialization_badges', 'get_languages_badges', 
                   'get_availability_status', 'get_total_appointments', 'get_quick_actions']
    list_filter = ['is_available', 'specialization']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialization', 'languages']
    list_editable = []  # Removed is_available since we have custom display method
    inlines = [AvailableSlotInline]
    ordering = ['user__last_name', 'user__first_name']
    list_per_page = 20
    
    fieldsets = [
        ('👤 Basic Information', {
            'fields': ['first_name', 'last_name', 'email', 'username'],
            'classes': ['wide'],
            'description': 'Basic details for the counselor. Username will be auto-generated if left blank.'
        }),
        ('🎓 Professional Details (Optional)', {
            'fields': ['specialization', 'bio'],
            'classes': ['wide'],
            'description': 'Professional information with sensible defaults'
        }),
        ('🌍 Languages & Availability', {
            'fields': ['languages', 'is_available'],
            'classes': ['wide'],
            'description': 'Language support and availability status'
        })
    ]
    
    def get_counselor_name(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">' +
            '<span style="font-weight: 600; color: #2c5aa0;">{}</span>' +
            '</div>',
            obj.user.get_full_name() or obj.user.username
        )
    get_counselor_name.short_description = 'Counselor Name'
    get_counselor_name.admin_order_field = 'user__last_name'
    
    def get_specialization_badges(self, obj):
        specializations = [s.strip() for s in obj.specialization.split(',')]
        badges = []
        for spec in specializations[:3]:  # Show max 3 badges
            color_map = {
                'anxiety': '#e74c3c',
                'depression': '#8e44ad',
                'stress': '#f39c12',
                'trauma': '#e67e22',
                'grief': '#34495e',
                'relationships': '#e91e63'
            }
            spec_lower = spec.lower()
            color = next((color for key, color in color_map.items() if key in spec_lower), '#5bc0de')
            badges.append(
                f'<span class="specialization-badge" style="background: {color}; color: white; padding: 3px 8px; ' +
                f'border-radius: 12px; font-size: 10px; margin: 2px; display: inline-block;">{spec}</span>'
            )
        if len(specializations) > 3:
            badges.append(f'<span style="color: #666; font-size: 10px;">+{len(specializations)-3} more</span>')
        return format_html(''.join(badges))
    get_specialization_badges.short_description = 'Specializations'
    
    def get_languages_badges(self, obj):
        languages = [lang.strip() for lang in obj.languages.split(',')]
        badges = []
        for lang in languages[:4]:  # Show max 4 language badges
            badges.append(
                f'<span class="language-badge" style="background: #5bc0de; color: white; padding: 2px 6px; ' +
                f'border-radius: 8px; font-size: 9px; margin: 1px; display: inline-block;">{lang}</span>'
            )
        if len(languages) > 4:
            badges.append(f'<span style="color: #666; font-size: 9px;">+{len(languages)-4}</span>')
        return format_html(''.join(badges))
    get_languages_badges.short_description = 'Languages'
    
    def get_availability_status(self, obj):
        if obj.is_available:
            return format_html(
                '<span style="background: #5cb85c; color: white; padding: 4px 8px; border-radius: 12px; ' +
                'font-size: 10px; font-weight: 600;">🟢 AVAILABLE</span>'
            )
        else:
            return format_html(
                '<span style="background: #d9534f; color: white; padding: 4px 8px; border-radius: 12px; ' +
                'font-size: 10px; font-weight: 600;">🔴 UNAVAILABLE</span>'
            )
    get_availability_status.short_description = 'Status'
    get_availability_status.admin_order_field = 'is_available'
    
    def get_total_appointments(self, obj):
        total = obj.appointment_set.count()
        today = obj.appointment_set.filter(date=timezone.now().date()).count()
        upcoming = obj.appointment_set.filter(date__gt=timezone.now().date()).count()
        return format_html(
            '<div style="text-align: center;">' +
            '<div style="font-weight: 600; color: #2c5aa0;">{}</div>' +
            '<div style="font-size: 9px; color: #666;">Today: {} | Upcoming: {}</div>' +
            '</div>',
            total, today, upcoming
        )
    get_total_appointments.short_description = 'Appointments'
    
    def get_quick_actions(self, obj):
        change_url = reverse('admin:booking_system_counselor_change', args=[obj.id])
        appointments_url = reverse('admin:booking_system_appointment_changelist') + f'?counselor__id__exact={obj.id}'
        slots_url = reverse('admin:booking_system_availableslot_changelist') + f'?counselor__id__exact={obj.id}'
        
        return format_html(
            '<div style="display: flex; gap: 4px; flex-wrap: wrap;">' +
            '<a href="{}" class="admin-quick-action" style="background: #2c5aa0; color: white; padding: 4px 8px; ' +
            'border-radius: 4px; text-decoration: none; font-size: 9px;">📝 Edit</a>' +
            '<a href="{}" class="admin-quick-action" style="background: #5cb85c; color: white; padding: 4px 8px; ' +
            'border-radius: 4px; text-decoration: none; font-size: 9px;">📅 Appointments</a>' +
            '<a href="{}" class="admin-quick-action" style="background: #f0ad4e; color: white; padding: 4px 8px; ' +
            'border-radius: 4px; text-decoration: none; font-size: 9px;">⏰ Slots</a>' +
            '</div>',
            change_url, appointments_url, slots_url
        )
    get_quick_actions.short_description = 'Quick Actions'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user').annotate(
            appointment_count=Count('appointment')
        )
    
    class Media:
        css = {
            'all': ('admin/css/booking-admin.css',)
        }
        js = ('admin/js/booking-admin.js',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['get_student_info', 'get_counselor_info', 'get_appointment_datetime', 
                   'get_status_badge', 'get_session_type', 'get_quick_actions']
    list_filter = [AppointmentStatusFilter, 'date', 'counselor', 'created_at']
    search_fields = ['student__username', 'student__first_name', 'student__last_name',
                    'counselor__user__username', 'counselor__user__first_name', 'counselor__user__last_name',
                    'notes']
    list_editable = []  # Removed status since we have custom display method
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'get_appointment_duration']
    ordering = ['-date', '-time']
    list_per_page = 25
    actions = ['confirm_appointments', 'cancel_appointments', 'mark_completed']
    
    fieldsets = [
        ('📅 Appointment Details', {
            'fields': ['student', 'counselor', 'date', 'time', 'status'],
            'classes': ['wide']
        }),
        ('💬 Session Information', {
            'fields': ['notes'],
            'classes': ['wide'],
            'description': 'Private notes and session details'
        }),
        ('📊 Additional Information', {
            'fields': ['get_appointment_duration'],
            'classes': ['collapse']
        }),
        ('⏰ Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    def get_student_info(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">' +
            '<div>' +
            '<div style="font-weight: 600; color: #2c5aa0;">{}</div>' +
            '<div style="font-size: 10px; color: #666;">{}</div>' +
            '</div>' +
            '</div>',
            obj.student.get_full_name() or obj.student.username,
            obj.student.email
        )
    get_student_info.short_description = 'Student'
    get_student_info.admin_order_field = 'student__last_name'
    
    def get_counselor_info(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">' +
            '<div>' +
            '<div style="font-weight: 600; color: #5cb85c;">{}</div>' +
            '<div style="font-size: 9px; color: #666;">{}</div>' +
            '</div>' +
            '</div>',
            obj.counselor.user.get_full_name() or obj.counselor.user.username,
            obj.counselor.specialization[:30] + ('...' if len(obj.counselor.specialization) > 30 else '')
        )
    get_counselor_info.short_description = 'Counselor'
    get_counselor_info.admin_order_field = 'counselor__user__last_name'
    
    def get_appointment_datetime(self, obj):
        now = timezone.now()
        appointment_datetime = timezone.make_aware(
            datetime.datetime.combine(obj.date, obj.time)
        )
        
        time_diff = appointment_datetime - now
        if time_diff.total_seconds() > 0:
            if time_diff.days > 0:
                time_status = f'In {time_diff.days} days'
                color = '#5cb85c'
            elif time_diff.seconds > 3600:
                hours = time_diff.seconds // 3600
                time_status = f'In {hours}h'
                color = '#f0ad4e'
            else:
                minutes = time_diff.seconds // 60
                time_status = f'In {minutes}m'
                color = '#d9534f'
        else:
            time_status = 'Past'
            color = '#666'
        
        return format_html(
            '<div style="text-align: center;">' +
            '<div style="font-weight: 600; color: #2c5aa0;">{} {}</div>' +
            '<div style="font-size: 9px; color: {}; font-weight: 500;">{}</div>' +
            '</div>',
            obj.date.strftime('%b %d'),
            obj.time.strftime('%I:%M %p'),
            color,
            time_status
        )
    get_appointment_datetime.short_description = 'Date & Time'
    get_appointment_datetime.admin_order_field = 'date'
    
    def get_status_badge(self, obj):
        status_config = {
            'confirmed': {'color': '#5cb85c', 'icon': '✅', 'label': 'CONFIRMED'},
            'pending': {'color': '#f0ad4e', 'icon': '⏳', 'label': 'PENDING'},
            'cancelled': {'color': '#d9534f', 'icon': '❌', 'label': 'CANCELLED'},
            'completed': {'color': '#5bc0de', 'icon': '✨', 'label': 'COMPLETED'}
        }
        
        config = status_config.get(obj.status, {'color': '#666', 'icon': '❓', 'label': obj.status.upper()})
        
        return format_html(
            '<span data-status="{}" style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; ' +
            'font-size: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; ' +
            'box-shadow: 0 2px 4px rgba(0,0,0,0.2);">{} {}</span>',
            obj.status, config['color'], config['icon'], config['label']
        )
    get_status_badge.short_description = 'Status'
    get_status_badge.admin_order_field = 'status'
    
    def get_session_type(self, obj):
        # This would need to be added to the model, for now showing as placeholder
        session_types = ['📹 Video', '📞 Phone', '🏢 In-Person']
        import random
        session_type = random.choice(session_types)
        
        return format_html(
            '<span style="background: #e9ecef; color: #495057; padding: 3px 6px; border-radius: 8px; ' +
            'font-size: 9px; font-weight: 500;">{}</span>',
            session_type
        )
    get_session_type.short_description = 'Session Type'
    
    def get_quick_actions(self, obj):
        change_url = reverse('admin:booking_system_appointment_change', args=[obj.id])
        
        actions = []
        if obj.status == 'pending':
            actions.append(
                f'<button onclick="updateStatus({obj.id}, \'confirmed\')" ' +
                'style="background: #5cb85c; color: white; border: none; padding: 3px 6px; ' +
                'border-radius: 4px; font-size: 8px; cursor: pointer;">✅ Confirm</button>'
            )
        
        if obj.status in ['pending', 'confirmed']:
            actions.append(
                f'<button onclick="updateStatus({obj.id}, \'cancelled\')" ' +
                'style="background: #d9534f; color: white; border: none; padding: 3px 6px; ' +
                'border-radius: 4px; font-size: 8px; cursor: pointer;">❌ Cancel</button>'
            )
        
        if obj.status == 'confirmed':
            actions.append(
                f'<button onclick="updateStatus({obj.id}, \'completed\')" ' +
                'style="background: #5bc0de; color: white; border: none; padding: 3px 6px; ' +
                'border-radius: 4px; font-size: 8px; cursor: pointer;">✨ Complete</button>'
            )
        
        actions.append(
            f'<a href="{change_url}" style="background: #2c5aa0; color: white; padding: 3px 6px; ' +
            'border-radius: 4px; text-decoration: none; font-size: 8px;">📝 Edit</a>'
        )
        
        return format_html('<div style="display: flex; gap: 2px; flex-wrap: wrap;">{}</div>', ''.join(actions))
    get_quick_actions.short_description = 'Quick Actions'
    
    def get_appointment_duration(self, obj):
        # Placeholder for appointment duration calculation
        return "1 hour (standard)"
    get_appointment_duration.short_description = 'Duration'
    
    # Custom admin actions
    def confirm_appointments(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} appointments were successfully confirmed.', messages.SUCCESS)
    confirm_appointments.short_description = "✅ Confirm selected appointments"
    
    def cancel_appointments(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} appointments were cancelled.', messages.WARNING)
    cancel_appointments.short_description = "❌ Cancel selected appointments"
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} appointments were marked as completed.', messages.SUCCESS)
    mark_completed.short_description = "✨ Mark selected appointments as completed"
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('student', 'counselor__user')
    
    class Media:
        css = {
            'all': ('admin/css/booking-admin.css',)
        }
        js = ('admin/js/booking-admin.js',)


@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ['get_counselor_info', 'get_slot_datetime', 'get_duration', 'get_booking_status', 'get_quick_actions']
    list_filter = ['is_booked', 'date', 'counselor']
    search_fields = ['counselor__user__username', 'counselor__user__first_name', 'counselor__user__last_name']
    list_editable = []  # Removed is_booked since we have custom display method
    date_hierarchy = 'date'
    ordering = ['-date', 'start_time']
    list_per_page = 30
    actions = ['mark_as_booked', 'mark_as_available']
    
    fieldsets = [
        ('👥 Counselor & Slot Details', {
            'fields': ['counselor', 'date', 'start_time', 'end_time'],
            'classes': ['wide']
        }),
        ('📊 Booking Status', {
            'fields': ['is_booked'],
            'classes': ['wide']
        })
    ]
    
    def get_counselor_info(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">' +
            '<div>' +
            '<div style="font-weight: 600; color: #2c5aa0;">{}</div>' +
            '<div style="font-size: 9px; color: #666;">{}</div>' +
            '</div>' +
            '</div>',
            obj.counselor.user.get_full_name() or obj.counselor.user.username,
            obj.counselor.specialization[:25] + ('...' if len(obj.counselor.specialization) > 25 else '')
        )
    get_counselor_info.short_description = 'Counselor'
    get_counselor_info.admin_order_field = 'counselor__user__last_name'
    
    def get_slot_datetime(self, obj):
        now = timezone.now().date()
        days_diff = (obj.date - now).days
        
        if days_diff < 0:
            time_status = 'Past'
            color = '#666'
        elif days_diff == 0:
            time_status = 'Today'
            color = '#d9534f'
        elif days_diff == 1:
            time_status = 'Tomorrow'
            color = '#f0ad4e'
        else:
            time_status = f'In {days_diff} days'
            color = '#5cb85c'
        
        return format_html(
            '<div style="text-align: center;">' +
            '<div style="font-weight: 600; color: #2c5aa0;">{}</div>' +
            '<div style="font-size: 9px; color: {}; font-weight: 500;">{}</div>' +
            '</div>',
            f"{obj.date.strftime('%b %d')} {obj.start_time.strftime('%I:%M %p')}",
            color,
            time_status
        )
    get_slot_datetime.short_description = 'Date & Start Time'
    get_slot_datetime.admin_order_field = 'date'
    
    def get_duration(self, obj):
        start_dt = datetime.datetime.combine(datetime.date.today(), obj.start_time)
        end_dt = datetime.datetime.combine(datetime.date.today(), obj.end_time)
        duration = end_dt - start_dt
        
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        duration_text = ''
        if hours > 0:
            duration_text += f'{hours}h '
        if minutes > 0:
            duration_text += f'{minutes}m'
        
        return format_html(
            '<div style="text-align: center;">' +
            '<div style="font-weight: 600; color: #5bc0de;">{}</div>' +
            '<div style="font-size: 9px; color: #666;">Until {}</div>' +
            '</div>',
            duration_text.strip() or '0m',
            obj.end_time.strftime('%I:%M %p')
        )
    get_duration.short_description = 'Duration'
    
    def get_booking_status(self, obj):
        if obj.is_booked:
            return format_html(
                '<span style="background: #d9534f; color: white; padding: 4px 8px; border-radius: 12px; ' +
                'font-size: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">' +
                '🔴 BOOKED</span>'
            )
        else:
            return format_html(
                '<span style="background: #5cb85c; color: white; padding: 4px 8px; border-radius: 12px; ' +
                'font-size: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">' +
                '🟢 AVAILABLE</span>'
            )
    get_booking_status.short_description = 'Status'
    get_booking_status.admin_order_field = 'is_booked'
    
    def get_quick_actions(self, obj):
        change_url = reverse('admin:booking_system_availableslot_change', args=[obj.id])
        
        actions = []
        
        if not obj.is_booked:
            actions.append(
                f'<button onclick="updateSlotStatus({obj.id}, true)" ' +
                'style="background: #d9534f; color: white; border: none; padding: 3px 6px; ' +
                'border-radius: 4px; font-size: 8px; cursor: pointer;">🔴 Mark Booked</button>'
            )
        else:
            actions.append(
                f'<button onclick="updateSlotStatus({obj.id}, false)" ' +
                'style="background: #5cb85c; color: white; border: none; padding: 3px 6px; ' +
                'border-radius: 4px; font-size: 8px; cursor: pointer;">🟢 Mark Available</button>'
            )
        
        actions.append(
            f'<a href="{change_url}" style="background: #2c5aa0; color: white; padding: 3px 6px; ' +
            'border-radius: 4px; text-decoration: none; font-size: 8px;">📝 Edit</a>'
        )
        
        return format_html('<div style="display: flex; gap: 2px; flex-wrap: wrap;">{}</div>', ''.join(actions))
    get_quick_actions.short_description = 'Quick Actions'
    
    # Custom admin actions
    def mark_as_booked(self, request, queryset):
        updated = queryset.update(is_booked=True)
        self.message_user(request, f'{updated} slots were marked as booked.', messages.WARNING)
    mark_as_booked.short_description = "🔴 Mark selected slots as booked"
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_booked=False)
        self.message_user(request, f'{updated} slots were marked as available.', messages.SUCCESS)
    mark_as_available.short_description = "🟢 Mark selected slots as available"
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('counselor__user')
    
    class Media:
        css = {
            'all': ('admin/css/booking-admin.css',)
        }
        js = ('admin/js/booking-admin.js',)
