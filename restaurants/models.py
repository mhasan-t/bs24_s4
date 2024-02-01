from django.db import models
from accounts.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=255, null=False)
    location = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField()
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.title} - {self.restaurant.name}'


class OfferedItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date_offered_on = models.DateField()

    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='offered')

    REQUIRED_FIELDS = ['date_offered_on']

    def __str__(self) -> str:
        return f'{self.menu.title} - Offered on {self.date_offered_on}'
