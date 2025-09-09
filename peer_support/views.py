from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def forum_home(request):
    """Forum homepage"""
    return render(request, 'peer_support/forum.html')

def forum_category(request, category_id):
    """Posts in a specific category"""
    return render(request, 'peer_support/category.html', {'category_id': category_id})

def view_post(request, post_id):
    """View a forum post and replies"""
    return render(request, 'peer_support/post.html', {'post_id': post_id})

@login_required
def create_post(request):
    """Create a new forum post"""
    return render(request, 'peer_support/create_post.html')

def volunteer_list(request):
    """List of peer volunteers"""
    return render(request, 'peer_support/volunteers.html')
