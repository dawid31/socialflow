from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('create-post', views.create_post, name="create-post"),
    path('login', views.login, name="login"),
    path('profile', views.profile, name="profile"),
    path('register', views.register, name="register"),
]
