from django.db import models
from ckeditor.fields import RichTextField
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


class Workers(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    is_busy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Workers"


class Checkouts(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=50)
    worker = models.ForeignKey(Workers, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='closed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Checkouts"
    
class Notifications(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()
    worker = models.ForeignKey(Workers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Notifications"