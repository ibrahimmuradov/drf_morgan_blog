from rest_framework import serializers
from ..models import Blog, Category, Tag, Comment

class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("user", "parent", "blog", "message")
        extra_kwargs = {
            'user': {'required': False},
            'parent': {'required': True},
            'blog': {'required': False},
            'message': {'required': False},
        }

    def validate(self, attrs):
        user = attrs.get('user')

        if not user:
            raise serializers.ValidationError({"error": "User not recognized"})
        if not user.is_authenticated:
            raise serializers.ValidationError({"error": "This user is not authenticated"})

        return attrs


class CommentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", )
        extra_kwargs = {
            'id': {'required': False}
        }


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"