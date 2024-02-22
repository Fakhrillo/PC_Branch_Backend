from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from environs import Env
env = Env()
env.read_env()

from eskiz_sms import EskizSMS
import redis
import re
import random

from ..models import *
from ..serializers import WorkersSerializer

redis_client = redis.StrictRedis(host='localhost', port=6379)

class WorkersAPI(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    serializer_class = WorkersSerializer

    def get_queryset(self):
        queryset = User.objects.all().values('username', 'first_name', "position")
        return queryset

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

class IsWorkerExist(APIView):
    def get(self, request):
        username = request.data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error":"Invalid credentials"}, status=401)
        else:
            verification_code = ''.join(random.choice('0123456789') for i in range(6))
            redis_client.set(username, verification_code, ex=120)
            send_SMS(username, verification_code)
            return Response({"success": "Sms code has been sent to the user successfuly!"}, status=200)

class GET_TOKEN(APIView):
    def post(self, request):
        verif_code = request.data['verif_code']
        username = request.data['username']
        
        if not username or not verif_code:
            return Response({"error": "Username and verification code are required"}, status=400)
            
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error":"Invalid credentials"}, status=401)
        
        stored_code = redis_client.get(username)
        if stored_code and stored_code.decode('utf-8') == verif_code:

            refresh = RefreshToken.for_user(user)
            return Response({"access":str(refresh.access_token), "refresh":str(refresh)}, status=200)
        else:
            return Response({"error": "Invalid verification code"}, status=401)
    

def send_SMS(user_phone, random_code):
    email = env('email')
    password = env('password')
    cleaned_number = re.sub(r'\+', '', user_phone)
    eskiz = EskizSMS(email=email, password=password)
    eskiz.send_sms(cleaned_number, f'<#> Your verification code: {random_code}', from_whom='4546', callback_url=None)