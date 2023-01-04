from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('create-post/', views.create_post, name="create-post"),
    path('post-details/<str:pk>/', views.post_details, name="post-details"),
    path('edit-post/<str:pk>/', views.edit_post, name="edit-post"),
    path('delete-post/<str:pk>/', views.delete_post, name="delete-post"),
    path('delete-comment/<str:pk>/', views.delete_comment, name="delete-comment"),
    path('edit-comment/<str:pk>/', views.edit_comment, name="edit-comment"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='DjangoBlogApp/password_reset.html'),
    name="password_reset"),

    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name='DjangoBlogApp/password_reset_done.html'),
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='DjangoBlogApp/password_reset_confirm.html'),
    name="password_reset_confirm"),

    path('password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='DjangoBlogApp/password_reset_complete.html'),
    name="password_reset_complete"),

    path('profile/<str:pk>/', views.profile, name="profile"),
    path('followers/<str:pk>/', views.followers, name="followers"),
    path('following/<str:pk>/', views.following, name="following"),
    path('register/', views.registerUser, name="register"),
]

'''
built in password reset functionality pattern:
--
in urls.py:

1)
    from django.contrib.auth import views as auth_views


2)
    submit ur email ->  auth_views.PasswordResetView.as_view()

    info that email was sent successfully -> auth_views.PasswordResetDoneView.as_view()

    template rendered after you enter link in your email -> auth_views.PasswordResetConfirmView.as_view()
    (uid64 and token args required in url for safety reasons!)  

    notification about successfully changed password -> auth_views.PasswordResetCompleteView.as_view()

3) add dynamic name for above urls listed in documentation
https://docs.djangoproject.com/en/3.0/topics/auth/default/#all-authentication-views
'''