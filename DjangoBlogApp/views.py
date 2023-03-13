from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomUserCreationForm, AccountForm, PostForm
from .models import *

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    users = User.objects.all()
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    logged_in_users = []
    for session in active_sessions:
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if user_id is not None:
            logged_in_users.append(User.objects.get(pk=user_id))

    profiles = Profile.objects.all()
    user_points = {}
    for profile in profiles:
        user = profile.user
        points = profile.points
        user_points[user] = points

    #sort users_and_posts by descending value (in result on page they are displayed in asceding order)
    user_points = dict(sorted(user_points.items(), key=lambda item: item[1], reverse=True))
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(name__icontains=q) |
        Q(content__icontains=q) |
        Q(host__username__icontains=q)
    )

    #Setting up paginator (what do we want to paginate and how many objects per page)
    p = Paginator(Post.objects.all(), 3)
    page = request.GET.get('page')
    paginated_posts = p.get_page(page)
    if request.user.is_authenticated:
        followed_people = request.user.profile.following.all()
        followed_posts = Post.objects.filter(host__in=followed_people).all()
    else:
        followed_posts = None

    
                
                
    recent_comments = Comment.objects.all().order_by('-published')[:5]
    comments = Comment.objects.all()

    context = {
        'posts': posts,
        'paginated_posts': paginated_posts,
        'comments': comments,
        'recent_comments': recent_comments,
        'user_points': user_points,
        'logged_in_users': list(dict.fromkeys(logged_in_users)),
        'logged_in_user_count': len(list(dict.fromkeys(logged_in_users))),
        'followed_posts': followed_posts,
    }

    if request.method == "POST":
        @login_required
        def handle_post(request):

            if "like" in request.POST:
                post_to_like = get_object_or_404(Post, id=request.POST.get('post_id'))
                post_to_like.likes.add(request.user)
                post_to_like.host.profile.points += 3
                post_to_like.host.profile.save()

            if "unlike" in request.POST:
                post_to_unlike = get_object_or_404(Post, id=request.POST.get('post_id'))
                post_to_unlike.likes.remove(request.user)
                post_to_unlike.host.profile.points -= 3
                post_to_unlike.host.profile.save()

            if "comment" in request.POST:
                post_to_comment = get_object_or_404(Post, id=request.POST.get('post_id'))
                content = request.POST.get('comment_content')
                Comment.objects.create(
                    post = post_to_comment,
                    author = request.user,
                    content = content
                )
                post_to_comment.host.profile.points += 5
                post_to_comment.host.profile.save()


            return render(request, 'DjangoBlogApp/home.html', context)

        return handle_post(request)

    return render(request, 'DjangoBlogApp/home.html', context)


def create_post(request):
    if request.method == "POST":
        name = request.POST.get('post_name')
        content = request.POST.get('post_content')
        img = request.FILES.get('post_image')
        Post.objects.create(
        host = request.user,
        name = name,
        content = content,
        img = img,
        )
        return redirect('home')
    context = {}
    return render(request, 'DjangoBlogApp/create_post.html', context)

@login_required
def post_details(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        if "comment" in request.POST:
                post_to_comment = get_object_or_404(Post, id=request.POST.get('post_id'))
                content = request.POST.get('comment_content')
                Comment.objects.create(
                    post = post_to_comment,
                    author = request.user,
                    content = content
                )
                post_to_comment.host.profile.points += 5
                post_to_comment.host.profile.save()
        
        if "like" in request.POST:
            post_to_like = get_object_or_404(Post, id=request.POST.get('post_id'))
            post_to_like.likes.add(request.user)

            post_to_like.host.profile.points += 3
            post_to_like.host.profile.save()

        if "unlike" in request.POST:
            post_to_unlike = get_object_or_404(Post, id=request.POST.get('post_id'))
            post_to_unlike.likes.remove(request.user)

            post_to_unlike.host.profile.points -= 3
            post_to_unlike.host.profile.save()


    context = {'post': post}
    return render(request, 'DjangoBlogApp/post_details.html', context)


def edit_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        post.name = request.POST.get('post_name')
        post.content = request.POST.get('post_content')
        post.img = request.FILES.get('post_image')
        post.save()
    
    context = {'post': post}
    return render(request, 'DjangoBlogApp/edit_post.html', context)


def delete_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        post.delete()
        post.host.profile.points -= 5
        post.host.profile.save()
        return redirect('home')

    context = {'post': post}
    return render(request, 'DjangoBlogApp/delete_post.html', context)


def edit_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.method == "POST":
        content = request.POST.get('comment_content')
        comment.content = content
        comment.save()
        return redirect('home')

    context = {'comment': comment}
    return render(request, 'DjangoBlogApp/edit_comment.html', context)


def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.method == "POST":
        comment.delete()
        comment.post.host.profile.points -= 5
        comment.post.host.profile.save()
        return redirect('home')

    context = {'comment': comment}
    return render(request, 'DjangoBlogApp/delete_comment.html', context)

@login_required
def profile(request, pk):
    user = User.objects.get(id=pk)
    user_profile = request.user.profile
    form = AccountForm(instance=user_profile) #fills fields with user profile data

    if request.method == "POST":
        if "account_form" in request.POST:
            form = AccountForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
        
        if "follow" in request.POST:
            user.profile.followers.add(request.user)
            request.user.profile.following.add(user)
            user.profile.points += 8
            user.profile.save()
        
        if "unfollow" in request.POST:
            user.profile.followers.remove(request.user)
            request.user.profile.following.remove(user)
            user.profile.points -= 8
            user.profile.save()


    context = {'user': user, 'form': form}
    return render(request, 'DjangoBlogApp/profile.html', context)


def followers(request, pk):
    user = User.objects.get(id=pk)
    followers = user.profile.followers.all()
    context = {'followers': followers}
    return render(request, 'DjangoBlogApp/followers.html', context)


def following(request, pk):
    user = User.objects.get(id=pk)
    following = user.profile.following.all()
    context = {'following': following}
    return render(request, 'DjangoBlogApp/following.html', context)


def about(request):
    context = {}
    return render(request, 'DjangoBlogApp/about.html', context)
    

def loginUser(request):
    next_page = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error appeared during your login attempt.')
    context = {}
    return render(request, 'DjangoBlogApp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def leaderboard_info(request):
    context = {}
    return render (request, 'DjangoBlogApp/leaderboard_info.html')

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
                messages.success(request, "Your account was created successfully")
                return redirect('home')

    context = {'form': form}
    return render(request, 'DjangoBlogApp/register.html', context)
