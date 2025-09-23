from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/coping-strategies/', views.get_coping_strategies, name='get_coping_strategies'),
    path('coping-strategies/', views.coping_strategies, name='coping_strategies'),
]
