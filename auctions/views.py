from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
    
    if request.method == "POST":
        if form.is_valid():
            new_bid = form.cleaned_data["bid"]
            if listing.current_bid and listing.current_bid.bid < new_bid:
                bid = Bid(bid=new_bid, user=request.user)
                bid.save()
                listing.current_bid = bid
                listing.save()
                return render (request, "auctions/listing.html", {
                    "listing": listing,
                    "form": form,
                    "message": "Bid succeeded."
                })
            elif listing.start_bid < new_bid:
                bid = Bid(bid=new_bid, user=request.user)
                bid.save()
                listing.current_bid = bid
                listing.save()
                return render (request, "auctions/listing.html", {
                    "listing": listing,
                    "form": form,
                    "message": "Bid succeeded."
                 })
            else:
                return render (request, "auctions/listing.html", {
                    "listing": listing,
                    "form": form,
                    "message": "Error: Bid must be greater than current bid."
                })

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(),
    })