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
    users_and_posts = {}
    for user in users:
        if Post.objects.filter(host=user):
            user_posts = Post.objects.filter(host=user).count()
            users_and_posts[Post.objects.filter(host=user).first().host] = user_posts
        
    #sort users_and_posts by descending value (in result on page they are displayed in asceding order)
    users_and_posts = dict(sorted(users_and_posts.items(), key=lambda item: item[1], reverse=True))
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
        'users_and_posts': users_and_posts,
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

            if "unlike" in request.POST:
                post_to_unlike = get_object_or_404(Post, id=request.POST.get('post_id'))
                post_to_unlike.likes.remove(request.user)

            if "comment" in request.POST:
                post_to_comment = get_object_or_404(Post, id=request.POST.get('post_id'))
                content = request.POST.get('comment_content')
                Comment.objects.create(
                    post = post_to_comment,
                    author = request.user,
                    content = content
                )
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

        if "comment_content" in request.POST:
            Comment.objects.create(
                author = request.user,
                post = post,
                content = request.POST.get('comment_content'),
            )

        if "like" in request.POST:
            post_to_like = get_object_or_404(Post, id=request.POST.get('post_id'))
            post_to_like.likes.add(request.user)
        
        if "unlike" in request.POST:
                post_to_unlike = get_object_or_404(Post, id=request.POST.get('post_id'))
                post_to_unlike.likes.remove(request.user)
            
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
        
        if "unfollow" in request.POST:
            user.profile.followers.remove(request.user)
            request.user.profile.following.remove(user)

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
