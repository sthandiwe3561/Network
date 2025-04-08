from rest_framework import serializers
from .models import Profile,User,Follow


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","image"]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only = True)

    class Meta:
        model = User
        fields =["id","username","profile"]

class FollowSerializer(serializers.ModelSerializer):
    #for creating or storing id for follow model (POST)
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only= True)

    class Meta:
        model = Follow
        fields = ["id","follower","following","follow_status"]