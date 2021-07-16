"""
Commerce

EBay-like e-commerce auction site

Gemaakt door: Susanne Becker
"""

from django.urls import path

from . import views

"""
All the paths you can go to on the website
"""

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name ="create"),
    path("add_listing",views.add_listing,name ="add_listing"),
    path("listing/<int:number>",views.view_listing, name ="view_listing"),
    path("add_watchlist/<int:number>",views.add_watchlist,name = "add_watchlist"),
    path("remove_watchlist/<int:number>",views.remove_watchlist,name = "remove_watchlist"),
    path("close_auction/<int:number>",views.close_auction,name = "close_auction")
]
