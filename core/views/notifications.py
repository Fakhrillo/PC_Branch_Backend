from rest_framework import generics
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser

from ..models import *
from ..serializers import NotificationsSerializer

class NotificationsAPI(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer