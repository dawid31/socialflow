from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('create-post', views.create_post, name="create-post"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('profile', views.profile, name="profile"),
    path('register', views.registerUser, name="register"),
]
