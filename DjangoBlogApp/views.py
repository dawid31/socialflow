from django.shortcuts import render, redirect

from .forms import PostForm, CustomUserCreationForm
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'DjangoBlogApp/home.html', context)


def create_post(request):
    if request.method == "POST":
        name = request.POST.get('post_name')
        content = request.POST.get('post_content')
        Post.objects.create(
            user = request.user,
            name = name,
            content = content,
        )
    context = {}
    return render(request, 'DjangoBlogApp/create_post.html', context)


def profile(request):
    context = {}
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
