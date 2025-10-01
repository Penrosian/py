from django.contrib import admin
from django.db import models

# Register your models here.
from .models import User, TodoItem

class TodoItemInline(admin.TabularInline):
    model = TodoItem
    extra = 0
    formfield_overrides = {
        models.TextField: {'required': False},
    }

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["username"]}),
        ]
    
    inlines = [TodoItemInline]

    list_display = ["username"]
    search_fields = ["username"]

admin.site.register(User, UserAdmin)