from rest_framework import generics
from rest_framework.response import Response
from .serializers import BlogsSerializer, CommentDeleteSerializer, CategoriesSerializer, TagsSerializer, CommentsSerializer, CommentCreateSerializer
from ..models import Blog, Category, Tag, Comment
from .paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from services.permissions import AccessPermission

class BlogsListView(generics.ListAPIView):
    serializer_class = BlogsSerializer
    permission_classes = (AccessPermission, )
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('title', 'subject')
    filterset_fields = ('tags', 'category')

    def get_queryset(self):
        blogs = Blog.objects.filter(status='Active')

        return blogs


class BlogPostView(generics.RetrieveAPIView):
    serializer_class = BlogsSerializer
    permission_classes = (AccessPermission,)
    lookup_field = "slug"

    def get_queryset(self):
        post = Blog.objects.filter(status='Active')

        return post


class CommentsListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    permission_classes = (AccessPermission,)
    serializer_class = CommentsSerializer


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentDeleteSerializer
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.filter(id=kwargs['id'])
        user = request.user

        if comment.exists():
            comment = Comment.objects.get(id=kwargs['id'])
            if user.is_authenticated:
                if comment.user == user:
                    comment.delete()
                    return Response({"success": "Comment deleted successfully"}, status=200)
                else:
                    return Response({"error": "Comment does not belong to user"}, status=404)
            else:
                return Response({"error": "This user is not authenticated"}, status=404)
        else:
            return Response({"error": "Comment not found"}, status=404)


class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AccessPermission,)
    serializer_class = CategoriesSerializer


class TagsListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = (AccessPermission,)
    serializer_class = TagsSerializer