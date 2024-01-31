
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .models import Restaurant, FoodItem, OfferedItem
from .serializers import RestaurantsSerializer, FoodItemSerializer, OfferedItemSerializer

from rest_framework.response import Response
from rest_framework import status


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, rpk):
        data = request.data
        data['restaurant_id'] = rpk
        get_object_or_404(Restaurant, pk=rpk)

        new = FoodItem.objects.create(**data)
        serializer = FoodItemSerializer(new)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, rpk):
        get_object_or_404(Restaurant, pk=rpk)
        data = self.queryset.filter(restaurant_id=rpk)
        serialized = FoodItemSerializer(data, many=True)
        return Response(serialized.data)


class OfferedItemViewSet(viewsets.ModelViewSet):
    queryset = OfferedItem.objects.all()
    serializer_class = OfferedItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, menu_pk):
        food_item = get_object_or_404(FoodItem, pk=menu_pk)
        data = request.data
        data['food_item'] = food_item

        new = OfferedItem.objects.create(**data)
        serializer = OfferedItemSerializer(new)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, menu_pk):
        get_object_or_404(FoodItem, pk=menu_pk)
        data = self.queryset.filter(food_item=menu_pk)
        serialized = OfferedItemSerializer(data, many=True)
        return Response(serialized.data)
