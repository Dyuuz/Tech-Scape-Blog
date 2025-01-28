import json
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from datetime import datetime
from django.core.cache import cache
from django import template
from django.urls import reverse
from .models import *
import random
from itertools import chain
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Count
import re

# Create your views here.
def home(request):        
    user = request.user
    if user.is_authenticated:
        all_user_likes = user.like_post.all()
        all_user_likes = [int(blog.id) for blog in all_user_likes]
        
        user_subscribed = Newsletter.objects.get(user=user)
        user_subscribed = True if user_subscribed and user_subscribed.subscribe else False
        
        all_user_bookmarks = user.bookmark_post.all()
        
        # Today's pick post based on user's interaction
        blog = get_blogs_based_on_user_likes(user)
        all_blog_id = [int(myblog.id) for myblog in blog]
    else:
        blog = Blog.objects.all().order_by('?')[:11]

        
    # Category post instance
    all_categ = Category.objects.all()
    
    # Randomize database query results
    all_categ_articles = Category.objects.order_by('?')
    current_user = request.user
    
    # Cache key identifier as user username
    cache_key = f"{current_user}"
    
    # To test for query outputs if cached or not
    # cache.clear() 
    
    # Retrieves the value from the cache assigned with the custom key.
    images_data = cache.get(cache_key)
    
    # If executes if images_data returns none
    if not images_data:
        serialized_data  = serializers.serialize('json', all_categ_articles)
        
        # Cache the image data list for 2 hours
        cache.set(cache_key, serialized_data , timeout = 7200)
        
        # Custom function to deserialize serialized data
        images_data = deserial(serialized_data)
        random.shuffle(images_data)
        print(f"Not: {images_data}") 
        
    else:
        # Condtion runs when cache is created
        # Custom function to deserialize serialized data
        images_data = deserial(images_data)
        random.shuffle(images_data)
        print(f"True: {images_data}")  # Output after deserializing
    
    # Popular post blog instance
    popular_cat = Blog.objects.all().order_by('-views_count')[:10]
    
    # Most liked post blog instance
    post_likes = Blog.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes')[:10]
    
    # Recent post blog instance
    blog_mod = Blog.objects.all().order_by('-time')[:8]
    for mod in blog_mod:
        target_date_str = f"{mod.time}"
        target = target_date_str.split('+')[0]
        
        # Convert the string to a datetime object using strptime
        target_date = datetime.strptime(target, '%Y-%m-%d %H:%M:%S.%f')
        current_date = datetime.now()

        time_difference = current_date - target_date

        # Get the total hours difference (total_seconds() / 3600)
        hours_difference = time_difference.total_seconds() / 60
        time_diff = hours_difference - 60
        mod.time = f"{time_diff:.0f}"
        mod.time = int(mod.time)
        
    return render(request, 'index.html', locals())

# Query recently uploaded record from DB
def recentposts(request):
    user = request.user
    if user.is_authenticated:
        all_user_likes = user.like_post.all()
        all_user_likes = [int(blog.id) for blog in all_user_likes]
    all_categ = Category.objects.all()
    recentpost = Blog.objects.all().order_by('-time')
    
    cache_key = f"category_images_recentposts"
    
    # Try to get the list of images from cache
    images_data_recent = cache.get(cache_key)
    
    if not images_data_recent:
        # If it is not cached, fetch images from the database
        images_data_recent = recentpost
        
        # Cache the image data list for 1 hour
        cache.set(cache_key, images_data_recent, timeout=1000)
    
    paginator = Paginator(recentpost, 5)
    
    # Get the current page number from the URL query parameters
    page_number = request.GET.get('page')
    
    # Retrieve the relevant page of results
    page_obj = paginator.get_page(page_number)
    
    current_page = page_obj.number
    total_pages = paginator.num_pages
    start_range = max(1, current_page - 2)  
    end_range = min(total_pages, current_page + 2)  
    page_range = range(start_range, end_range + 1) 
    
    show_ellipsis = total_pages - current_page
     
    for mod in page_obj :
        target_date_str = f"{mod.time}"
        print(target_date_str)
        target = target_date_str.split('+')[0]
        
        # Convert the string to a datetime object using strptime
        target_date = datetime.strptime(target, '%Y-%m-%d %H:%M:%S.%f')
        current_date = datetime.now()

        time_difference = current_date - target_date

        # Get the total hours difference (total_seconds() / 3600)
        hours_difference = time_difference.total_seconds() / 60
        time_diff = hours_difference - 60
        mod.time = f"{time_diff:.0f}"
        mod.time = int(mod.time)
    return render (request , 'recent.html', locals())

