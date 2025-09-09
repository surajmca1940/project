from django.db import models
from django.contrib.auth.models import User

class ForumCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Forum Categories"
    
    def __str__(self):
        return self.name

class ForumPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=True, help_text="Hide author identity")
    is_moderated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class ForumReply(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=True)
    is_moderated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply to {self.post.title}"

class PeerVolunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_trained = models.BooleanField(default=False)
    training_date = models.DateField(null=True, blank=True)
    specialties = models.TextField(help_text="Areas of expertise")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Volunteer: {self.user.get_full_name()}"
