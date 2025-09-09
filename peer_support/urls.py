from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum'),
    path('category/<int:category_id>/', views.forum_category, name='category'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('new-post/', views.create_post, name='create_post'),
    path('volunteers/', views.volunteer_list, name='volunteers'),
]
