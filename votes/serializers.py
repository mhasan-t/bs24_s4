from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from accounts.serializers import UserSerializer
from restaurants.serializers import OfferedItemSerializer
from .models import Vote, Winner


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    user_id = UserSerializer(many=False, read_only=True)
    item = OfferedItemSerializer(many=False, read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'created_at', 'user_id', 'item']


class WinnerSerializer(serializers.HyperlinkedModelSerializer):
    item = OfferedItemSerializer(many=False, read_only=True)

    class Meta:
        model = Winner
        fields = ['id', 'created_at', 'item']


class TodaysStandingsSerializer(serializers.Serializer):
    item = OfferedItemSerializer()
    vote_count = serializers.IntegerField()
