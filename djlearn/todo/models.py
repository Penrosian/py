from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username
    
class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name