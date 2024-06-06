from django.urls import path
from .views import (
    CustomLoginView,
    SignUpView,
    update_profile,
    profile,
    follow_user,
    unfollow_user,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", SignUpView.as_view(), name="register"),
    path("profile/<int:id>", profile, name="profile"),
    path("update_profile/", update_profile, name="update-profile"),
    # follow unfollow users
    path("follow/<int:user_id>/", follow_user, name="follow-user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow-user"),
]
