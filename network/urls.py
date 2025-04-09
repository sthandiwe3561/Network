
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile",views.profile,name="profile"),
    path("post", views.create_or_edit_post, name="create_post"),
    path("post/<int:post_id>", views.create_or_edit_post, name="edit_post"),
    path("delete/<int:post_id>", views.delete, name="delete"),
    path("like/<int:post_id>", views.like_button, name="like"),
    path("profile_display/<int:user_id>", views.profile_display, name="profile_display"),
    path("follow", views.Follower_display,name="follow")

]

router = DefaultRouter()
router.register('follow',views.FollowViewSet, basename="follow")

urlpatterns += [
        path("", include(router.urls)),
]

