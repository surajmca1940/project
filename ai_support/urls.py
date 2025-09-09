from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('coping-strategies/', views.coping_strategies, name='coping_strategies'),
]
