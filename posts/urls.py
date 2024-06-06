from django.urls import path
from .views import PostCreateView, PostListView, PostDeleteView, PostUpdateView, PostDetailView, CommentCreateView

app_name = "posts"
urlpatterns = [
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('new/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # comments
    path('comments/new/', CommentCreateView.as_view(), name='comment-create'),
]
