from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, PostForm, ProfileForm, CommentForm
from .models import Post, Profile, Like, Comment, Follow


# ─── HOME ────────────────────────────────────────────
def home_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'social/home.html')


# ─── REGISTER ────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to MiniSocial, {user.username}!')
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'social/register.html', {'form': form})


# ─── LOGIN ───────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('feed')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'social/login.html')


# ─── LOGOUT ──────────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ─── FEED ────────────────────────────────────────────
@login_required(login_url='login')
def feed_view(request):
    posts = Post.objects.all().select_related('author', 'author__profile')
    liked_posts = Like.objects.filter(
        user=request.user
    ).values_list('post_id', flat=True)
    comment_form = CommentForm()
    return render(request, 'social/feed.html', {
        'posts': posts,
        'liked_posts': liked_posts,
        'comment_form': comment_form,
    })


# ─── CREATE POST ─────────────────────────────────────
@login_required(login_url='login')
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post shared successfully!')
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'social/create_post.html', {'form': form})


# ─── LIKE / UNLIKE ───────────────────────────────────
@login_required(login_url='login')
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


# ─── ADD COMMENT ─────────────────────────────────────
@login_required(login_url='login')
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


# ─── PROFILE ─────────────────────────────────────────
@login_required(login_url='login')
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    posts = Post.objects.filter(author=profile_user)
    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()
    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'followers_count': profile.get_followers_count(),
        'following_count': profile.get_following_count(),
        'posts_count': profile.get_posts_count(),
    })


# ─── EDIT PROFILE ────────────────────────────────────
@login_required(login_url='login')
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'social/edit_profile.html', {'form': form})


# ─── FOLLOW / UNFOLLOW ───────────────────────────────
@login_required(login_url='login')
def follow_view(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )
        if not created:
            follow.delete()
    return redirect('profile', username=username)
