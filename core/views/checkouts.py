from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from ..models import *
from ..serializers import CheckoutsSerializer

class CheckoutsAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Checkouts.objects.all()
    serializer_class = CheckoutsSerializer
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['status']


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