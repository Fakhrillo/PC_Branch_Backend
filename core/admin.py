from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
admin.site.unregister(Group)
# Register your models here.

@admin.register(Camera_details)
class CameraDetails(admin.ModelAdmin):
    list_display = ('id', 'MxID', 'located', 'status', 'stream_link', "created_at")
    list_display_links = ['id', 'MxID']
    list_filter = ['MxID', 'located', 'status']
    search_fields = ('id', 'MxID')

@admin.register(User)
class WorkersAdmin(admin.ModelAdmin):
    list_display = ('id', "username", "first_name", "position", "status", "created_at")
    list_display_links = ["id", "username"]
    list_filter = ["username", "position", "status"]
    search_fields = ("id", "username")

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "start_time", "end_time", "created_at")
    list_display_links = ["id", "username"]
    list_filter = ["username", "start_time", "end_time"]
    search_fields = ("id", "username", "start_time", "end_time")

@admin.register(Checkouts)
class CheckoutsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "worker", "status", "created_at")
    list_display_links = ["id", "name"]
    list_filter = ["name", "status"]

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "worker", "is_activated", "created_at")
    list_display_links = ["id", "title"]
    list_filter = ["title", "worker", "is_activated"]
    search_fields = ("id", "title", "worker")