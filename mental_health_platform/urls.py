"""
URL configuration for mental_health_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('ai-support/', include(('ai_support.urls', 'ai_support'), namespace='ai_support')),
    path('booking/', include(('booking_system.urls', 'booking_system'), namespace='booking_system')),
    path('resources/', include(('resources.urls', 'resources'), namespace='resources')),
    path('community/', include(('peer_support.urls', 'peer_support'), namespace='peer_support')),
    path('dashboard/', include(('admin_dashboard.urls', 'admin_dashboard'), namespace='admin_dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
