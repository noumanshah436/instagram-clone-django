from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from posts.forms import PostForm
from .models import Post, Comment
from django.template.loader import render_to_string
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/home.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("home")
    success_message = "Post was created successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()  # Retrieve the Post instance
        comments = Comment.objects.filter(post=post).order_by(
            "-created_at"
        )  # Order comments by creation date (descending)
        context["comments"] = comments
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Post
    context_object_name = "post"
    success_url = reverse_lazy("home")
    success_message = "Post deleted successfully"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # check for ajax request
        if request.META.get("HTTP_X_REQUESTED_WITH") != "XMLHttpRequest":
            return JsonResponse({"error": "Invalid request"}, status=400)

        pk = request.POST.get("pk")
        comment_data = request.POST.get("commentData")

        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist."}, status=404)

        comment = Comment(content=comment_data, author=request.user, post=post)
        comment.save()

        comment_template = render_to_string(
            "comments/_comment.html", {"comment": comment}
        )
        return JsonResponse({"comment_template": comment_template})
