# Commerce

For minor programming we have to make an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Requirements

* Models: Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.
* Create Listing: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
* Active Listings Page: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).
* Listing Page: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
    * If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
    * If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
    * If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
    * If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
    * Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.

## Design document pages

### Index page

The user can see all active products here. You can also see at the top whether you are logged in or not and under what name.
<img src = design-images/logged-in.png>
<img src = design-images/logged-out.png>

### Login and Register

Pages to login and to register.
<img src = design-images/login.png>
<img src = design-images/register.png>

### Create

Page where the user can create a new product to sell.
<img src = design-images/create.png>

### Listing

Product page.
<img src = design-images/listing-signed.png>
<img src = design-images/listing-notsigned.png>


## Design document routes
<img src = design-images/card.png>


## Getting Started

1. install python and pip
2. clone the repository (in terminal) or download it as a zip file (click the green button at the top right):
```
$ git clone https://github.com/uva-webapps/commerce-Susanne-Becker.git
```
3. run in terminal:
```
$ python3 -m pip install Django
```
4. run in terminal:
```
$ python3 manage.py makemigrations auctions
```
5. run in terminal:
```
$ python3 manage.py migrate
```
6. run in terminal: 
```
$ python3 manage.py runserver
```

