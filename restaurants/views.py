
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from rest_framework.response import Response
from rest_framework import status

from .models import Restaurant, Menu, OfferedItem
from accounts.models import User
from .serializers import RestaurantsSerializer, MenuSerializer, OfferedItemSerializer
from .permissions import IsRestaurantManager, CanChangeMenu, CanChangeOffer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantsSerializer
    permission_classes = [permissions.IsAdminUser, IsRestaurantManager]

    def create(self, request):
        data = request.data
        manager = get_object_or_404(User, pk=request.data['manager'])

        if manager.user_type == 1:
            return Response({
                "details": "Invalid user."
            }, status=status.HTTP_400_BAD_REQUEST)

        data['manager'] = manager

        new = Restaurant.objects.create(**data)
        serializer = RestaurantsSerializer(new)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, CanChangeMenu]

    def create(self, request, rpk):
        data = request.data
        data['restaurant_id'] = rpk
        get_object_or_404(Restaurant, pk=rpk)

        new = Menu.objects.create(**data)
        serializer = MenuSerializer(new)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, rpk):
        get_object_or_404(Restaurant, pk=rpk)
        data = self.queryset.filter(restaurant_id=rpk)
        serialized = MenuSerializer(data, many=True)
        return Response(serialized.data)


class OfferedItemViewSet(viewsets.ModelViewSet):
    queryset = OfferedItem.objects.all()
    serializer_class = OfferedItemSerializer
    permission_classes = [permissions.IsAuthenticated, CanChangeOffer]

    def create(self, request, menu_pk):
        menu = get_object_or_404(Menu, pk=menu_pk)
        data = request.data
        data['menu'] = menu

        new = OfferedItem.objects.create(**data)
        serializer = OfferedItemSerializer(new)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, menu_pk):
        get_object_or_404(Menu, pk=menu_pk)
        data = self.queryset.filter(menu=menu_pk)
        serialized = OfferedItemSerializer(data, many=True)
        return Response(serialized.data)
