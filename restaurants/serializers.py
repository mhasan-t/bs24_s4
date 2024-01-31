from .models import Restaurant
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class RestaurantsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location']
