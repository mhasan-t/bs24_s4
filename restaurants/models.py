from django.db import models
from accounts.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=255, null=False)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.name


class FoodItem(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.title} - {self.restaurant.name}'
