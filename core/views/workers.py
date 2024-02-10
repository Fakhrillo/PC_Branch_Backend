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
        username = request.data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error":"Invalid credentials"}, status=401)
        refresh = RefreshToken.for_user(user)
        return Response({"access":str(refresh.access_token), "refresh":str(refresh)})
    
class IsWorkerExist(APIView):
    def get(self, request):
        username = request.data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error":"Invalid credentials"}, status=401)
        else:
            return Response({"Success":f"{user} is registered and can be accessed!"}, status=200)