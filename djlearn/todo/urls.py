from django.urls import path

from . import views

app_name = "todo"
urlpatterns = [
    path('', views.index, name='index'),
    path('todolist/<int:pk>/', views.todolist, name='todolist'),
    path('update/', views.update, name='update'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('user/', views.user_redirect, name='user_redirect'),
    path('user/<int:pk>/', views.user, name='user'),
    path('team/<int:pk>/', views.team, name='team'),
    path('signup/', views.signup, name='signup'),
]