from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create-listing',views.create_listing, name="create_listing"),
    path('categories', views.categories_view, name="categories_view"),
    path('categories/<str:category>', views.select_category, name='select_category'),
    path('watchlist_view', views.watchlist_view, name="watchlist_view"),
    path('closed_listing', views.closed_listing, name="closed_listing"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('<str:listing>', views.detail_listing, name="detail"),
    path('<str:listing>/place_bid', views.place_bid, name="place_bid"),
    path('<str:listing>/change_watchlist', views.change_watchlist, name="change_watchlist"),
    path('<str:listing>/close_auction', views.close_auction, name="close_auction"),

]
