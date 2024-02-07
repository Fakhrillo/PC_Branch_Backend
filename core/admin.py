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

@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    list_display = ('id', "name", "phone_number", "is_busy", "created_at")
    list_display_links = ["id", "name"]
    list_filter = ["name", "phone_number", "is_busy"]
    search_fields = ("id", "name", "phone_number")

@admin.register(Checkouts)
class CheckoutsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "worker", "status", "created_at")
    list_display_links = ["id", "name"]
    list_filter = ["name", "status"]

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "worker", "created_at")
    list_display_links = ["id", "title"]
    list_filter = ["title", "worker"]
    search_fields = ("id", "title", "worker")