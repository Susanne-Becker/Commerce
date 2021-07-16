"""
Commerce

EBay-like e-commerce auction site

Gemaakt door: Susanne Becker
"""

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length= 128)
    start_value = models.IntegerField()
    category = models.CharField(max_length=64, default=None, blank=True, null=True)
    image_link = models.CharField(max_length=200, default=None, blank=True, null=True)
    watchlist = models.IntegerField(default = 0) 
    active = models.IntegerField(default = 0)
    winner = models.CharField(max_length=50, null = True, blank = True,default = None)

    def __str__ (self):
        return f"{self.title}"


class Bid(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name = "object")


    def __str__ (self):
        return f"{self.value}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name = "item")
    comment = models.CharField(max_length= 400)

    def __str__ (self):
        return f"{self.comment}"

