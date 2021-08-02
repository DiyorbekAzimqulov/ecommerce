from django import forms
from django.contrib.admin.helpers import checkbox
from django.forms.widgets import Textarea
from .models import Comment, Bid, Listing


class ListingForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    price = forms.IntegerField()
    image = forms.ImageField()
    category = forms.CharField(max_length=50)
    # class Meta:
    #     model = Listing
    #     fields = ['title', 'description', 'bid_amount', 'image', 'category']

class BidForm(forms.Form):
    bid_amount = forms.IntegerField(help_text="Your bid")

