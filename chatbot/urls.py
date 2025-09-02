from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chatbot_index'),
    path('reply/', views.reply, name='chatbot_reply'),
]