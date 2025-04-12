from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.db.models import Count
from rest_framework import viewsets , status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User,Profile,Post,Follow,Comment
from .serializer import FollowSerializer




def get_posts(user_id=None, page_number=1, posts_per_page=10):
    """
    Fetches posts.
    If post_id is provided, fetches a specific post.
    If post_id is not provided, fetches all posts with pagination.
    """
    if user_id:
         if isinstance(user_id, list):
            # When filtering multiple users (e.g. followers)
            posts = Post.objects.filter(user__id__in=user_id).annotate(like_count=Count('likes')).order_by('-created_at')
         else:
            # Filtering posts from a single user
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

    # 🚫 Check if user is not authenticated
    if not user.is_authenticated:
        messages.error(request, "You must be logged in to like a post.")
        return redirect('login') 

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

def Follower_display(request):
    #Get users id
    user = request.user
    #fetch data from follow model
    followed_users = Follow.objects.filter(follower=user, follow_status=True)

    # Extract the user IDs of the users being followed
    following_user_ids = [follow.following.id for follow in followed_users]
    

    #fetching post of followers
    page_number = request.GET.get('page', 1)  # Get page number from query param
    posts = get_posts(user_id=following_user_ids, page_number=page_number)

    return render(request,"network/follow.html",{"following":followed_users, "posts":posts})


    

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    #to check the follow status
    # Custom action to check follow status between current user and the user of the post
  # Custom action to check follow status
    @action(detail=False, methods=["GET"], url_path="follow-status/(?P<follower_id>[^/.]+)/(?P<following_id>[^/.]+)")
    def follow_status(self, request, follower_id, following_id):
        """Check if the logged-in user is following another user."""
        is_following = bool(Follow.objects.filter(follower=follower_id, following=following_id).exists())
        return Response({"follow_status": is_following}, status=status.HTTP_200_OK)
    
      #create a create function for follow model validations
    def perform_create(self, serializer):
        #get data for follower and following
        follower = self.request.data.get("follower")
        following = self.request.data.get("following")

        #make sure thatthe user is not following themselves
        if follower == following:
            return Response({"error": "Can not follow your self"}, status= status.HTTP_406_NOT_ACCEPTABLE)
        
        # make suer the are no duplicate
        if Follow.objects.filter(follower=follower, following=following).exists():
            return Response({"error":"You already follow this user"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(follower_id=follower, following_id=following)
    
    @action(detail=False, methods=["DELETE"], url_path="unfollow/(?P<follower_id>[^/.]+)/(?P<following_id>[^/.]+)")
    def unfollow(self, request, follower_id=None, following_id=None):
          """Delete a follow relationship"""
          try:
             follow_instance = Follow.objects.get(follower_id=follower_id, following_id=following_id)
             follow_instance.delete()
             return Response({"message": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)
          except Follow.DoesNotExist:
              return Response({"error": "Follow relationship not found"}, status=status.HTTP_404_NOT_FOUND)

@login_required  # Ensures only logged-in users can access this view
def create_or_edit_comment(request, post_id=None, comment_id=None):
    if post_id:
       post = get_object_or_404(Post, id=post_id)
    elif comment_id:
         comment = get_object_or_404(Comment, id=comment_id)
         post = comment.post
    else:
        return redirect("index")  # or show 404

    
    if request.method == "POST":
        content = request.POST["content"]

        if comment_id:
              # Editing existing comment
            if comment.user != request.user:
                return redirect("index")  # Only owner can edit
            comment.content = content
            comment.save()
        else:
            Comment.objects.create(
                 user=request.user,
                 post=post,
                 content=content
                 )
         # Get redirect target (from query parameter)
        redirect_to = request.GET.get('redirect_to', 'index')  # Default to 'index' if not provided

        # If liking from profile page, include user ID in redirect
        if redirect_to == "profile_display":
              return redirect(reverse(redirect_to, args=[post.user.id]) + f'?post_id={post.id}')
    
        return redirect(reverse(redirect_to) + f'?post_id={post.id}')
