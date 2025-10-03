from django.urls import path

from . import views

app_name = "todo"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('todolist/<int:pk>/', views.todolist, name='todolist'),
    path('update/', views.update, name='update'),
    path('user/<int:pk>/', views.user, name='user')
]