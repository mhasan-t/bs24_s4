from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', "user_type"]

        extra_kwargs = {'password': {'write_only': True},
                        'full_name': {'required': True},
                        'user_type': {'required': True},
                        }

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
