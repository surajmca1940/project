from django.db import models
from django.contrib.auth.models import User

class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    languages = models.CharField(max_length=200, help_text="Comma-separated list of languages")
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Private notes from student")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['counselor', 'date', 'time']
        ordering = ['-date', '-time']
    
    def __str__(self):
        return f"{self.student.username} with {self.counselor} on {self.date}"

class AvailableSlot(models.Model):
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['counselor', 'date', 'start_time']
    
    def __str__(self):
        return f"{self.counselor} - {self.date} {self.start_time}-{self.end_time}"
