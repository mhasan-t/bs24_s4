from .models import Restaurant, Menu, OfferedItem
from accounts.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title', 'description', 'restaurant_id']


class RestaurantsSerializer(serializers.HyperlinkedModelSerializer):
    items = MenuSerializer(many=True, read_only=True)
    manager = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'items', "manager"]


class OfferedItemSerializer(serializers.HyperlinkedModelSerializer):
    menu = MenuSerializer(many=False, read_only=True)

    class Meta:
        model = OfferedItem
        fields = ['id', 'date_offered_on', 'created_at', "menu"]
