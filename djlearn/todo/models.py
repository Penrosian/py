from django.db import models

# Create your models here.
class Todo_User(models.Model):
    username = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    friends = models.ManyToManyField('self')
    friend_perms = models.CharField(max_length=1,choices={
        "P": "None",
        "V": "View",
        "M": "Modify"
    }, default="V")
    everyone_perms = models.CharField(max_length=1,choices={
        "P": "None",
        "V": "View",
        "M": "Modify"
    }, default="P")
    friend_requests = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return self.username
    
class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(Todo_User, related_name='team_members')
    leaders = models.ManyToManyField(Todo_User, related_name='team_leaders')

    def __str__(self):
        return self.name
    
class TodoItem(models.Model):
    user = models.ForeignKey(Todo_User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    completed = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
    category = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name