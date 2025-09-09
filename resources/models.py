from django.db import models
from django.contrib.auth.models import User

class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class")
    
    class Meta:
        verbose_name_plural = "Resource Categories"
    
    def __str__(self):
        return self.name

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('guide', 'Guide/Article'),
        ('worksheet', 'Worksheet'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, default='en')
    file_url = models.URLField(blank=True, help_text="External URL for the resource")
    file_upload = models.FileField(upload_to='resources/', blank=True)
    duration = models.IntegerField(blank=True, null=True, help_text="Duration in minutes for audio/video")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.resource_type})"

class ResourceView(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    class Meta:
        unique_together = ['resource', 'user']
