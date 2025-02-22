from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile_setup", views.profile_setup, name="profile_setup"),

    #api path
    path("users/getuser/",views.getuser, name="getuser"),
    path("users/createuser/", views.createuser,name="createuser"),
    path("users/userdetails/<int:pk>", views.userdetails, name="userdetails"),
    path("createpost", views.createpost, name="createpost"),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)