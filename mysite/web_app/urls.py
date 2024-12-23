from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", UserProfileListViewSet, basename="users-list"),
router.register(r"users-detail", UserProfileDetailViewSet, basename="users-detail"),
router.register(r"post", PostViewSet, basename="post-list"),
router.register(r"post-detail", PostProfileViewSet, basename="post-detail"),
router.register(r"comment", CommentViewSet, basename="comment-list"),
router.register(r"story", StoryViewSet, basename="story-list"),
router.register(r"save", SaveViewSet, basename="save-list"),
router.register(r"save_item", SaveItemViewSet, basename="save_item-detail"),

urlpatterns = [
    path("", include(router.urls)),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]