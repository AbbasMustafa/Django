from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from .models import User, Post, Follower, Comments
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json


def index(request, *objects):
    
    if len(objects) == 0:
        posts = Post.objects.all()
        heading = "All Posts"
    else:
        posts = []
        following = Follower.objects.get(userProfile=request.user)
        following = [follow for follow in following.following.all()]
        for post in following:
            posts += post.get_posts.all()
        heading = "Following"

    # Paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ownLikes = []
    likes = []
    comments = []
    for post in page_obj:
        if request.user in post.likes.all():
            ownLikes.append(1)
        else:
             ownLikes.append(0)
        likes.append(len(post.likes.all()))
        comments.append(len(post.get_comments.all()))

    return render(request, "network/index.html",{
            "form":PostForm,
            "posts":zip(page_obj, likes, ownLikes, comments),
            "heading":heading,
            "page_obj":page_obj,
        })

@login_required(login_url='login')
def newPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()

    return HttpResponseRedirect(reverse('index'))

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            follower = Follower.objects.create(userProfile=user)
            follower.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


## get_likes
# API
@login_required(login_url='login')
def get_likes(request):
    data_id = int(request.GET.get('id'))
    post = Post.objects.get(pk=data_id)
    flag = ""
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        flag = "Like"
    else: 
        post.likes.add(request.user)
        flag = "Liked"
    
    count = len(post.likes.all())
    return HttpResponse([count, flag])


## Profile view

def get_profile(request, profileName):

    user = User.objects.get(username=profileName)

    posts = user.get_posts.all()
    follow = user.get_user_followers.all()
    
    lenFollowers = len(follow[0].follower.all())
    lenFollowing = len(follow[0].following.all())


    if ( request.user in follow[0].follower.all() ):
        textFollow = "Following"
    else:
        textFollow = "Follow"
    
    # Paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ownLikes = []
    likes = []
    comments = []
    for post in page_obj:
        if request.user in post.likes.all():
            ownLikes.append(1)
        else:
             ownLikes.append(0)
        likes.append(len(post.likes.all()))
        comments.append(len(post.get_comments.all()))
    return render(request, 'network/profile.html',{
            "profileName":profileName,
            "posts":zip(page_obj, likes, ownLikes, comments),
            "lenFollowers":lenFollowers,
            "lenFollowing":lenFollowing,
            "textFollow":textFollow,
            "page_obj":page_obj,
            "countPost":len(user.get_posts.all()),
        })

@csrf_exempt
def get_follow(request):
    profileUser = request.GET.get('id');
    profileUser = User.objects.get(username=profileUser)

    # User Following
    followOn = Follower.objects.get(userProfile=profileUser)
    # request for following
    following = Follower.objects.get(userProfile=request.user)

    if request.user not in followOn.follower.all():
        followOn.follower.add(request.user)
        following.following.add(profileUser)
        textFollow = "Following"
    else:
        followOn.follower.remove(request.user)
        following.following.remove(profileUser)
        textFollow = "Follow"

    follow = profileUser.get_user_followers.all()
    lenFollowers = len(follow[0].follower.all())
    lenFollowing = len(follow[0].following.all())
        

    return JsonResponse({'lenFollowers':lenFollowers,
                            'lenFollowing':lenFollowing,
                                'textFollow':textFollow})

## following view
def get_following(request):
    return index(request, "abc")

@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = int(data['id'])
        post_value = data['value']

        Post.objects.filter(pk=post_id).update(post=post_value)

        return HttpResponse(post_value)

def get_comments(request, id):
    post = Post.objects.get(pk=id)

    if request.user in post.likes.all():
        ownLike = 1
    else:
        ownLike = 0

    like = len(post.likes.all())
    
    if request.method == "POST":
        value = request.POST['comment']
        comment = Comments(comment_by=request.user,
                                on_post=post,
                                    comment=value)
        comment.save()

    return render(request, 'network/comments.html',{
        "post":post,
        "like": like,
        "ownLike": ownLike,
        "comments":post.get_comments.all(),
        })