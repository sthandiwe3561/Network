from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView


from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile_setup", views.profile_setup, name="profile_setup"),


    #api path
   # path("post", views.PostView,name="postview"),
    #path("get", views.getpost, name="getpost")
]

router = DefaultRouter()
router.register('post', views.PostViewSet, basename="post"),
router.register('follow',views.FollowViewSet, basename="follow"),
router.register('user',views.UserViewSet, basename="user"),

urlpatterns += [
        path("", include(router.urls)),
        re_path(r"^.*$", TemplateView.as_view(template_name="network/layout.html")),  # Catch-all for React
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)