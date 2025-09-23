from django.urls import path
from . import views

app_name = 'peer_support'

urlpatterns = [
    # Main forum pages
    path('', views.ForumHomeView.as_view(), name='forum_home'),
    path('search/', views.search_threads, name='search'),
    path('volunteers/', views.volunteer_list, name='volunteers'),
    
    # Thread management
    path('thread/create/', views.ThreadCreateView.as_view(), name='thread_create'),
    path('thread/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/<int:pk>/edit/', views.ThreadUpdateView.as_view(), name='thread_update'),
    path('thread/<int:pk>/delete/', views.ThreadDeleteView.as_view(), name='thread_delete'),
    
    # Reply management
    path('thread/<int:thread_pk>/reply/', views.create_reply, name='create_reply'),
    
    # Voting (AJAX endpoints)
    path('thread/<int:thread_pk>/vote/', views.vote_thread, name='vote_thread'),
    path('reply/<int:reply_pk>/vote/', views.vote_reply, name='vote_reply'),
    
    # Legacy URLs for backward compatibility
    path('forum/', views.forum_home, name='forum'),
    path('category/<int:category_id>/', views.forum_category, name='category'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('new-post/', views.create_post, name='create_post'),
    path('api/create-post/', views.create_post_api, name='create_post_api'),
]
