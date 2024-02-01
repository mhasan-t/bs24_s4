from django.db import models
from datetime import datetime

from restaurants.models import OfferedItem
from accounts.models import User


class Vote(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(OfferedItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'User [{self.user_id}] voted for item [{self.item}]'


class Winner(models.Model):
    item = models.ForeignKey(OfferedItem, on_delete=models.CASCADE)
    casted_votes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Menu [{self.item}] won with {self.casted_votes} votes.'
