from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm
from .models import *

from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(
        Q(name__icontains=q) |
        Q(content__icontains=q) |
        Q(host__username__icontains=q)
    )
    comments = Comment.objects.all()
    context = {'posts': posts, 'comments': comments}
    return render(request, 'DjangoBlogApp/home.html', context)


def create_post(request):
    if request.method == "POST":
        name = request.POST.get('post_name')
        content = request.POST.get('post_content')
        Post.objects.create(
            host = request.user,
            name = name,
            content = content,
        )
    context = {}
    return render(request, 'DjangoBlogApp/create_post.html', context)


def post_details(request):
    return render(request, 'DjangoBlogApp/post_details.html')


def create_comment(request):
    return render(request, 'DjangoBlogApp/create-comment.html')


def profile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
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
