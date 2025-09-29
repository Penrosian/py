from django.db.models import F
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from .models import User, TodoItem

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.filter(todoitem__isnull=False).order_by('username')