# Create operation for new users
def register(request):
    all_categ = Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create_user(
                username=username,
                email=email,
                )
            user.set_password(password)
            user.save()
            Newsletter.objects.create(user=user, subscribe=False)
            return redirect('login')
        else:
            return HttpResponse("Passwords are incorrect")
            return render(request, 'register.html', locals())
        
    else:
        return render(request, 'register.html', locals())

# Creates session when user tries to interact with a blog post if no user is authenticated
def loginsession(request, name, slug):
    request.session.flush() # Clear existing data in session
    request.session['post_slug'] = slug
    request.session['cat_name'] = name
    return redirect("login")

# Read operation for existing users 
def login_view(request):
    all_categ = Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=username, password=password)
            
            if user.is_authenticated:
                login(request, user)
                post_slug = request.session.get('post_slug')
                cat_name = request.session.get('cat_name')
                
                if post_slug and cat_name:
                    url = reverse('postpage', kwargs={'name': cat_name, 'slug': post_slug})
                    return redirect(url)
                
                    response = postpage(request, name=cat_name, slug=post_slug)
                    # request.session.flush()
                    return response
                    
                return redirect('home')
            
            else:
                return HttpResponse("Invalid password")
        
        except Exception as e:
            return HttpResponse(str(e))
            # return render(request, 'login.html', locals())
        
    else:
        return render(request, 'login.html', locals())

# Sign out user method
def logout_view(request):
    logout(request)
    return redirect('login')

def category(request, cat):
    category = Category.objects.get(name = cat)
    blog = Blog.objects.filter(category = category)
    all_categ = Category.objects.all()
    return render(request, 'category.html', locals())

# Categorize blog posts according to their division 
def categories(request):
    user = request.user
    if user.is_authenticated:
        all_user_likes = user.like_post.all()
        all_user_likes = [int(blog.id) for blog in all_user_likes]
    categories = Category.objects.prefetch_related('posts').all()
    all_categ = Category.objects.all()
    for category in categories:
            category.limited_posts = category.posts.all().order_by('-time')[:5]
            for mod in category.limited_posts:
                target_date_str = f"{mod.time}"
                target = target_date_str.split('+')[0]
                
                # Convert the string to a datetime object using strptime
                target_date = datetime.strptime(target, '%Y-%m-%d %H:%M:%S.%f')
                current_date = datetime.now()

                time_difference = current_date - target_date

                # Get the total hours difference (total_seconds() / 3600)
                hours_difference = time_difference.total_seconds() / 60
                time_diff = hours_difference - 60
                mod.time = f"{time_diff:.0f}"
                mod.time = int(mod.time)
    return render(request, 'categories.html', locals())

# Displays all blog posts in a category 
def category_detail(request, name):
    user = request.user
    if user.is_authenticated:
        all_user_likes = user.like_post.all()
        all_user_likes = [int(blog.id) for blog in all_user_likes]
    category = get_object_or_404(Category, name=name)
    blog_posts = category.posts.all().order_by('-time')
    all_categ = Category.objects.all()
    
    # blog_posts = Blog.objects.all()
    
    # Create a Paginator object (5 posts per page)
    paginator = Paginator(blog_posts, 5)
    
    # Get the current page number from the URL query parameters
    page_number = request.GET.get('page')
    
    # Retrieve the relevant page of results
    page_obj = paginator.get_page(page_number)
    
    current_page = page_obj.number
    total_pages = paginator.num_pages
    start_range = max(1, current_page - 1)  # Start 4 pages before current page
    end_range = min(total_pages, current_page + 1)  # End 4 pages after current page
    page_range = range(start_range, end_range + 1)  # Include the end range
    
    show_ellipsis = total_pages - current_page 
    
    return render(request, 'category_detail.html', locals())

# Displays a blog post full content
def postpage(request, name, slug):
    blog = Blog.objects.get(slug=slug)
    if request.user:
        blog = blog
    else:
        blog = blog.body[:72]
        
    name = Category.objects.get(name=name)
    all_categ = Category.objects.all()
    
    category = get_object_or_404(Category, name=name)
    blog_postpage = category.posts.all().order_by('?').exclude(slug=slug)[:3]
    
    # Check if the post has already been viewed in this session
    session_key = f'viewed_post_{slug}'
    if not request.session.get(session_key):
        blog.views_count += 1  # Increment the view count
        blog.save()
        request.session[session_key] = True
        
    user = request.user
    if user.is_authenticated:
        is_liked = blog in user.like_post.all()
        is_bookmarked = blog in user.bookmark_post.all()
        # all = user.like_post.all()
    
    return render(request, 'postpage.html', locals())

