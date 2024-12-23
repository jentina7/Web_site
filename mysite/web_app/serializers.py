from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("username", "email", "password", "first_name", "last_name",
                 "bio", "image", "website")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "user": {
                "username": instance.username,
                "email": instance.email,
            },
            'access': str(refresh.access_token),
            "refresh": str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only= True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["username", "first_name", "last_name", "image"]


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["username","image"]

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ["comment", "like"]


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y" "%H:%M")
    user = UserProfileSimpleSerializer()
    comment_like = CommentLikeSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ["post", "user", "text", "parent", "created_at", "comment_like"]


class PostLikesSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = PostLike
        fields = ["user", "post", "like"]


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format="%d-%m-%Y" "%H:%M")
    post_like = PostLikesSerializer(many=True, read_only=True)
    post_comment = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ["user", "image", "video", "post_like", "description", "hashtag", "post_comment", "created_at"]


class FollowerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y" "%H:%M")
    class Meta:
        model = Follow
        fields = ["follower", "created_at"]


class FollowingSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y" "%H:%M")
    class Meta:
        model = Follow
        fields = ["following", "created_at"]


class StorySerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format="%d-%m-%Y" "%H:%M")
    class Meta:
        model = Story
        fields = ["user", "image", "video", "created_at"]


class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = '__all__'


class SaveItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y" "%H:%M")
    class Meta:
        model = SaveItem
        fields = ["save", "post", "created_at"]


class PostProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format="%d-%m-%Y" "%H:%M")
    post_like = PostLikesSerializer(many=True, read_only=True)
    post_comment = CommentSerializer(many=True, read_only=True)
    follower = FollowerSerializer(many=True, read_only=True)
    following = FollowingSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ["user", "image", "follower", "following", "video", "post_like", "description", "hashtag", "post_comment", "created_at"]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    post_user = PostProfileSerializer(many=True, read_only=True)
    follower = FollowerSerializer(many=True, read_only=True)
    following = FollowingSerializer(many=True, read_only=True)
    story_user = StorySerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = ["id", "username", "story_user", "first_name", "last_name", "image", "follower", "following", "bio", "website", "post_user"]

