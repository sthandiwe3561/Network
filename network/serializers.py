from rest_framework import serializers
from .models import Post,User

#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]

#api/serializer for post
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'