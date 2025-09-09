from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def forum_home(request):
    """Forum homepage"""
    return render(request, 'peer_support/forum.html')

def forum_category(request, category_id):
    """Posts in a specific category"""
    return render(request, 'peer_support/category.html', {'category_id': category_id})

def view_post(request, post_id):
    """View a forum post and replies"""
    return render(request, 'peer_support/post.html', {'post_id': post_id})

@csrf_exempt
def create_post_api(request):
    """API endpoint for creating forum posts"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()
            category = data.get('category', 'discussion')
            
            if not title or not content:
                return JsonResponse({
                    'error': 'Title and content are required',
                    'status': 'error'
                })
            
            # Here you would normally save to database
            # For now, we'll simulate a successful post creation
            
            return JsonResponse({
                'message': 'Post created successfully!',
                'status': 'success'
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
    """Create a new forum post"""
    return render(request, 'peer_support/create_post.html')

def volunteer_list(request):
    """List of peer volunteers"""
    return render(request, 'peer_support/volunteers.html')
