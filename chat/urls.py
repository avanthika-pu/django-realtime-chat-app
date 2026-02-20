from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('chat/<str:username>/', views.chat_view, name='chat_view'),
    path('logout/', views.logout_view, name='logout'), # Point to custom logout
]
