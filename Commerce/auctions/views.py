from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .forms import ListingForm, PictureForm, BidForm
from .models import User, Listing, Picture, Bid, Category


def index(request, *category):
    heading = "Active Listings"
    if category:
        listings = Listing.objects.filter(category=category[0])
        heading = category[0].category
    else:
        listings = Listing.objects.exclude(flActive=False)

    listing_pic(listings)

    return render(request, "auctions/index.html",{
            "items":listings,
            "heading":heading,
            "watch_count":count_watchlist(request),
            "categories":categories(),
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
        return render(request, "auctions/login.html",{
            "categories":categories(),
            })


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
        return render(request, "auctions/register.html",{
            "categories":categories(),
            })

# This view is for Create Listing
@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        # Lsiting Data Loading into database..
        form = ListingForm(request.POST)
        if form.is_valid():
            newListing = form.save(commit=False)
            newListing.creator = request.user
            newListing.save()

            # Image Data Loading into database..
            form = PictureForm(request.POST, request.FILES)
            if form.is_valid():
                newPic = form.save(commit=False)
                newPic.listing = newListing
                newPic.alt_text = newListing.title
                newPic.save()

            return HttpResponseRedirect(reverse('detail',args=(newListing.slug,)))

    return render(request, 'auctions/create.html',{
            "form":ListingForm,
            "picForm":PictureForm,
            "watch_count":len(request.user.watched_listings.all()),
            "categories":categories(),
        })

# This view is for detail Lising
def detail_listing(request, listing):
    item = Listing.objects.get(slug=listing)  
    winner = item.buyers
    return render(request,'auctions/detail.html',{
            "item": item,
            "pics": item.get_pictures.all(),
            "form": BidForm,
            "bid_len": Bid.objects.filter(auction=item),
            "watch_count": count_watchlist(request),
            "watcher": item.watchers.filter(username=request.user.username),
            "winner": winner,
            "categories":categories()
        })

# this view is for place bidding
@login_required(login_url='login')
def place_bid(request, listing):
    item = Listing.objects.get(slug=listing)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            offer = float(form.cleaned_data['offer'])
            # Check offer is grether than cuurentbid and startingbid
            if is_valid_offer(offer, item):
                cBid = form.save(commit=False)
                cBid.auction = item 
                cBid.user = request.user
                cBid.save()
                Listing.objects.filter(slug=listing).update(currentBid=offer)
            # Return an Error if offer is less than current or starting bid
            else:
                return render(request,'auctions/detail.html',{
                    "item": item,
                    "pics": item.get_pictures.all(),
                    "form": BidForm,
                    "bid_len": Bid.objects.filter(auction=item),
                    "watch_count":count_watchlist(request),
                    "watcher": item.watchers.filter(username=request.user.username),
                    "bidError":"Bid Must be higher than Current or Starting Bid!",
                 })

    return HttpResponseRedirect(reverse('detail_listing', args=(listing,)))

# Helper method for place_bid
def is_valid_offer(offer, item):
    # check if offer is greather than starting bid or current bid
    if offer > item.startingBid and (item.currentBid is None or offer > item.currentBid):
        return True
    else:
        return False

# This view is for add or remove watchlist
@login_required(login_url='login')
def change_watchlist(request, listing):
    item = Listing.objects.get(slug=listing)
    # Toggler
    if request.user in item.watchers.all():
        item.watchers.remove(request.user)
    else:
        item.watchers.add(request.user)

    return HttpResponseRedirect(reverse('detail',args=(listing,)))

# This method is for closing Auctions
@login_required(login_url='login')
def close_auction(request, listing):
    item = Listing.objects.get(slug=listing)
    # Check if listing have atleast single bid or Not!
    if item.currentBid:
        bid_list = Bid.objects.filter(auction=item)
        winner = bid_list.order_by('-offer')[0].user
        item.buyers = winner
        item.flActive = False
        item.save()
        return HttpResponseRedirect(reverse('detail',args=(listing,)))
    else:
        return render(request,'auctions/detail.html',{
                    "item": item,
                    "pics": item.get_pictures.all(),
                    "form": BidForm,
                    "bid_len": Bid.objects.filter(auction=item),
                    "watch_count":count_watchlist(request),
                    "watcher": item.watchers.filter(username=request.user.username),
                    "bidError":"For closing, listing must have alteast single bid!",
                 })

# this view is for categories
def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html',{
        "categories":categories,
        "watch_count":count_watchlist(request)
        })
# this view is for specific listing redirect to index
def select_category(request, category):
    cat = Category.objects.get(category=category)
    return index(request, cat)

# this view is For create Watchlist
@login_required(login_url='login')
def watchlist_view(request):
    listings = request.user.watched_listings.all()
    listing_pic(listings)
    return render(request, 'auctions/index.html',{
            "items":listings,
            "heading":"Watchlist",
            "watch_count":count_watchlist(request),
            "categories":categories(),
        })

@login_required(login_url='login')
def closed_listing(request):
    listings = Listing.objects.exclude(flActive=True)
    for listing in listings:
        listing.mainPicture = listing.get_pictures.first()

    return render(request, "auctions/index.html",{
            "items":listings,
            "heading":"Closed Listings",
            "watch_count":count_watchlist(request),
            "categories":categories(),
        })

def dashboard(request):
    creatorlistings = request.user.all_creator_listings.all()
    wonListings = request.user.buyers_lisitng.all()
    listing_pic(wonListings)
    listing_pic(creatorlistings)

    return render(request, 'auctions/dashboard.html',{
            "items":creatorlistings,
            'wonItems':wonListings,
            "heading":"Dashboard",
            "watch_count":count_watchlist(request),
            "categories":categories()
        })

# Helper Method
def count_watchlist(request):
    watch_count = None
    if request.user.is_authenticated:
        watch_count = len(request.user.watched_listings.all())
    
    return watch_count

def listing_pic(listings):
    for listing in listings:
        listing.mainPicture = listing.get_pictures.first()


def categories():
    return Category.objects.all()[:3]