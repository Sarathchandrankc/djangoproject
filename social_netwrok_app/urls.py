"""social_netwrok_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.SignupView.as_view(),name="register"),
    path("login",views.LoginView.as_view(),name="signin"),
    path('index',views.IndexView.as_view(),name="home"),
    path("posts/<int:id>comments/post",views.add_comment,name="add-comment"),
    path("comments/<int:id>/like/",views.like_cmt,name="like"),
    # path("posts/<int:id>/like/",views.like_pst,name="like"),
    path('posts/<int:id>/likes',views.post_likes,name="like-posts"),
    path('posts/all',views.MyPostsView.as_view(),name="myposts"),
    path('posts/<int:id>/delete',views.post_delete,name="post-delete"),
    path('logout',views.sign_out,name="signout"),
    path('user',views.UserProfileView.as_view(),name="userprof")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)