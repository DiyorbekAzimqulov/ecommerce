from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.expressions import Col, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from auctions.forms import ListingForm, BidForm
from auctions.models import User, Listing, Comment, Bid
from . import utils
import datetime


def index(request):
    listings = Listing.objects.filter(is_active=True)
    comments = Comment.objects.all()
    context = {
        "listings": listings,
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
@login_required
def create_listing(request):
    if request.method == "POST":
        print(request.user.id)

        form = ListingForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            form.cleaned_data['owner'] = request.user
            listing = Listing.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse("auctions:index"))
        return render(request, 'auctions/create_listing.html', {
            "form": form
        })
    return render(request, 'auctions/create_listing.html', {
        'form': ListingForm()
    })
@login_required
def listing_detail(request, id):
    comments = Comment.objects.filter(listing_id=id)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            max_bid = utils.get_max_bid(Bid.objects.filter(listing_id=id))
            if max_bid < form.cleaned_data['bid_amount']:
                Bid.objects.create(listing_id=Listing.objects.get(id=id), 
                owner=request.user, 
                bid_amount=form.cleaned_data['bid_amount']
                )
                L_object = Listing.objects.get(id=id)
                L_object.number_of_bids += 1
                L_object.save()
                
                return HttpResponseRedirect(reverse('auctions:listing-detail', args=(id,)))
            else:
                error = "You must enter more than current bid."
                context = {
                    "listing": Listing.objects.get(id=id),
                    "form": BidForm(),
                    "error": error,
                    "current_bid": max_bid,
                    "comments": comments
                }
                return render(request, "auctions/listing_detail.html", context)    
        listing = Listing.objects.get(id=id)
        current_bid = Bid.objects.filter(listing_id=listing)
        try:
            current_bid = current_bid[len(current_bid)-1]
        except:
            current_bid = 0
        context = {
            "listing": Listing.objects.get(id=id),
            "form": form,
            "current_bid": current_bid[len(current_bid)-1],
            "comments": comments
        }
        return render(request, "auctions/listing_detail.html", context)
    try:
        listing = Listing.objects.get(id=id)
        current_bid = Bid.objects.filter(listing_id=listing)
    except Listing.DoesNotExist:
        raise ValueError("Listing was not found.")
    try:
        current_bid = current_bid[len(current_bid)-1]
    except:
        current_bid = 0
    context = {
        "listing": listing,
        "form": BidForm(),
        "current_bid": current_bid,
        "comments": comments
    }
    return render(request, "auctions/listing_detail.html", context)

def categories(request):
    listings = []
    for listing in Listing.objects.all():
        if listing.category not in listings:
            listings.append(listing)
    context = {
        "listings": listings
    }
    return render(request, "auctions/categories.html", context)

# def list_categories(request, category):
#     listings = []
#     for listing in Listing.objects.all():
#         if listing.category == category:
#             listings.append(listing)
#     context = {
#         "listings": listings
#     }
#     return render(request, "auctions/list_categories.html", context)
@login_required
def watchlist(request):
    if request.method == "POST":
        watchlist_id = request.POST['watchlist_id']            
        listing_obj = Listing.objects.get(id=watchlist_id)
        if bool(int(request.POST['add'])):
            request.user.watchlist.add(listing_obj)
            return HttpResponseRedirect(reverse("auctions:watchlist"))
        request.user.watchlist.remove(listing_obj)
        return HttpResponseRedirect(reverse("auctions:watchlist"))
    watchlists = request.user.watchlist.all()
    context = {
        "watchlists": watchlists
    }
    return render(request, "auctions/watchlist.html", context)

def close_listing(request):
    if request.method == "POST":
        closing_obj_id = request.POST['close_id']
        bids = Bid.objects.filter(listing_id=int(closing_obj_id))
        max_bid = 0
        for bid in bids:
            if bid.bid_amount > max_bid:
                max_bid = bid.bid_amount
                winner = bid.owner.username
        listing = Listing.objects.get(id=int(closing_obj_id))
        listing.is_active = False
        listing.winner = winner
        listing.closed = datetime.datetime.now()
        listing.save()
        return HttpResponseRedirect(reverse("auctions:listing-detail", args=(int(closing_obj_id), )))
    
def inactive(request):
    listings = Listing.objects.filter(is_active=False)
    context = {
        "listings": listings
    }
    return render(request, "auctions/inactive.html", context)

def comment(request):
    if request.method == "POST":
        comment = Comment.objects.create(owner=request.user, 
                               listing_id=Listing.objects.get(id=int(request.POST['id'])),
                               text=request.POST['comment']
                               )
        comment.save()
        return HttpResponseRedirect(reverse("auctions:listing-detail", args=(int(request.POST['id']), )))