from rest_framework import generics
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser

from ..models import *
from ..serializers import WorkersSerializer

class WorkersAPI(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    queryset = Workers.objects.all()
    serializer_class = WorkersSerializer