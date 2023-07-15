import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Post


def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-date")

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts_pag = paginator.page(page)
    except PageNotAnInteger:
        posts_pag = paginator.page(1)
    except EmptyPage:
        posts_pag = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        liked_posts = request.user.likes_users.all()
    else:
        liked_posts = []

    return render(request, "network/index.html", {
        "posts": posts_pag,
        "liked_posts": liked_posts
    })


def profile(request, name):
    user = User.objects.get(username=name)
    followers = user.followers.count()
    following = user.following.count()

    posts = Post.objects.filter(author=user.id)
    posts = posts.order_by('-date')

    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    try:
        posts_pag = paginator.page(page)
    except PageNotAnInteger:
        posts_pag = paginator.page(1)
    except EmptyPage:
        posts_pag = paginator.page(paginator.num_pages)


    return render(request, 'network/profile.html', {
            'username': user,
            'followers_count': followers,
            'following_count': following,
            'posts': posts_pag,
        })

@login_required
def fol_posts(request):
    user = request.user

    posts = []
    for user in request.user.following.all():
        all_posts = Post.objects.filter(author = user)
        for post in all_posts:
            posts.append(post.serialize())

    posts = sorted(posts, key= lambda k: k['id'], reverse= True)

    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    try:
        posts_pag = paginator.page(page)
    except PageNotAnInteger:
        posts_pag = paginator.page(1)
    except EmptyPage:
        posts_pag = paginator.page(paginator.num_pages)

    return render(request, 'network/fol_posts.html', {
            "posts": posts_pag,
            'username': user,
        })


@csrf_exempt
@login_required
def compose_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    body_post = json.loads(request.body)
    text = body_post.get("subject", "")

    post = Post(
        author=request.user,
        text=text
    )
    post.save()

    return JsonResponse({"message": "Post saved successfully."}, status=201)

@csrf_exempt
@login_required
def follow(request, name):
    receiver = User.objects.get(username = name)

    if request.method == 'PUT':
        is_follow = json.loads(request.body)
        if is_follow.get('follow'):
            follow_set = receiver.followers
            follow_set.add(request.user)
            receiver.save()

            follower = request.user
            follower.following.add(receiver)
            follower.save()
            return JsonResponse({'status': 'success'}, status=204)
        else:
            follow_set = receiver.followers
            follower_inst = receiver.followers.get(pk=request.user.id)
            follow_set.remove(follower_inst)
            receiver.save()

            follower = request.user
            following_set = follower.following
            following_inst = follower.following.get(username=name)
            following_set.remove(following_inst)
            follower.save()
            return HttpResponse(status=204)
    else:
        return JsonResponse({'error': 'Invalid request method, use PUT'})

def is_follow(request, name):
    user = request.user
    profile = User.objects.get(username = name)
    if user in profile.followers.all():
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})

def count(request, name):
    profile = User.objects.get(username = name)
    return JsonResponse(
        {
            'followers': profile.followers.count(),
            'following': profile.following.count()
        }
    )

@csrf_exempt
@login_required
def edited_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = Post.objects.get(pk = post_id)
        post_data = json.loads(request.body)
        post_text = post_data.get('update_post_content')
        post.text = post_text
        post.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@login_required
def likes(request, post_id):
    data = json.loads(request.body)
    post = Post.objects.get(pk=post_id)
    user = request.user

    if request.method == 'POST':
        if data.get('like'):
            post.likes.add(user)
            post.save()
            return HttpResponse(status=200)

        else:
            post.likes.remove(post.likes.get(pk=user.id))
            post.save()
            return HttpResponse(status=200)
    else:
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
