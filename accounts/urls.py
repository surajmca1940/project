from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .debug_views import auth_debug_view, protected_view

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('debug/auth/', auth_debug_view, name='auth_debug'),
    path('debug/protected/', protected_view, name='protected_view'),
]
