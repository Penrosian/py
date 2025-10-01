from django.db.models import F
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
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

def todolist(request, pk):
    user = get_object_or_404(User, pk=pk)
    todo_items = user.todoitem_set.order_by('id')
    return render(request, 'todo/todolist.html', {'user': user, 'todo_list': todo_items})
    
def update(request):
    if request.method == 'POST':
        try:
            item_id = int(request.POST['item_id'])
            item = get_object_or_404(TodoItem, pk=item_id)
            item.completed = not item.completed
            item.save()
            return HttpResponse("Item updated successfully", status=200)
        except (KeyError, ValueError):
            return HttpResponse("Invalid item ID", status=400)
    else:
        return HttpResponse("Method Not Allowed: " + request.method, status=405)