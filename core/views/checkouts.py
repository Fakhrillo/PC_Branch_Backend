from rest_framework import generics
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser

from ..models import *
from ..serializers import CheckoutsSerializer

class CheckoutsAPI(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    queryset = Checkouts.objects.all()
    serializer_class = CheckoutsSerializer


class CheckoutUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    queryset = Checkouts.objects.all()
    serializer_class = CheckoutsSerializer

class CheckoutDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    queryset = Checkouts.objects.all()
    serializer_class = CheckoutsSerializer