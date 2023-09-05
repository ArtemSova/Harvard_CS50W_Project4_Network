from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import *

# Новые функции регистрируй в urls.py

# Количество постов на странице для пагинации
posts_per_page = 5

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Changes Successful", "data": data["content"]})

def index(request):
    # Получаем все посты в обратном порядке
    allPosts = Post.objects.all().order_by("id").reverse()

    # Пагинация
    paginator = Paginator(allPosts, posts_per_page)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_posts": page_posts,
    })


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

def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    # Получаем все посты пользователя
    allPosts = Post.objects.filter(user=user).order_by("id").reverse()
    # Фоловеры пользователя
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)

    try:
        checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False


    # Пагинация
    paginator = Paginator(allPosts, posts_per_page)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    # Данные, отправляемые в html
    return render(request, "network/profile.html", {
        "allPosts": allPosts,
        "page_posts": page_posts,
        "username": user.username,
        "following": following,
        "followers": followers,
        "my_profile": user,
        "isFollowing": isFollowing
    })

def follow(request):
    userfollow = request.POST["userfollow"]
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow(user=currentUser, user_follower=userfollowData)
    f.save()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request):
    userfollow = request.POST["userfollow"]
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=currentUser, user_follower=userfollowData)
    f.delete()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    following_users = Follow.objects.filter(user=currentUser)
    allPosts = Post.objects.all().order_by("id").reverse()

    following_posts = []
    for post in allPosts:
        for fuser in following_users:
            if fuser.user_follower == post.user:
                following_posts.append(post)

    paginator = Paginator(following_posts, posts_per_page)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    a_f_posts = len(following_posts)

    return render(request, "network/following.html", {
        "page_posts": page_posts,
        "a_f_posts": a_f_posts
        })

def like(request, pk):

    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse("index"))





