from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import UserProfile, Project

# Register your models here.


# Unregister Groups
admin.site.unregister(Group)


# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = UserProfile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    #     Just display username
    fields = ["username", "email", "first_name", "last_name"]
    inlines = [ProfileInline]


# Unregister initial User
admin.site.unregister(User)


# Register User and Profile
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'name_project', 'get_tags', 'created_at']

    def get_tags(self, obj):
        return ", ".join(o for o in obj.tags.names())
