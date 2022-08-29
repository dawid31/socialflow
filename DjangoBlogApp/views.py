from django.shortcuts import render
from .forms import PostForm, UserRegisterForm
from .models import *
from django.contrib.auth.models import User

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
            name=name,
            content=content
        )
    context = {}
    return render(request, 'DjangoBlogApp/create_post.html', context)


def profile(request):
    context = {}
    return render(request, 'DjangoBlogApp/profile.html', context)


def about(request):
    context = {}
    return render(request, 'DjangoBlogApp/about.html', context)
    

def login(request):
    context = {}
    return render(request, 'DjangoBlogApp/login.html', context)
    

def register(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
    context = {'form': form}
    return render(request, 'DjangoBlogApp/register.html', context)
