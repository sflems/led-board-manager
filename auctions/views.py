from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing_view(request, listing_id): 

    listing = Listing.objects.get(pk=listing_id)
    form = BidForm(request.POST, instance=listing)
    commentform = CommentForm(request.POST, instance=listing)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                new_bid = form.cleaned_data["bid"]
                if listing.current_bid and listing.current_bid.bid < new_bid:
                    bid = Bid(listing=listing, bid=new_bid, user=request.user)
                    bid.save()
                    listing.current_bid = bid
                    listing.save()
                    return render (request, "auctions/listing.html", {
                        "listing": listing,
                        "form": form,
                        "commentform": CommentForm(),
                        "message": "Bid successful."
                    })
                elif listing.start_bid < new_bid:
                    bid = Bid(listing=listing, bid=new_bid, user=request.user)
                    bid.save()
                    listing.current_bid = bid
                    listing.save()
                    return render (request, "auctions/listing.html", {
                        "listing": listing,
                        "form": form,
                        "commentform": CommentForm(),
                        "message": "Bid successful."
                     })
                else:
                    return render (request, "auctions/listing.html", {
                        "listing": listing,
                        "form": form,
                        "commentform": CommentForm(),
                        "message": "Error: Bid must be greater than current bid."
                    })
        
            if commentform.is_valid():
                comment = Comment(listing_title=listing, comment=commentform.cleaned_data["comment"], user=request.user)
                comment.save()
                return render (request, "auctions/listing.html", {
                    "listing": listing,
                    "commentform": commentform,
                    "message": "Comment posted."
                })
            else:
                return render (request, "auctions/listing.html", {
                    "listing": listing,
                    "commentform": commentform,
                    "message": "Comment Failed."
                 })
        
        try:
            watchlist = Watchlist.objects.get(user=request.user) # Query watchlist
        except Watchlist.DoesNotExist:
            watchlist = Watchlist(user=request.user) 
            watchlist.save() # If no watchlist found for user, create one.

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": watchlist,
            "form": BidForm(),
            "commentform": CommentForm(),

        })
        
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": BidForm(),
            "commentform": CommentForm(),

        })

@login_required    
def close_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.is_active = 0
        listing.save()
    
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": BidForm(),
            "commentform": CommentForm(),

        })

@login_required    
def create(request):
    if request.method == "POST":
        listingform = ListingForm(request.POST)
        if listingform.is_valid():
            newlisting = Listing(title = listingform.cleaned_data["title"],
                description = listingform.cleaned_data["description"],
                image_URL = listingform.cleaned_data["image_URL"],
                category = listingform.cleaned_data["category"],
                start_bid = listingform.cleaned_data["start_bid"],
                user = request.user,)
            newlisting.save()
            
            return render (request, "auctions/listing.html", {
                        "listing": newlisting,
                        "form": BidForm(),
                        "commentform": CommentForm(),
                        "message": "Listing created successfully."
                     })
        
    else:   
        return render(request, "auctions/create.html", {
            "listingform": ListingForm(),
        })
        
@login_required     
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.get(user=request.user),
    })
    
@login_required     
def watchlist_add(request, listing_id):
    watchlist = Watchlist.objects.get(user=request.user)
    listing = Listing.objects.get(pk=listing_id)
    watchlist.items.add(listing)
    watchlist.save()
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "message": "Item successfully added to watchlist.",
    })

@login_required     
def watchlist_remove(request, listing_id):
    
    watchlist = Watchlist.objects.get(user=request.user)
    listing = Listing.objects.get(pk=listing_id)
    watchlist.items.remove(listing)
    watchlist.save()
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.get(user=request.user),
        "message": "Item successfully removed from watchlist.",
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    }) 
    
def categories_index(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category_id)
    return render(request, "auctions/categories_index.html", {
        "listings": listings,
        "category": category,
    })