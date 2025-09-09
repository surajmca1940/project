from django.urls import path
from . import views

urlpatterns = [
    path('', views.resource_list, name='list'),
    path('category/<int:category_id>/', views.resources_by_category, name='by_category'),
    path('view/<int:resource_id>/', views.view_resource, name='view'),
    path('search/', views.search_resources, name='search'),
]
