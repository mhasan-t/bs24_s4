from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from restaurants.models import OfferedItem

from .models import Vote, Winner
from .serializers import VoteSerializer, WinnerSerializer
from .permissions import IsEmployee


class VotesViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]

    def create(self, request):
        data = request.data
        user = get_object_or_404(User, pk=request.user.id)
        item = get_object_or_404(OfferedItem, pk=request.body["item_id"])

        data['user_id'] = user
        data['item_id'] = item

        new = Vote.objects.create(**data)
        serializer = VoteSerializer(new)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
