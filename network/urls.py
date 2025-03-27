
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile",views.profile,name="profile"),
    path("post", views.create_or_edit_post, name="create_post"),
    path("post/<int:post_id>", views.create_or_edit_post, name="edit_post")
]
