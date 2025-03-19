from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .serializers import PostSerializer, FollowSerializer,UserSerializer
from .models import User, ProfileSetup,Post,Follow
#import from rest_framework
from rest_framework.pagination import PageNumberPagination
from .pagination import PostPagination  # Import custom pagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework import viewsets




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
        return HttpResponseRedirect(reverse("profile_setup"))
    else:
        return render(request, "network/register.html")

@login_required
def profile_setup(request):
    #fetch User data and accesing profile
    current_user = request.user
    profile = ProfileSetup.objects.filter(user=current_user).first()
    if request.method == "POST":
        #fetch input data
        first_name = request.POST["first_name"].capitalize()
        last_name = request.POST["last_name"].capitalize()
        date_birth = request.POST["date_of_birth"]
        location = request.POST["location"]
        email = request.POST["email"]
        bio = request.POST["bio"]
        profile_picture = request.FILES.get("profile_picture")

        #saving data in user model
        current_user.first_name = first_name
        current_user.last_name = last_name

        current_user.email = email
        current_user.save()
        #saving data in profile_setup model
         # Saving data in profile_setup model
        if profile:
            profile.birth_date = date_birth
            profile.location = location
            profile.bio = bio
            profile.profile_picture = profile_picture
            profile.save()  # Don't forget to save the profile!
        else:
            # Handle case if profile does not exist (create a new profile if necessary)
            profile = ProfileSetup.objects.create(
                user=current_user,
                birth_date=date_birth,
                location=location,
                bio=bio,
                profile_picture=profile_picture
            )
        login(request, current_user)

        return HttpResponseRedirect(reverse("index"))

    return render(request,"network/profile_setup.html", {
        "user":current_user
    })


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Assigns the authenticated user to the post before saving."""
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        """Override the context to pass the current user."""
        context = super().get_serializer_context()
        context['request'] = self.request  # Add the request to the context
        return context
    
    #it is to update some fields because viewset class when you use PUT it expect you to update all the  fields so this 
    #is to add an extra condition so the class will be able to also PUT some fileds not only all of them
    def update(self, request, *args, **kwargs):
        """Allow partial updates, specifically for hiding posts."""
        instance = self.get_object()
        data = request.data  # Get request data
        
         # Check if any update fields are provided in the request
        if 'content' in data or 'hide' in data or 'image' in request.FILES:
            # Update content if present in the request
            if 'content' in data:
                instance.content = data['content']
            
            # Update hide status if present in the request
            if 'hide' in data:
                instance.hide = data['hide']
            
            # Handle image update if a new image is provided
            if 'image' in request.FILES:
                instance.image = request.FILES['image']  # Update the image field

            # Save the updated post instance
            instance.save()

            return Response({"message": "Post updated successfully"}, status=status.HTTP_200_OK)

        else:
            # Return error response if no valid fields are provided
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['GET', 'POST', 'DELETE'], url_path=r'like/(?P<user_id>\d+)')
    def like(self, request, pk= None, user_id=None):
        """GET: Check if a user liked a post  
           POST: Like a post for a user  
           DELETE: Unlike a post for a user"""
        post = self.get_object()  # Fetch the post instance using pk
        try:
            user = User.objects.get(id=user_id)  # Get the user from `user_id`
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if request.method == "DELETE":
          print(f"User {user.id} is unliking Post {post.id}")  # Debugging

          post.likes.remove(user)
          post.save()  # Ensure it's saved
          return Response({"message": "Post unliked","liked": False, "like_count": post.likes.count()}, status=200)

    
        if request.method == "GET":
            liked = post.likes.filter(id=user.id).exists()
            like_count = post.likes.count()  # Get the total number of likes on the post

            return Response({"liked": liked,
                            "like_count": like_count}, status=200)

        if request.method == "POST":
           post.likes.add(user)
           post.save()
           return Response({"message": "Post liked", "liked":True, "like_count": post.likes.count()}, status=200)
        return Response({"message": "Already liked"}, status=400)
            

        
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [AllowAny]
    pagination_class = PostPagination  # Enable pagination for this view


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


        
    # Custom action to check follow status
    @action(detail=False, methods=["GET"], url_path="follow-status/(?P<follower_id>[^/.]+)/(?P<following_id>[^/.]+)")
    def follow_status(self, request, follower_id, following_id):
        """Check if the logged-in user is following another user."""
        is_following = bool(Follow.objects.filter(follower=follower_id, following=following_id).exists())
        return Response({"follow_status": is_following}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["DELETE"], url_path="unfollow/(?P<follower_id>[^/.]+)/(?P<following_id>[^/.]+)")
    def unfollow(self, request, follower_id, following_id):
          """Delete a follow relationship"""
          try:
             follow_instance = Follow.objects.get(follower_id=follower_id, following_id=following_id)
             follow_instance.delete()
             return Response({"message": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)
          except Follow.DoesNotExist:
              return Response({"error": "Follow relationship not found"}, status=status.HTTP_404_NOT_FOUND)

    # Custom action to get posts from users the current user follows
    @action(detail=False, methods=['GET'], url_path=r'following-posts/(?P<user_id>\d+)')
    def following_posts(self, request, user_id):
        """Retrieve posts only from users that the current user follows."""
        
        # Get a list of user IDs that the current user follows
        following_users = Follow.objects.filter(follower_id=user_id).values_list("following_id", flat=True)
        
        print(f"User {user_id} follows: {list(following_users)}")  # Debugging

        # Retrieve posts from those users
        posts = Post.objects.filter(user_id__in=following_users).order_by('-created_at')

        print(f"Posts retrieved: {posts.values()}")  # Debugging

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserViewSet(viewsets.ModelViewSet):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     permission_classes = [AllowAny]


     # Custom action to get followers count for a user
     @action(detail=False, methods=['GET'], url_path=r'followers-count/(?P<user_id>\d+)')
     def followers_count(self, request, user_id):
        """Retrieve the number of followers for a specific user."""
        try:
            user = User.objects.get(id=user_id)
            # Count followers using the 'following' field in the Follow model
            followers_count = Follow.objects.filter(following=user).count()
            return Response({"followers_count": followers_count}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

     # Custom action to get following count for a user
     @action(detail=False, methods=['GET'], url_path=r'following-count/(?P<user_id>\d+)')
     def following_count(self, request, user_id):
        """Retrieve the number of people a user is following."""
        try:
            user = User.objects.get(id=user_id)
            # Count following using the 'follower' field in the Follow model
            following_count = Follow.objects.filter(follower=user).count()
            return Response({"following_count": following_count}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



