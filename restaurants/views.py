from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Restaurant
from .serializers import RestaurantsSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
