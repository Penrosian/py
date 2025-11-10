from django.contrib import admin
from django.db import models

# Register your models here.
from.models import Todo_User, TodoItem, Team

class TodoItemInline(admin.TabularInline):
    model = TodoItem
    extra = 0

class UserInline(admin.TabularInline):
    model = Team.members.through
    extra = 0
    verbose_name = "Member"

class LeaderInline(admin.TabularInline):
    model = Team.leaders.through
    extra = 0
    verbose_name = "Leader"

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["username"]}),
        (None, {"fields": ["display_name"]}),
        (None, {"fields": ["friend_perms"]}),
        ]
    
    inlines = [TodoItemInline]

    list_display = ["username", "display_name"]
    search_fields = ["username"]

class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ]
    
    inlines = [UserInline, LeaderInline]

    list_display = ["name"]
    search_fields = ["name"]

admin.site.register(Todo_User, UserAdmin)
admin.site.register(Team, TeamAdmin)