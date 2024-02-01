from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from django.db import models
from django.utils import timezone

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
        data['item'] = item

        new = Vote.objects.create(**data)
        serializer = self.serializer_class(new)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Results(viewsets.ViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def current_standings(self, request):
        votes = Vote.objects.select_related("item", "item__menu") \
            .filter(item__date_offered_on=datetime.now()) \
            .values("item_id", "item__menu_id") \
            .annotate(vote_count=models.Count('user_id_id')) \
            .order_by('-vote_count')[:4]

        three_days_ago = timezone.now() - timezone.timedelta(days=3)
        last_winners = Winner.objects.select_related("item") \
            .filter(created_at__range=[three_days_ago, timezone.now()])

        if last_winners.count() >= 3:
            last_3_days_winner = last_winners[0].item.menu.id
            same_winner = True
            for winner in last_winners:
                if winner.item.menu.id != last_3_days_winner:
                    same_winner = False

            if same_winner:
                votes = [v for v in votes if v["item__menu_id"]
                         != last_3_days_winner]

        item_ids = [entry['item_id'] for entry in votes]
        items = OfferedItem.objects.filter(id__in=item_ids)
        item_mapping = {item.id: item for item in items}

        for entry in votes:
            entry['item'] = item_mapping[entry['item_id']]

        serialized = TodaysStandingsSerializer(votes, many=True)
        return Response(serialized.data)


class WinnerViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def select_todays_winner(self, request):
        winner_obj_count = Winner.objects.filter(
            created_at__date=datetime.now()).count()

        if winner_obj_count > 0:
            return Response({
                "detail": "Todays winner has already been selected."
            })

        votes = Vote.objects.select_related("item") \
            .filter(item__date_offered_on=datetime.now()) \
            .values("item_id") \
            .annotate(vote_count=models.Count('user_id_id')) \
            .order_by('-vote_count')[:1]

        data = {}
        data["item_id"] = votes[0]["item_id"]
        data["casted_votes"] = votes[0]["vote_count"]
        new = Winner.objects.create(**data)

        serialized = WinnerSerializer(new)
        return Response(serialized.data)
