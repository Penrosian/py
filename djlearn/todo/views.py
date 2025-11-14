from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from accounts.views import SignUpView
from .models import Todo_User, TodoItem, Team

# Create your views here.

def index(request):
    return render(request, 'todo/index.html', {'todo_user': Todo_User.objects.get(username=request.user.username) if request.user.is_authenticated else None})

def todolist(request, pk):
    user = get_object_or_404(Todo_User, pk=pk)
    perms = user.everyone_perms
    if request.user.is_authenticated:
        self = get_object_or_404(Todo_User, username=request.user.username)
        if self == user:
            perms = 'M'
        elif self in user.friends.all():
            match user.friend_perms:
                case 'V':
                    if perms != 'M':
                        perms = 'V'
                case 'M':
                    perms = 'M'
    if perms == 'P':
        return HttpResponse("You do not have permission to view this user's todo list.", status=403)
    todo_items = user.todoitem_set.order_by('id')
    categories = Team.objects.filter(members=user).order_by('name')
    if categories.exists():
        categorized = []
        for category in categories:
            items_in_category = todo_items.filter(category=category)
            if items_in_category.exists():
                categorized.append({'name': category.name, 'todo_items': items_in_category, 'modify': True})
        uncategorized_items = todo_items.filter(category__isnull=True)
        if uncategorized_items.exists():
            categorized.append({'name': 'Uncategorized', 'todo_items': uncategorized_items, 'modify': True if perms == 'M' else False})
        return render(request, 'todo/todolist.html', {'user': user, 'categories': categorized})
    else:
        return render(request, 'todo/todolist.html', {'user': user, 'categories': [{'name': 'Uncategorized', 'todo_items': todo_items, 'modify': True if perms == 'M' else False}]})

def check_modify_permission(user, self):
    if self == user:
        return True
    elif user.everyone_perms == 'M':
        return True
    elif self in user.friends.all() and user.friend_perms == 'M':
        return True
    return False
