from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Camera_details(models.Model):
    MxID = models.CharField(max_length=50)
    located = models.CharField(max_length=155)
    status = models.BooleanField(default=False)
    stream_link = models.URLField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.MxID
    
    class Meta:
        verbose_name_plural = "Camera Details"


class User(AbstractUser):
    is_busy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=50)
    password = models.CharField(max_length=5,null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "User"

class WorkingHours(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        verbose_name_plural = "Working Hours"


class Checkouts(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=50)
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='closed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Checkouts"
    
class Notifications(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Notifications"