# Pending 
def comment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        pk = request.POST.get('pk')
        pk = int(pk)
        blog = Blog.objects.get(pk=pk)
        
        protocol = Comments(name=name, comment=comment,category=blog)
        return HttpResponse("Comment saved!")
    return HttpResponse("Error Loading page")

# Caching operation of converting serialized data to a default data structure 
def deserial(data):
    # Function to deserialize data if serialized data is cached
    images_data = serializers.deserialize('json', data)
    
    # Extract the model instances to a list from images_data json structure
    images_data = [obj.object for obj in images_data] 
    # print(f" data {images_data}")
    return images_data

# Ajax request to update user's interaction on a blog's like feature 
def update_like(request):
    """
    Function to update user like feature directly with ajax request 
    """
    if request.method == "POST":
        data = request.body
        Ajax_data = json.loads(data.decode('utf-8'))
        user = request.user
        post_id = int(Ajax_data.get('post_id'))
        buttonBoolean = Ajax_data.get('buttonBoolean')
        likeBoolean = Ajax_data.get('likeBoolean')
        # print(buttonBoolean)
        # print(user.like_post.all())
        # print(user.bookmark_post.all())
        blog = Blog.objects.get(id=post_id)
        
        if buttonBoolean == "true":
            blog.likes.add(user)
            blog.save()
            return JsonResponse({'success': True, 'message': 'Post liked successfully!'})
        else:
            blog.likes.remove(user)
            blog.save()
            return JsonResponse({'success': True, 'message': 'Post unliked successfully!'})

# Ajax request to update user's interaction on a blog's bookmark feature 
def update_bookmark(request):
    """
    Logic script to update user bookmark feature directly with ajax request 
    """
    if request.method == "POST":
        data = request.body
        Ajax_data = json.loads(data.decode('utf-8'))
        user = request.user
        post_id = int(Ajax_data.get('post_id'))
        buttonBoolean = Ajax_data.get('buttonBoolean')
        blog = Blog.objects.get(id=post_id)
        
        if buttonBoolean == "true":
            blog.bookmarks.add(user)
            blog.save()
            return JsonResponse({'success': True, 'message': 'Post bookmarked successfully!'})
        else:
            blog.bookmarks.remove(user)
            blog.save()
            return JsonResponse({'success': True, 'message': 'Post unbookmarked successfully!'})

def profile(request):
    try:
        user = request.user
        all_user_likes = user.like_post.all()
        return render(request , 'profile.html', locals())
    except:
        return redirect('home')

def get_blogs_based_on_user_likes(user):
    # Step 1: Get the user's top 3 most liked categories
    top_categories = (
        Category.objects.filter(posts__likes=user)  # Filter categories where user liked blogs
        .annotate(like_count=Count('posts__likes'))  # Count likes in each category
        .order_by('-like_count')  # Sort by most liked categories
        .values_list('id', flat=True)[:4]  # Get IDs of the top 4 categories
    )

    # Step 2: Fetch blog posts, picking 3 posts from each top category
    blogs = []
    for category_id in top_categories:
        category_blogs = Blog.objects.filter(category_id=category_id).order_by('-time')[:3]  # Get latest 3 posts
        blogs.append(category_blogs)

    # Flatten the list of QuerySets into a single list
    final_blog_list = list(chain(*blogs))

    # Step 3: If less than 11 posts, fill remaining spots with random blog posts from other categories
    if len(final_blog_list) < 11:
        remaining_count = 11 - len(final_blog_list)
        
        # Get random blog posts not in the user's top categories
        additional_blogs = Blog.objects.exclude(category_id__in=top_categories).order_by('?')[:remaining_count]
        
        # Combine both lists
        final_blog_list.extend(additional_blogs)

    return final_blog_list[:11]  # Ensure it returns exactly 11 posts

def update_subscribe(request):
    if request.method == "POST":
        data = request.body
        Ajax_data = json.loads(data.decode('utf-8'))
        emailVal = Ajax_data.get('emailVal')
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, emailVal):
            return JsonResponse({'success': False, 'message': 'Invalid email format!'})
        else:
            try:
                user = request.user
                if user:
                    subscribe = Newsletter.objects.get(user=user)
                    subscribe.subscribe = True
                    subscribe.email = emailVal
                    subscribe.save()
                    return JsonResponse({'success': True, 'message': 'Subscribed successfully!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Sign in to subscribe!'})
            except:
                return JsonResponse({'success': False, 'message': 'Sign in to subscribe!'})