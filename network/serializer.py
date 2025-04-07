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
    # Writeable ID fields (for input)
    follower_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='follower', write_only=True
    )
    following_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='following', write_only=True
    )

    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only= True)

    class Meta:
        model = Follow
        fields = ["id","follower","follower_id","following","following_id","follow_status"]