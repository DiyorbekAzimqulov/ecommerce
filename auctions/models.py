from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.files import ImageField


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="watchlisters")


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='listing/')
    category = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    closed = models.DateTimeField(blank=True, null=True)
    number_of_bids = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    winner = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()


    def __str__(self) -> str:
        return str(self.bid_amount)

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.TextField()


    def __str__(self) -> str:
        return self.owner.username