from .models import Restaurant, FoodItem, OfferedItem
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class RestaurantsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location']


class FoodItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'title', 'description', 'restaurant_id']


class OfferedItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferedItem
        fields = ['id', 'date_offered_on', 'created_at']
