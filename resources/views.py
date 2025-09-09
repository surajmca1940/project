from django.shortcuts import render
from django.shortcuts import get_object_or_404

def resource_list(request):
    """List all resources"""
    return render(request, 'resources/list.html')

def resources_by_category(request, category_id):
    """Resources filtered by category"""
    return render(request, 'resources/category.html', {'category_id': category_id})

def view_resource(request, resource_id):
    """View a specific resource"""
    return render(request, 'resources/view.html', {'resource_id': resource_id})

def search_resources(request):
    """Search resources"""
    query = request.GET.get('q', '')
    return render(request, 'resources/search.html', {'query': query})
