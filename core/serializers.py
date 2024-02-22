from rest_framework import serializers
from .models import *

class CameraDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera_details
        fields = '__all__'

class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'position', 'status',]

class CheckoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkouts
        fields = '__all__'

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

class WorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        fields = '__all__'