from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q, Count, Prefetch
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.utils.html import escape
from django.contrib.auth.models import User
import json

from .models import ForumThread, Reply, Vote, Tag, PeerVolunteer


class ForumHomeView(ListView):
    """Forum homepage with recent and popular threads"""
    model = ForumThread
    template_name = 'peer_support/forum_home.html'
    context_object_name = 'threads'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ForumThread.objects.filter(is_active=True).select_related('author').prefetch_related(
            'tags', 'replies', 'votes'
        )
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        
        # Filter by tag
        tag_filter = self.request.GET.get('tag')
        if tag_filter:
            queryset = queryset.filter(tags__name=tag_filter)
        
        # Filter by author
        author_filter = self.request.GET.get('author')
        if author_filter:
            queryset = queryset.filter(author__username=author_filter)
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'recent')
        if sort_by == 'popular':
            # Sort by vote score and view count
            queryset = queryset.annotate(
                vote_score=Count('votes', filter=Q(votes__vote_type='up')) - 
                          Count('votes', filter=Q(votes__vote_type='down'))
            ).order_by('-vote_score', '-view_count')
        elif sort_by == 'views':
            queryset = queryset.order_by('-view_count')
        else:  # recent
            queryset = queryset.order_by('-is_pinned', '-last_activity')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()[:20]
        context['current_sort'] = self.request.GET.get('sort', 'recent')
        context['current_search'] = self.request.GET.get('search', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        context['current_author'] = self.request.GET.get('author', '')
        return context


class ThreadDetailView(DetailView):
    """View a single thread with replies"""
    model = ForumThread
    template_name = 'peer_support/thread_detail.html'
    context_object_name = 'thread'
    
    def get_queryset(self):
        return ForumThread.objects.filter(is_active=True).select_related('author').prefetch_related(
            'tags',
            Prefetch('replies', queryset=Reply.objects.filter(is_active=True).select_related('author'))
        )
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count (but not for the author)
        if not self.request.user.is_authenticated or obj.author != self.request.user:
            obj.increment_view_count()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Paginate replies
        replies = self.object.replies.filter(is_active=True, parent=None).order_by('created_at')
        paginator = Paginator(replies, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['replies'] = page_obj
        context['user_thread_vote'] = None
        context['user_reply_votes'] = {}
        
        if self.request.user.is_authenticated:
            # Get user's vote on this thread
            try:
                context['user_thread_vote'] = Vote.objects.get(
                    user=self.request.user, thread=self.object
                ).vote_type
            except Vote.DoesNotExist:
                pass
            
            # Get user's votes on replies
            reply_votes = Vote.objects.filter(
                user=self.request.user, reply__in=replies
            ).values_list('reply_id', 'vote_type')
            context['user_reply_votes'] = dict(reply_votes)
        
        return context


class ThreadCreateView(LoginRequiredMixin, CreateView):
    """Create a new forum thread"""
    model = ForumThread
    template_name = 'peer_support/thread_create.html'
    fields = ['title', 'content', 'tags', 'is_anonymous']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Your thread has been created successfully!')
        return response


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    """Update a forum thread (only by author)"""
    model = ForumThread
    template_name = 'peer_support/thread_update.html'
    fields = ['title', 'content', 'tags', 'is_anonymous']
    
    def get_queryset(self):
        return ForumThread.objects.filter(author=self.request.user, is_active=True)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your thread has been updated successfully!')
        return response


class ThreadDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a forum thread (only by author or admin)"""
    model = ForumThread
    template_name = 'peer_support/thread_confirm_delete.html'
    success_url = reverse_lazy('peer_support:forum_home')
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ForumThread.objects.filter(is_active=True)
        return ForumThread.objects.filter(author=self.request.user, is_active=True)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Soft delete
        self.object.is_active = False
        self.object.save()
        messages.success(request, 'Thread has been deleted successfully!')
        return redirect(self.success_url)


@login_required
@require_POST
def create_reply(request, thread_pk):
    """Create a reply to a thread"""
    thread = get_object_or_404(ForumThread, pk=thread_pk, is_active=True)
    
    if thread.is_locked:
        messages.error(request, 'This thread is locked and cannot accept new replies.')
        return redirect(thread.get_absolute_url())
    
    content = request.POST.get('content', '').strip()
    parent_id = request.POST.get('parent_id')
    is_anonymous = request.POST.get('is_anonymous') == 'on'
    
    if not content or len(content) < 5:
        messages.error(request, 'Reply content must be at least 5 characters long.')
        return redirect(thread.get_absolute_url())
    
    parent = None
    if parent_id:
        parent = get_object_or_404(Reply, pk=parent_id, thread=thread, is_active=True)
    
    Reply.objects.create(
        thread=thread,
        content=content,
        author=request.user,
        parent=parent,
        is_anonymous=is_anonymous
    )
    
    messages.success(request, 'Your reply has been posted successfully!')
    return redirect(thread.get_absolute_url())


@login_required
@require_POST
def vote_thread(request, thread_pk):
    """Vote on a thread (AJAX)"""
    thread = get_object_or_404(ForumThread, pk=thread_pk, is_active=True)
    vote_type = request.POST.get('vote_type')
    
    if vote_type not in ['up', 'down']:
        return JsonResponse({'error': 'Invalid vote type'}, status=400)
    
    if thread.author == request.user:
        return JsonResponse({'error': 'You cannot vote on your own thread'}, status=400)
    
    try:
        # Check if user already voted
        existing_vote = Vote.objects.get(user=request.user, thread=thread)
        if existing_vote.vote_type == vote_type:
            # Remove vote if clicking same type
            existing_vote.delete()
            action = 'removed'
        else:
            # Change vote type
            existing_vote.vote_type = vote_type
            existing_vote.save()
            action = 'changed'
    except Vote.DoesNotExist:
        # Create new vote
        Vote.objects.create(user=request.user, thread=thread, vote_type=vote_type)
        action = 'created'
    
    # Get updated vote score
    vote_score = thread.get_vote_score()
    
    return JsonResponse({
        'success': True,
        'vote_score': vote_score,
        'action': action,
        'vote_type': vote_type
    })


@login_required
@require_POST
def vote_reply(request, reply_pk):
    """Vote on a reply (AJAX)"""
    reply = get_object_or_404(Reply, pk=reply_pk, is_active=True)
    vote_type = request.POST.get('vote_type')
    
    if vote_type not in ['up', 'down']:
        return JsonResponse({'error': 'Invalid vote type'}, status=400)
    
    if reply.author == request.user:
        return JsonResponse({'error': 'You cannot vote on your own reply'}, status=400)
    
    try:
        # Check if user already voted
        existing_vote = Vote.objects.get(user=request.user, reply=reply)
        if existing_vote.vote_type == vote_type:
            # Remove vote if clicking same type
            existing_vote.delete()
            action = 'removed'
        else:
            # Change vote type
            existing_vote.vote_type = vote_type
            existing_vote.save()
            action = 'changed'
    except Vote.DoesNotExist:
        # Create new vote
        Vote.objects.create(user=request.user, reply=reply, vote_type=vote_type)
        action = 'created'
    
    # Get updated vote score
    vote_score = reply.get_vote_score()
    
    return JsonResponse({
        'success': True,
        'vote_score': vote_score,
        'action': action,
        'vote_type': vote_type
    })


def search_threads(request):
    """Advanced search for threads"""
    query = request.GET.get('q', '')
    tag = request.GET.get('tag', '')
    author = request.GET.get('author', '')
    sort_by = request.GET.get('sort', 'recent')
    
    threads = ForumThread.objects.filter(is_active=True)
    
    if query:
        threads = threads.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    
    if tag:
        threads = threads.filter(tags__name=tag)
    
    if author:
        threads = threads.filter(author__username__icontains=author)
    
    # Apply sorting
    if sort_by == 'popular':
        threads = threads.annotate(
            vote_score=Count('votes', filter=Q(votes__vote_type='up')) - 
                      Count('votes', filter=Q(votes__vote_type='down'))
        ).order_by('-vote_score', '-view_count')
    elif sort_by == 'views':
        threads = threads.order_by('-view_count')
    else:
        threads = threads.order_by('-last_activity')
    
    # Pagination
    paginator = Paginator(threads, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'threads': page_obj,
        'query': query,
        'tag': tag,
        'author': author,
        'sort_by': sort_by,
        'tags': Tag.objects.all()[:20]
    }
    
    return render(request, 'peer_support/search_results.html', context)


def volunteer_list(request):
    """List of peer volunteers"""
    volunteers = PeerVolunteer.objects.filter(is_active=True).select_related('user')
    return render(request, 'peer_support/volunteers.html', {'volunteers': volunteers})


# Legacy views for backward compatibility
def forum_home(request):
    """Legacy forum homepage - redirect to new view"""
    return redirect('peer_support:forum_home')

def forum_category(request, category_id):
    """Legacy category view"""
    return render(request, 'peer_support/category.html', {'category_id': category_id})

def view_post(request, post_id):
    """Legacy post view"""
    return render(request, 'peer_support/post.html', {'post_id': post_id})

@csrf_exempt
def create_post_api(request):
    """Legacy API endpoint for creating forum posts"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()
            
            if not title or not content:
                return JsonResponse({
                    'error': 'Title and content are required',
                    'status': 'error'
                })
            
            if not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'You must be logged in to create a post',
                    'status': 'error'
                })
            
            # Create thread using new model
            thread = ForumThread.objects.create(
                title=title,
                content=content,
                author=request.user,
                is_anonymous=data.get('anonymous', False)
            )
            
            return JsonResponse({
                'message': 'Post created successfully!',
                'status': 'success',
                'thread_id': thread.id,
                'redirect_url': thread.get_absolute_url()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid data format',
                'status': 'error'
            })
        except Exception as e:
            return JsonResponse({
                'error': 'Something went wrong. Please try again.',
                'status': 'error'
            })
    
    return JsonResponse({'error': 'Invalid request method', 'status': 'error'})

@login_required
def create_post(request):
    """Legacy create post view - redirect to new view"""
    return redirect('peer_support:thread_create')
