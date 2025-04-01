from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.db.models import Count


from .models import User,Profile,Post



def get_posts(user_id=None, page_number=1, posts_per_page=10):
    """
    Fetches posts.
    If post_id is provided, fetches a specific post.
    If post_id is not provided, fetches all posts with pagination.
    """
    if user_id:
        # Fetch a specific post by ID
         # Fetch all posts by the given user, ordered by latest
        posts = Post.objects.filter(user=user_id).annotate(like_count=Count('likes')).order_by('-created_at')
    else:
        # Fetch all posts with like_count annotation
        posts = Post.objects.annotate(like_count=Count('likes')).order_by('-created_at')
        
    # Paginate posts
    paginator = Paginator(posts, posts_per_page)
    page_obj = paginator.get_page(page_number)  # Get the requested page
                
    return page_obj


def index(request):
    page_number = request.GET.get('page', 1)  # Get page number from query param
    post = get_posts(page_number=page_number)

    return render(request, "network/index.html",{"posts":post})


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


@login_required  # Ensures only logged-in users can access this view
def create_or_edit_post(request, post_id=None):

    #fecthing the users id 
    user = request.user

    #fetching all post
    page_number = request.GET.get('page', 1)  # Get page number from query param
    posts = get_posts(page_number=page_number)
    
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
       posts =Post.objects.all()

    
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

    return render(request, "network/index.html",{"post":post, "posts":posts})

def delete(request,post_id):
     #fecthing the users id 
    user = request.user
    
    
    post = get_object_or_404(Post, id=post_id)

    if post.user != user:
        return redirect("error_page")
    
    post.delete()
    return redirect("index")

def like_button(request,post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    if post:
        if user in post.likes.all():  # If the user already liked the post, unlike it
           post.likes.remove(user)
        else:  # Otherwise, like it
           post.likes.add(user)
           
     # Get redirect target (from query parameter)
    redirect_to = request.GET.get('redirect_to', 'index')  # Default to 'index' if not provided

    # If liking from profile page, include user ID in redirect
    if redirect_to == "profile_display":
        return redirect(reverse(redirect_to, args=[post.user.id]) + f'?post_id={post.id}')
    
    return redirect(reverse(redirect_to) + f'?post_id={post.id}')

def profile_display(request,user_id):
    profile  = Profile.objects.filter(user=user_id).first()

    #fetching user_id post
    page_number = request.GET.get('page', 1)  # Get page number from query param
    posts = get_posts(user_id=user_id, page_number=page_number)

    if profile:
        return render(request,"network/profile.html", {"profile":profile, "posts":posts})
    
    error = "Profile not available"
    return render(request,"network/profile.html",{"error":error})
