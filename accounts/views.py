from .models import User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from django.http import Http404

from .serializers import UserSerializer


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not request.user.is_superuser and request.user.id != pk:
            return Response({
                "detail": "Unauthorized."
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView, PageNumberPagination):
    def get(self, request):
        users = User.objects.all()
        results = self.paginate_queryset(users, request, view=self)

        serializer = UserSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_superuser:
            return Response({
                "detail": "Unauthorized."
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(email__exact=request.data['email'])
            if user:
                return Response({
                    "detail": "User already exists."
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            new = User.objects.create_user(**request.data)
            serialized_data = UserSerializer(new).data

            return Response(serialized_data, status=status.HTTP_201_CREATED)
