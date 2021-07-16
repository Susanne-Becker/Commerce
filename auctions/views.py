"""
Commerce

EBay-like e-commerce auction site

Gemaakt door: Susanne Becker
"""

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment


"""
Forms for new listings, new bids and new comments
"""
class NewListingForm(forms.Form):
    title = forms.CharField(label = "Title", widget = forms.TextInput(attrs = {'class': 'form-control'})) 
    desc = forms.CharField(label = "Description", widget = forms.Textarea(attrs = {'class': 'form-control'})) 
    bid = forms.FloatField(label = "Minimum price", widget = forms.TextInput(attrs = {'class': 'form-control'}))
    url = forms.CharField(label = "Image URL (optional)", required=False, widget = forms.TextInput(attrs = {'class': 'form-control'}))
    category = forms.CharField(label ="Category (optional)", required=False, widget = forms.TextInput(attrs = {'class': 'form-control'}))

class NewBidForm(forms.Form):
    value = forms.IntegerField(widget = forms.TextInput(attrs = {'class': 'form-control','placeholder': 'Bid'}))
    item_id = forms.IntegerField(widget = forms.HiddenInput())

class NewCommentForm(forms.Form):
    comment = forms.CharField(label = "Comment",widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Comment'}))
    item_id = forms.IntegerField(widget = forms.HiddenInput())


def index(request):
    """
    Display all active listings
    """
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active = 0)
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


def create(request):
    """
    Render to create.html with a form for new listings
    """
    return render(request,"auctions/create.html",{
        "form":NewListingForm()
    })

def add_listing(request):
    """
    Save new listing
    """
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():

            new_listing = Listing()
            new_listing.user = request.user
            new_listing.title = form.cleaned_data["title"]
            new_listing.description = form.cleaned_data["desc"]
            new_listing.category = form.cleaned_data["category"]
            new_listing.image_link = form.cleaned_data["url"]
            new_listing.start_value = form.cleaned_data["bid"]
            new_listing.save()

        return HttpResponseRedirect(reverse("index"))


def view_listing(request, number):
    """
    Show listing.html with up to date information
    """
    listing = Listing.objects.get(id = number)

    comments = Comment.objects.filter(item = listing)

    if request.method == 'GET':
        return render(request, "auctions/listing.html", {
            "listing":listing,
            "form_bid":NewBidForm(),
            "form_comment": NewCommentForm(),
            "comments":comments,
        })
    
    # request.method = "POST"
    else:
    
        # Save new bid
        form = NewBidForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data["value"]
            item_id = form.cleaned_data["item_id"]
            listing = Listing.objects.get(id=item_id)

            if(value > listing.start_value):
                new_bid = Bid()
                new_bid.value = value
                new_bid.item = listing
                new_bid.user = request.user
                new_bid.save()

                Listing.objects.filter(id = item_id).update(start_value = value)
                
                return render(request, "auctions/listing.html",{
                    "listing":listing,
                    "new_value": value,
                    "form_bid":NewBidForm(),
                    "form_comment": NewCommentForm(),
                    "comments":comments
                })
            else:
                return render(request,"auctions/error.html")

        # Save new comment
        commentform = NewCommentForm(request.POST)
        if commentform.is_valid():
            comment = commentform.cleaned_data["comment"]
            number = commentform.cleaned_data["item_id"]

            user_comment = Comment()
            user_comment.comment = comment
            user_comment.user = request.user
            user_comment.item = listing
            user_comment.save()
            return render(request, "auctions/listing.html", {
                "listing":listing,
                "form_bid":NewBidForm(),
                "form_comment": NewCommentForm(),
                "comments":comments
            })
        else:
            return render(request,"auctions/error.html")


def add_watchlist(request, number):
    """
    Add item to watchlist
    """
    listing = Listing.objects.get(id = number)
    comments = Comment.objects.filter(item = listing)
    Listing.objects.filter(id = number).update(watchlist = 1)
    return render(request, "auctions/listing.html", {
                "listing":listing,
                "form_bid":NewBidForm(),
                "form_comment": NewCommentForm(),
                "comments":comments
            })

def remove_watchlist(request, number):
    """
    Remove item from watchlist
    """
    listing = Listing.objects.get(id = number)
    comments = Comment.objects.filter(item = listing)
    watchlist = Listing.objects.filter(id = number).update(watchlist = 0)
    return render(request, "auctions/listing.html", {
                "listing":listing,
                "form_bid":NewBidForm(),
                "form_comment": NewCommentForm(),
                "comments":comments
            })
    
def close_auction(request, number):
    """
    Close the listing and determine who is the winner
    """
    listing = Listing.objects.get(id = number)
    comments = Comment.objects.filter(item = listing)
    highest_bid = Bid.objects.filter(item_id = number).last()

    Listing.objects.filter(id = number).update(active = 1)
    Listing.objects.filter(id = number).update(winner = highest_bid.user.username)

    return render(request, "auctions/listing.html", {
                "listing":listing,
                "form_bid":NewBidForm(),
                "form_comment": NewCommentForm(),
                "comments":comments
            })
