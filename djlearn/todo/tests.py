from django.test import TestCase

from .models import User, Team

# Create your tests here.

class TeamModelTests(TestCase):
    def test_team_creation(self):
        # Test creating a team and adding members and leaders
        team = Team.objects.create(name="Test Team")
        user1 = User.objects.create(username="user1", password="pass1")
        user2 = User.objects.create(username="user2", password="pass2")
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
        user1 = User.objects.create(username="user1", password="pass1")
        user2 = User.objects.create(username="user2", password="pass2")
        user1.friend_requests.add(user2)
        self.assertIn(user2, user1.friend_requests.all())
        self.assertNotIn(user1, user2.friend_requests.all())

class PermissionsTests(TestCase):
    def test_view_permission(self):
        user1 = User.objects.create(username="user", password="pass", friend_perms="V")
        user2 = User.objects.create(username="friend", password="pass")
        user1.friends.add(user2)
        response = self.client.get(f'/todo/todolist/{user1.id}/', {'user_id': user2.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/todo/update/', {'user_id': user2.id, 'todo_id': 1, 'completed': True})
        self.assertEqual(response.status_code, 403)
    
    def test_no_permission(self):
        user1 = User.objects.create(username="user", password="pass", friend_perms="P")
        user2 = User.objects.create(username="friend", password="pass")
        user1.friends.add(user2)
        response = self.client.get(f'/todo/todolist/{user1.id}/', {'user_id': user2.id})
        self.assertEqual(response.status_code, 403)

    def test_modify_permission(self):
        user1 = User.objects.create(username="user", password="pass", friend_perms="M")
        user2 = User.objects.create(username="friend", password="pass")
        user1.friends.add(user2)
        response = self.client.get(f'/todo/todolist/{user1.id}/', {'user_id': user2.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/todo/update/', {'user_id': user2.id, 'todo_id': 1, 'completed': True})
        self.assertEqual(response.status_code, 200)