def update(request, action) -> HttpResponse | HttpResponseRedirect:
    # CSRF validation does not like any methods that aren't POST, so I just use that for everything
    if request.method == 'POST':
        user = get_object_or_404(Todo_User, username=request.user.username) if request.user.is_authenticated else None
        if action == 'toggle':
            try:
                item_id = int(request.POST["item_id"])
                item = get_object_or_404(TodoItem, pk=item_id)
                if not check_modify_permission(item.user, user):
                    return HttpResponse("You do not have permission to modify this user's todo list.", status=403)
                item.completed = not item.completed
                item.save()
                return HttpResponse("Item updated successfully", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid item ID", status=400)
        elif action == 'edit':
            try:
                item_id = int(request.POST["item_id"])
                item = get_object_or_404(TodoItem, pk=item_id)
                if not check_modify_permission(item.user, user):
                    return HttpResponse("You do not have permission to modify this user's todo list.", status=403)
                item.name = request.POST['name']
                item.description = request.POST['description']
                item.save()
                return HttpResponse("Item edited successfully", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'add':
            try:
                user_id = int(request.POST["user_id"])
                item_user = get_object_or_404(Todo_User, pk=user_id)
                if not check_modify_permission(item_user, user):
                    return HttpResponse("You do not have permission to modify this user's todo list.", status=403)
                category_id = int(request.POST["category_id"])
                name = request.POST['name']
                description = request.POST['description']
                new_item = TodoItem(user=item_user, name=name, description=description, category=Team.objects.get(pk=category_id) if category_id != -1 else None)
                new_item.save()
                return HttpResponse("Item added successfully", status=201)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'delete':
            try:
                item_id = int(request.POST['item_id'])
                item = get_object_or_404(TodoItem, pk=item_id)
                if not check_modify_permission(item.user, user):
                    return HttpResponse("You do not have permission to modify this user's todo list.", status=403)
                item.delete()
                return HttpResponse("Item deleted successfully", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid item ID", status=400)
        elif action == 'deleteUser':
            try:
                user_id = int(request.POST['user_id'])
                delete_user = get_object_or_404(Todo_User, pk=user_id)
                if not delete_user == user:
                    return HttpResponse("Can only delete self", status=403)
                delete_user.delete()
                return HttpResponseRedirect(reverse('todo:index'))
            except (KeyError, ValueError):
                return HttpResponse("Invalid user ID", status=400)
        elif action == 'addFriend':
            try:
                friend_name = request.POST['friend_name']
                friend = get_object_or_404(Todo_User, username=friend_name)
                if friend == user:
                    return HttpResponse("Cannot add yourself as a friend", status=400)
                if friend in user.friends.all():
                    return HttpResponse("Already friends", status=400)
                if user in friend.friend_requests.all():
                    return HttpResponse("Friend request already sent", status=400)
                friend.friend_requests.add(user)
                friend.save()
                return HttpResponse("Friend request sent", status=201)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'acceptFriend':
            try:
                friend_id = int(request.POST['friend_id'])
                friend = get_object_or_404(Todo_User, pk=friend_id)
                if friend not in user.friend_requests.all():
                    return HttpResponse("No friend request from this user", status=400)
                user.friends.add(friend)
                user.friend_requests.remove(friend)
                user.save()
                return HttpResponse("Friend request accepted", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'removeFriend':
            try:
                friend_id = int(request.POST['friend_id'])
                friend = get_object_or_404(Todo_User, pk=friend_id)
                if friend not in user.friends.all():
                    return HttpResponse("Not friends with this user", status=400)
                user.friends.remove(friend)
                user.save()
                return HttpResponse("Friend removed", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'declineFriend':
            try:
                friend_id = int(request.POST['friend_id'])
                friend = get_object_or_404(Todo_User, pk=friend_id)
                if friend not in user.friend_requests.all():
                    return HttpResponse("No friend request from this user", status=400)
                user.friend_requests.remove(friend)
                user.save()
                return HttpResponse("Friend request declined", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'cancelFriendRequest':
            try:
                friend_id = int(request.POST['friend_id'])
                friend = get_object_or_404(Todo_User, pk=friend_id)
                if user not in friend.friend_requests.all():
                    return HttpResponse("No sent friend request to this user", status=400)
                friend.friend_requests.remove(user)
                friend.save()
                return HttpResponse("Friend request canceled", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'setFriendPerms':
            try:
                perms = request.POST['perms']
                if perms not in ['P', 'V', 'M']:
                    return HttpResponse("Invalid permissions value", status=400)
                user.friend_perms = perms
                user.save()
                return HttpResponse("Friend permissions updated", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'setEveryonePerms':
            try:
                perms = request.POST['perms']
                if perms not in ['P', 'V', 'M']:
                    return HttpResponse("Invalid permissions value", status=400)
                user.everyone_perms = perms
                user.save()
                return HttpResponse("Everyone permissions updated", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'setEmail':
            try:
                request.user.email = request.POST['email']
                request.user.save()
                return HttpResponse("Email updated successfully", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'setDisplayName':
            try:
                user.display_name = request.POST['display_name']
                user.save()
                return HttpResponse("Display name updated successfully", status=200)
            except (KeyError, ValueError):
                return HttpResponse("Invalid data provided", status=400)
        elif action == 'createTeam':
            try:
                team_name = request.POST['team_name']
                team = Team(name=team_name)
                team.save()
                team.leaders.add(user)
                team.save()
                return HttpResponseRedirect(reverse('todo:team', args=(team.id,)))
            except (KeyError, ValueError) as e:
                print(e)
                return HttpResponse("Invalid data provided", status=400)
        else:
            return HttpResponse("Invalid action", status=400)
    else:
        return HttpResponse("Method Not Allowed: " + request.method, status=405)

def edit(request, pk):
    user = get_object_or_404(Todo_User, pk=pk)
    todo_items = TodoItem.objects.filter(user=user)
    categories = Team.objects.filter(members=user).order_by('name')
    if categories.exists():
        categorized = []
        for category in categories:
            items_in_category = todo_items.filter(category=category)
            if items_in_category.exists():
                categorized.append({'name': category.name, 'todo_items': items_in_category, 'modify': True, 'id': category.id, 'super': False})
        uncategorized_items = todo_items.filter(category__isnull=True)
        if uncategorized_items.exists():
            categorized.append({'name': 'Uncategorized', 'todo_items': uncategorized_items, 'modify': True, 'id': -1, 'super': False})
        return render(request, 'todo/edit.html', {'user': user, 'categories': categorized})
    else:
        return render(request, 'todo/edit.html', {'user': user, 'categories': [{'name': 'Uncategorized', 'todo_items': todo_items, 'modify': True, 'id': -1, 'super': False}]})
    
def user(request, pk):
    user = get_object_or_404(Todo_User, pk=pk)
    categories = Team.objects.filter(members=user)
    categories = categories.union(Team.objects.filter(leaders=user))
    friend_requests = Todo_User.objects.filter(friend_requests=user)
    incoming_requests = user.friend_requests.all()
    friends = user.friends.all()
    self = get_object_or_404(Todo_User, username=request.user.username) if request.user.is_authenticated else None
    return render(request, 'todo/user.html', {'user': user, 'categories': categories, "friend_requests": friend_requests, "incoming_requests": incoming_requests, "friends": friends, "self": self})

def user_redirect(request):
    if request.user.is_authenticated:
        try:
            user = Todo_User.objects.get(username=request.user.username)
            return HttpResponseRedirect(reverse('todo:user', args=(user.id,)))
        except Todo_User.DoesNotExist:
            return HttpResponse("User not found. Try logging in again.", status=404)
    else:
        return HttpResponseRedirect(reverse('login'))

def team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = team.members.all()
    leaders = team.leaders.all()
    user = get_object_or_404(Todo_User, username=request.user.username) if request.user.is_authenticated else None
    if not user in team.members.all() and not user in team.leaders.all():
        return HttpResponse("You do not have permission to view this team.", status=403)
    todo_items = TodoItem.objects.filter(category=team)
    leader = user in team.leaders.all()
    return render(request, 'todo/team.html', {'team': team, 'members': members, 'leaders': leaders, 'todo_items': todo_items, 'user': user, 'leader': leader})

def signup(request):
    if request.method == 'POST':
        signup = SignUpView.as_view()(request)
        if signup.status_code == 302:
            Todo_User.objects.create(username=request.POST['username'], display_name=request.POST['username'])
        return signup
    else:
        return HttpResponse(status=405)