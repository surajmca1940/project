from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count, Q
from django.utils import timezone
from django.core.validators import MinLengthValidator

class Tag(models.Model):
    """Tags for categorizing forum threads"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_thread_count(self):
        return self.threads.filter(is_active=True).count()

class ForumThread(models.Model):
    """Main forum threads/posts"""
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    tags = models.ManyToManyField(Tag, blank=True, related_name='threads')
    is_anonymous = models.BooleanField(default=False, help_text="Hide author identity")
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_pinned', '-last_activity']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-last_activity']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('peer_support:thread_detail', kwargs={'pk': self.pk})
    
    def get_reply_count(self):
        return self.replies.filter(is_active=True).count()
    
    def get_vote_score(self):
        return self.votes.aggregate(
            score=Count('id', filter=Q(vote_type='up')) - Count('id', filter=Q(vote_type='down'))
        )['score'] or 0
    
    def get_display_author(self):
        if self.is_anonymous:
            return "Anonymous"
        return self.author.username
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

class Reply(models.Model):
    """Replies to forum threads"""
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(validators=[MinLengthValidator(5)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    is_anonymous = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['thread', 'created_at']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"Reply to {self.thread.title}"
    
    def get_vote_score(self):
        return self.votes.aggregate(
            score=Count('id', filter=Q(vote_type='up')) - Count('id', filter=Q(vote_type='down'))
        )['score'] or 0
    
    def get_display_author(self):
        if self.is_anonymous:
            return "Anonymous"
        return self.author.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update thread's last activity when a reply is added
        self.thread.update_last_activity()

class Vote(models.Model):
    """Votes for threads and replies"""
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Generic foreign key fields to vote on either threads or replies
    thread = models.ForeignKey(ForumThread, null=True, blank=True, on_delete=models.CASCADE, related_name='votes')
    reply = models.ForeignKey(Reply, null=True, blank=True, on_delete=models.CASCADE, related_name='votes')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'thread'], 
                condition=Q(thread__isnull=False),
                name='unique_user_thread_vote'
            ),
            models.UniqueConstraint(
                fields=['user', 'reply'], 
                condition=Q(reply__isnull=False),
                name='unique_user_reply_vote'
            ),
            models.CheckConstraint(
                check=(
                    Q(thread__isnull=False, reply__isnull=True) |
                    Q(thread__isnull=True, reply__isnull=False)
                ),
                name='vote_target_exclusivity'
            )
        ]
    
    def __str__(self):
        target = self.thread if self.thread else self.reply
        return f"{self.user.username} {self.vote_type}voted {target}"

# Keep the existing models for backward compatibility
class ForumCategory(models.Model):
    """Legacy model - keeping for backward compatibility"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Forum Categories"
    
    def __str__(self):
        return self.name

class ForumPost(models.Model):
    """Legacy model - keeping for backward compatibility"""
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
    """Legacy model - keeping for backward compatibility"""
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
