from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.urls import reverse

from django.core.exceptions import *
from django.db import IntegrityError

from .models import *
from django.core.paginator import Paginator



def index(request):
    posts = Post.objects.filter(is_active=1)
    paginator = Paginator(posts.order_by("-timestamp"), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Return paginated results.
    return render(request, "network/index.html", {'page_obj': page_obj})
    

def following(request):
    
    if request.user.is_authenticated:
    
        # Try to get posts from followed users in reverse chronologial order
        try:
            if FollowingList.objects.get(user=request.user) != []:
                following = FollowingList.objects.get(user=request.user).followed_users.all()
                posts = Post.objects.filter(author__in=following).order_by("-timestamp")
                paginator = Paginator(posts, 3)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                # Return paginated results.
                return render(request, "network/index.html", {'page_obj': page_obj})

        # If no following list exists or no followed users in list exceptions
        except FollowingList.ObjectDoesNotExist:
            return TemplateResponse(request, "network/index.html", {
                "error": "No followed users to show posts for.",
            })
        except FollowingList.EmptyResultSet:
            return TemplateResponse(request, "network/index.html", {
                "error": "No followed users to show posts for.",
            })
 
 
@login_required
def CreatePost(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    content = data.get("content")
    
    if len(content) <= 3:
        return JsonResponse({
            "error": "Post length must be greater than 3 characters."
        }, status=400)
        
    post = Post(
            author=request.user,
            content=content,
           )
    post.save()

    # Gets posts.html template, renders it as a string with post context for inserting HTML as json in following AJAX reponse.
    html = render_to_string("network/posts.html", {
        "post": post,
    }, request)

    return JsonResponse({
        "message": "Post created successfully.",
        "html": html,
        "post": post.id,
    }, status=200)
 
 
@login_required
def UpdatePost(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)


    # Update whether post is liked
    if request.method == "PUT":
        data = json.loads(request.body)
      # Fuctions to be performed on object
        if data.get("changed") is not None:
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user.id)
                post.save()
                return JsonResponse({
                    "message": "Post unliked successfully.",
                    "liked": False,
                    "likes": post.like_count(),
                    "post_id": post.id,
                }, status=202)
            else:
                post.likes.add(request.user.id)
                post.save()
                return JsonResponse({
                    "message": "Post liked successfully.",
                    "liked": True,
                    "likes": post.like_count(),
                    "post_id": post.id,
                }, status=202)
        

    # Update must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")