
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

menu_list = views.MenuViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
menu_detail = views.MenuViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

offered_item_list = views.OfferedItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
offered_item_detail = views.MenuViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', restaurants_list, name="restaurants"),
    path('<int:pk>/', restaurants_detail,
         name="restaurants-detail"),

    path('<int:rpk>/menu/', menu_list,
         name="restaurant-items"),
    path('menu/<int:pk>/', menu_detail,
         name="restaurant-items-detail"),

    path('menu/<int:menu_pk>/offers/', offered_item_list,
         name="restaurant-items"),
    path('menu/<int:menu_pk>/offers/<int:pk>/', offered_item_detail,
         name="restaurant-items-detail"),
]
