from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name']
        extra_kwargs = {'password': {'write_only': True},}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
