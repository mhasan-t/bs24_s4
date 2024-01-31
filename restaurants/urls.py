
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

restaurants_list = views.RestaurantViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
restaurants_detail = views.RestaurantViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', restaurants_list, name="restaurants"),
    path('<int:pk>/', restaurants_detail,
         name="restaurants-detail"),
]
