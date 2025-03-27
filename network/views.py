from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse

from .models import User,Profile,Post


def index(request):
    return render(request, "network/index.html")


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
        return redirect("profile")
    else:
        return render(request, "network/register.html")
    
@login_required   
def profile(request):
    if request.method == 'POST':
        #fecthing data from create_profile form
        username = request.POST.get("username")
        bio = request.POST.get("description")
        image = request.FILES.get("image")

        #save the fields   
        # Ensure the logged-in user has a profile
        profile, created = Profile.objects.get_or_create(user=request.user)

        # Assign form values to the profile
        profile.username = username
        profile.bio = bio
        #check if the is an image uploaded
        if image:
            profile.image = image
        profile.save()

        return redirect ("index")
    
    return render(request,"network/create_profile.html")

def create_or_edit_post(request, post_id=None):

    #fecthing the users id 
    user = request.user
    
    if post_id:
        post = get_object_or_404(Post, id=post_id)

        if post.user != user:
            return redirect("error_page")
    else:
        post = None
    
    if request.method == "POST":
       #fetching data form the form
       content = request.POST.get("content")
       image = request.FILES.get("image")
    
       if post:
          post.content = content
          if image:
              post.image = image
          post.save()
       else:
           Post.objects.create(user = user, 
                               content = content,
                                image = image)
       return redirect("index")

    return render(request, "network/index.html",{"post":post})
