from django.contrib import admin
from .models import Region, Institution, LanguageSupport, UserProfile, Counselor, CounselorAvailability, OfflineSupportTicket


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country', 'primary_language', 'is_active', 'created_at']
    list_filter = ['country', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'primary_language']
    readonly_fields = ['created_at']


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'institution_type', 'region', 'is_active', 'created_at']
    list_filter = ['institution_type', 'region', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'contact_email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'code', 'institution_type', 'region', 'address', 'contact_email', 'contact_phone']
        }),
        ('Customization', {
            'fields': ['logo', 'primary_color', 'secondary_color', 'custom_css'],
            'classes': ['collapse']
        }),
        ('Features', {
            'fields': ['enable_ai_support', 'enable_peer_support', 'enable_offline_booking', 'enable_anonymous_mode']
        }),
        ('Configuration', {
            'fields': ['working_hours_start', 'working_hours_end', 'timezone', 'is_active']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]


@admin.register(LanguageSupport)
class LanguageSupportAdmin(admin.ModelAdmin):
    list_display = ['language_name', 'language_code', 'region', 'is_primary', 'is_active']
    list_filter = ['region', 'is_primary', 'is_active']
    search_fields = ['language_name', 'language_code']
    list_editable = ['is_primary', 'is_active']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'institution', 'preferred_language', 'is_anonymous', 'created_at']
    list_filter = ['institution', 'preferred_language', 'is_anonymous', 'show_in_peer_support']
    search_fields = ['user__username', 'user__email', 'institution__name']
    readonly_fields = ['created_at', 'updated_at']


class CounselorAvailabilityInline(admin.TabularInline):
    model = CounselorAvailability
    extra = 1


@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'institution', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['institution', 'is_active', 'languages', 'created_at']
    search_fields = ['full_name', 'email', 'specialization']
    filter_horizontal = ['languages']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CounselorAvailabilityInline]


@admin.register(CounselorAvailability)
class CounselorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['counselor', 'get_weekday_display', 'start_time', 'end_time', 'location', 'is_online']
    list_filter = ['weekday', 'is_online', 'counselor__institution']
    search_fields = ['counselor__full_name', 'location']


@admin.register(OfflineSupportTicket)
class OfflineSupportTicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'institution', 'counselor', 'status', 'scheduled_for', 'created_at']
    list_filter = ['status', 'institution', 'counselor', 'created_at']
    search_fields = ['subject', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
