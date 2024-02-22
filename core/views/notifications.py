from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from ..models import *
from ..serializers import NotificationsSerializer

class NotificationsAPI(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

class NotificationsListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = NotificationsSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user:
            return Response({"error": "This user is not valid"}, status=400)
        
        queryset = Notifications.objects.filter(worker_id=user).order_by("-created_at")
        serializer = self.serializer_class(queryset, many=True)
        
        response_data = {
            "notifications": serializer.data
        }
        
        return Response(response_data)