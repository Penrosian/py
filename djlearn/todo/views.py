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
        return User.objects.order_by('username')

def todolist(request, pk):
    user = get_object_or_404(User, pk=pk)
    todo_items = user.todoitem_set.order_by('id')
    return render(request, 'todo/todolist.html', {'user': user, 'todo_list': todo_items})
    
def update(request):
    # CSRF validation does not like any methods that aren't POST, so I just use that instead.
    if request.method == 'POST':
        if request.POST.get('action') == 'toggle':
            try:
                item_id = int(request.POST['item_id'])
                item = get_object_or_404(TodoItem, pk=item_id)
                item.completed = not item.completed
                item.save()
                return HttpResponse("Item updated successfully", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid item ID", status=400)
        elif request.POST.get('action') == 'edit':
            try:
                item_id = int(request.POST['item_id'])
                if request.POST.get('name'):
                    new_name = request.POST['name']
                if request.POST.get('description'):
                    new_description = request.POST['description']
                item = get_object_or_404(TodoItem, pk=item_id)
                if new_name:
                    item.name = new_name
                if new_description:
                    item.description = new_description
                item.save()
                return HttpResponse("Item edited successfully", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif request.POST.get('action') == 'add':
            try:
                user_id = int(request.POST['user_id'])
                name = request.POST['name']
                description = request.POST['description']
                user = get_object_or_404(User, pk=user_id)
                new_item = TodoItem(user=user, name=name, description=description, completed=False)
                new_item.save()
                return HttpResponse("Item added successfully", status=201)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif request.POST.get('action') == 'delete':
            try:
                item_id = int(request.POST['item_id'])
                item = get_object_or_404(TodoItem, pk=item_id)
                item.delete()
                return HttpResponse("Item deleted successfully", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid item ID", status=400)
        else:
            return HttpResponse("Invalid action", status=400)
    else:
        return HttpResponse("Method Not Allowed: " + request.method, status=405)

def user(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'todo/user.html', {'user': user})