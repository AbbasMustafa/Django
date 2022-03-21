
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #################################################
    path('newPost',views.newPost, name="newPost"),
    path('following', views.get_following, name="following"),
    path('edit', views.edit_post, name="edit"),
    path('comments/<int:id>', views.get_comments, name="comments"),
    path('profile/<str:profileName>', views.get_profile, name="profile"),


    #API
    path("likes", views.get_likes, name="likes"),
    path("follow", views.get_follow, name="follow"),
]

