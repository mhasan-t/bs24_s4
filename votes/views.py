from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from django.db import models

from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from restaurants.models import OfferedItem

from .models import Vote, Winner
from .serializers import VoteSerializer, WinnerSerializer, TodaysStandingsSerializer
from .permissions import IsEmployee


class VotesViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsEmployee | permissions.IsAdminUser]

    def create(self, request):
        data = request.data
        user = get_object_or_404(User, pk=request.user.id)
        item = get_object_or_404(OfferedItem, pk=request.body["item_id"])

        data['user_id'] = user
        data['item_id'] = item

        new = Vote.objects.create(**data)
        serializer = self.serializer_class(new)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Results(viewsets.ViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def current_standings(self, request):
        votes = Vote.objects.values("item_id_id") \
            .annotate(vote_count=models.Count('user_id_id')) \
            .order_by('-vote_count')[:3]

        item_ids = [entry['item_id_id'] for entry in votes]
        items = OfferedItem.objects.filter(id__in=item_ids)
        item_mapping = {item.id: item for item in items}

        for entry in votes:
            entry['item'] = item_mapping[entry['item_id_id']]

        serialized = TodaysStandingsSerializer(votes, many=True)
        return Response(serialized.data)
