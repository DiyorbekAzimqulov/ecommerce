from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.files import ImageField


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    bid_amount = models.IntegerField()
    image = models.ImageField(upload_to='listing/')
    category = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.TextField()