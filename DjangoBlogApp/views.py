from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, AccountForm, PostForm
from .models import *

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    users = User.objects.all()
    users_and_posts = {}
    for user in users:
        user_posts = Post.objects.filter(host=user).count()
        users_and_posts[Post.objects.filter(host=user).first().host] = user_posts
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(name__icontains=q) |
        Q(content__icontains=q) |
        Q(host__username__icontains=q)
    )
    if request.method == "POST":
        content = request.POST.get('comment_content')
        Comment.objects.create(
            author = request.user,
            content = content,
            #post = ????
            )
    recent_posts = Post.objects.all().order_by('-published')[:5]
    recent_comments = Comment.objects.all().order_by('-published')[:5]
    comments = Comment.objects.all()

    context = {
        'posts': posts,
        'comments': comments,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'users_and_posts': users_and_posts,
    }

    return render(request, 'DjangoBlogApp/home.html', context)


def create_post(request):
    if request.method == "POST":
        name = request.POST.get('post_name')
        content = request.POST.get('post_content')
        img = request.POST.get('post_image')
        Post.objects.create(
        host = request.user,
        name = name,
        content = content,
        img = img
        )
    context = {}
    return render(request, 'DjangoBlogApp/create_post.html', context)


def post_details(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}

    if request.method == "POST":
        Comment.objects.create(
            author = request.user,
            post = post,
            content = request.POST.get('comment_content'),
        )
    return render(request, 'DjangoBlogApp/post_details.html', context)


def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}

    if request.method == "POST":
        pass
    return render(request, 'DjangoBlogApp/edit_post.html', context)


def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    context = {'post': post}
    return render(request, 'DjangoBlogApp/delete_post.html', context)


def profile(request, pk):
    user = User.objects.get(id=pk)
    user_profile = request.user.profile
    form = AccountForm(instance=user_profile) #fills fields with user profile data

    if request.method == "POST":
        form = AccountForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()

    context = {'user': user, 'form': form}
    return render(request, 'DjangoBlogApp/profile.html', context)


def about(request):
    context = {}
    return render(request, 'DjangoBlogApp/about.html', context)
    

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    context = {}
    return render(request, 'DjangoBlogApp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('home')
    context = {'form': form}
    return render(request, 'DjangoBlogApp/register.html', context)
