from django.urls import path
from . import views

urlpatterns = [
    path('random-chat/', views.random_chat_view, name='random_chat'),
    path('room/<str:room_name>/', views.chat_view, name='chat'),
]