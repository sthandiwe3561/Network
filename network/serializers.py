from rest_framework import serializers
from .models import Post,User,ProfileSetup,Follow

class ProfileSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSetup
        fields = ('profile_picture', 'bio', 'location', 'birth_date')

#user serializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSetupSerializer(read_only=True,  required=False)  # Fetch related profile details

    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','profile')

#api/serializer for post
class PostSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
     model= Post
     fields = ('id','user','content','image','hide','created_at')

class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id','follower','following','follow_status','created_at')

