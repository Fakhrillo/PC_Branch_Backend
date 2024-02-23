from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser

from ..models import *
from ..serializers import WorkingHoursSerializer

class WorkingHoursAPI(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer

class WorkingHoursUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer