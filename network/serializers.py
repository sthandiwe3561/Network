from rest_framework import serializers
from .models import Post,User,ProfileSetup

class ProfileSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSetup
        fields = ('profile_picture', 'bio', 'location', 'birth_date')

#user serializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSetupSerializer(read_only=True)  # Fetch related profile details

    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','profile')

#api/serializer for post
class PostSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
     model= Post
     fields = ('id','user','content','image','hide','created_at')

