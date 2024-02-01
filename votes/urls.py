
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

votes_list = views.VotesViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
votes_detail = views.VotesViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

standings = views.Results.as_view({
    "get": "current_standings"
})

select_winner = views.WinnerViewSet.as_view({
    "get": "select_todays_winner"
})


urlpatterns = [
    path('', votes_list, name="votes"),
    path('current_standings/', standings, name="current_standings"),

    path('<int:pk>/', votes_detail,
         name="votes-detail"),
    path("select_todays_winner/", select_winner, name="select_winner")

]
