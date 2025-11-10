from django.test import TestCase
from django.contrib.auth.models import User
from .models import Todo_User, Team

# Create your tests here.

class TeamModelTests(TestCase):
    def test_team_creation(self):
        # Test creating a team and adding members and leaders
        team = Team.objects.create(name="Test Team")
        user1 = Todo_User.objects.create(username="user1")
        user2 = Todo_User.objects.create(username="user2")
        team.members.add(user1)
        team.leaders.add(user2)
        self.assertIn(user1, team.members.all())
        self.assertIn(user2, team.leaders.all())
    
    def test_unique_team_name(self):
        # Test that team names must be unique
        Team.objects.create(name="Unique Team")
        with self.assertRaises(Exception):
            Team.objects.create(name="Unique Team")

class UserModelTests(TestCase):
    def test_friend_requests(self):
        # Test sending and receiving friend requests
        user1 = Todo_User.objects.create(username="user1")
        user2 = Todo_User.objects.create(username="user2")
        user1.friend_requests.add(user2)
        self.assertIn(user2, user1.friend_requests.all())
        self.assertNotIn(user1, user2.friend_requests.all())

class PermissionsTests(TestCase):
    def test_view_friend_permission(self):
        user1 = Todo_User.objects.create(username="user", friend_perms="V")
        user2 = Todo_User.objects.create(username="friend")
        self.user = User.objects.create_user(username="friend", password='12345')
        self.client.login(username='friend', password='12345')
        user1.friends.add(user2)
        response = self.client.get(f'/todo/todolist/{user1.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/todo/update/add/', "user_id=" + str(user1.id) + "&name=test&description=&category_id=-1", content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 403)
    
    def test_no_friend_permission(self):
        user1 = Todo_User.objects.create(username="user", friend_perms="P")
        user2 = Todo_User.objects.create(username="friend")
        user1.friends.add(user2)
        response = self.client.get(f'/todo/todolist/{user1.id}/')
        self.assertEqual(response.status_code, 403)
        response = self.client.post(f'/todo/update/add/', "user_id=" + str(user1.id) + "&name=test&description=&category_id=-1", content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 403)

    def test_modify_friend_permission(self):
        user1 = Todo_User.objects.create(username="user", friend_perms="M")
        user2 = Todo_User.objects.create(username="friend")
        user1.friends.add(user2)
        self.user = User.objects.create_user(username="friend", password='12345')
        self.client.login(username='friend', password='12345')
        response = self.client.get(f'/todo/todolist/{user1.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/todo/update/add/', "user_id=" + str(user1.id) + "&name=test&description=&category_id=-1", content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 201)
    
    def test_view_everyone_permission(self):
        user = Todo_User.objects.create(username="user", friend_perms="P", everyone_perms="V")
        response = self.client.get(f'/todo/todolist/{user.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/todo/update/add/', "user_id=" + str(user.id) + "&name=test&description=&category_id=-1", content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 403)

    def test_no_everyone_permission(self):
        user = Todo_User.objects.create(username="user", friend_perms="P", everyone_perms="P")
        response = self.client.get(f'/todo/todolist/{user.id}/')
        self.assertEqual(response.status_code, 403)
        response = self.client.post(f'/todo/update/add/', "user_id=" + str(user.id) + "&name=test&description=&category_id=-1", content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 403)

    def test_modify_everyone_permission(self):
        user = Todo_User.objects.create(username="user", friend_perms="P", everyone_perms="M")
        response = self.client.get(f'/todo/todolist/{user.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/todo/update/add/', "user_id=" + str(user.id) + "&name=test&description=&category_id=-1", content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 201)
    
    def test_lower_friend_permission(self):
        user1 = Todo_User.objects.create(username="user", friend_perms="V", everyone_perms="M")
        user2 = Todo_User.objects.create(username="friend")
        self.user = User.objects.create_user(username="friend", password='12345')
        self.client.login(username='friend', password='12345')
        user1.friends.add(user2)
        response = self.client.get(f'/todo/todolist/{user1.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/todo/update/add/', "user_id=" + str(user1.id) + "&name=test&description=&category_id=-1", content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 201)