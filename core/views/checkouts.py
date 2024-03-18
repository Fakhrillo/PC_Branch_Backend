from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
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


class CheckoutUpdateAPI(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, pk):
        data = request.data
        checkout_id = pk
        checkout = Checkouts.objects.get(pk=checkout_id)
        checkout_status = data['status']
        checkout.status = checkout_status

        worker_id = data['worker']
        worker = User.objects.get(pk=worker_id)
        
        if checkout_status == "open":
            worker.status = "working"
            if checkout.worker:
                checkout.worker.status = "free"
                checkout.worker.save()

            checkout.worker = worker

        else:
            worker.status = "free"
            checkout.worker = None
        
        checkout.save()
        worker.save()

        return Response(data=f" {checkout.status}")


class CheckoutDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    queryset = Checkouts.objects.all()
    serializer_class = CheckoutsSerializer