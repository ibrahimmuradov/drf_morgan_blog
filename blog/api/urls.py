from django.urls import path
from . import views

app_name = 'blog-api'

urlpatterns = [
    path('blogs/', views.BlogsListView.as_view(), name='blogs'),
    path('post/<slug>/', views.BlogPostView.as_view(), name='post'),

    path('comments/', views.CommentsListView.as_view(), name='comments'),
    path('comment-create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment-delete/<int:id>/', views.CommentDeleteView.as_view(), name='comment-delete'),

    path('categories/', views.CategoriesListView.as_view(), name='categories'),
    path('tags/', views.TagsListView.as_view(), name='tags'),
]