from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse

from django.core.exceptions import *
from django.db import IntegrityError

from .models import *
import json


def index(request):
    posts = Post.objects.filter(is_active=1)
    return render(request, "network/index.html", {
        "posts": posts.order_by("-timestamp"),
        "postform": PostForm(),
    })
    

def view(request, view):

    posts = {}
    
    # Filter emails returned based on mailbox
    if view == "all_posts":
        try:
            posts = Post.objects.all().order_by("-timestamp")
        except ObjectDoesNotExist:
            return JsonResponse({"error": "No posts found."}, status=400)
    
    elif view == "following" and request.user.is_authenticated:
        try:
            if FollowingList.objects.get(user=request.user) != []:
                following = FollowingList.objects.get(user=request.user).followed_users.all()
                posts = Post.objects.filter(author__in=following)

        except ObjectDoesNotExist:
            return JsonResponse({"error": "No followed users to show posts for."}, status=400)
            


    # Return posts in reverse chronologial order
    return JsonResponse([post.serialize() for post in posts], safe=False)
    
@csrf_exempt
@login_required
def UpdatePost(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)


    # Update whether email is read or should be archived
    if request.method == "PUT":
        data = json.loads(request.body)
      # Fuctions to be performed on object
        ''' if data.get("read") is not None:
            email.read = data["read"] '''
        email.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
        
@csrf_exempt
@login_required
def CreatePost(request):

    # Composing a new email must be via POST
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

    return JsonResponse({"message": "Post created successfully."}, status=201)



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
