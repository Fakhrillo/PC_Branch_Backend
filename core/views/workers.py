from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from ..models import *
from ..serializers import WorkersSerializer

class WorkersAPI(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    queryset = User.objects.all()
    serializer_class = WorkersSerializer

class WorkerUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    queryset = User.objects.all()
    serializer_class = WorkersSerializer

class WorkerDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    queryset = User.objects.all()
    serializer_class = WorkersSerializer

class GET_TOKEN(APIView):
    def post(self, request):
        password = request.data['password']
        username = request.data['username']

        print(password, username)
        user = User.objects.filter(username=username, password=password).first()
        print(user)
        if not user:
            return Response({"error":"Invalid credentials"}, status=401)
        refresh = RefreshToken.for_user(user)
        return Response({"access":str(refresh.access_token), "refresh":str(refresh)})