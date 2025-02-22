from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .serializers import UserSerializer, PostSerializer
from .models import User, ProfileSetup
#import from rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
        return HttpResponseRedirect(reverse("profile_setup"))
    else:
        return render(request, "network/register.html")

def profile_setup(request):
    #fetch User data and accesing profile
    current_user = request.user
    profile = ProfileSetup.objects.filter(user=current_user).first()
    if request.method == "POST":
        #fetch input data
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        date_birth = request.POST["date_of_birth"]
        location = request.POST["location"]
        email = request.POST["email"]
        bio = request.POST["bio"]
        profile_picture = request.FILES.get("profile_picture")

        #saving data in user model
        current_user.first_name = first_name
        current_user.last_name = last_name

        if current_user.email is not email:
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

        return HttpResponseRedirect(reverse("index"))

    return render(request,"network/profile_setup.html", {
        "user":current_user
    })

#This is for user model
#get user
@api_view(['GET'])
def getuser(request):
    #get data fromthe model and display it
    user = User.objects.all()

    #serialize the data 
    serializer = UserSerializer(user,many=True)
    #returning the data that has been serialized
    return Response(serializer.data)



#create users
@api_view(['POST'])
def createuser(request):
    # GET the data from the input and serailize and save i
    serializer = UserSerializer(data = request.data)

    #check if the data we got above is valid and save it
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

#get a specific user delete the user or put(update) the user

@api_view(['GET','PUT','DELETE'])
def userdetails(request,pk):
    #fecth the users data by the id passed 
    try:
        user = User.objects.get(pk=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    #covering the get method for that particuler user
    if request.method == 'GET':
        #serializing the user requested data
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    #updating the certain users data 
    if request.method == 'PUT':
        #GET THE DATA THAT TO UPDATE WITH
        serializer = UserSerializer(user,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    #deleting the data for that requested user
    if request.method == 'DELETE':
        user.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createpost(request):
    serializer = PostSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_400_BAD_REQUEST)



