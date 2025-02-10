import json
from django.conf import settings
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
from App.utils.utility import *
import random
from itertools import chain
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Count
from django.core.mail import send_mail
import re
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):        
    # Cache key identifier as user username
    current_user = request.user
    
    if current_user.is_authenticated:
        all_user_likes = current_user.like_post.all()
        all_user_likes = [int(blog.id) for blog in all_user_likes]
        
        user_subscribed = subscribe_check(request)
        
        all_user_bookmarks = current_user.bookmark_post.all()
        
        # Today's pick post based on user's interaction
        blog = get_blogs_based_on_user_likes(current_user)
        all_blog_id = [int(myblog.id) for myblog in blog]
        
    else:
        no_user_auth_key = f"Today-Picks-{current_user}"
        blog = Blog.objects.all().order_by('?')[:11]
        blog_data = cache.get(no_user_auth_key)
        # blog = Blog.objects.select_related('likes', 'bookmarks').all().order_by('?')[:11]
        
        now = datetime.now()
        end_of_day = datetime.combine(now.date(), datetime.max.time())
        seconds_until_end_of_day = (end_of_day - now).seconds
        
        if not blog_data:
            serialized_blog_data  = serializers.serialize('json', blog)
            
            # Cache the image data list until the end of the day
            cache.set(no_user_auth_key, serialized_blog_data, timeout=seconds_until_end_of_day)
            
            # Custom function to deserialize serialized data
            blog = deserial(serialized_blog_data)
        else:
            # Custom function to deserialize serialized data
            cached_blog_cnts = deserial(blog_data)
            cached_blog_ids = [blog.id for blog in cached_blog_cnts]
            
            all_blogs = list(Blog.objects.all())
            
            existing_cached_blogs = list(Blog.objects.filter(id__in=cached_blog_ids))
            serialized_blog_data  = serializers.serialize('json', existing_cached_blogs)
            cache.set(no_user_auth_key, serialized_blog_data)
            blog = deserial(blog_data)
            
            # # Check if all cached contents are a subset of all blog instances
            # if set(cached_blog_cnts).issubset(set(all_blogs)):
            #     for cached_blog in cached_blog_cnts:
            #         db_blog = Blog.objects.get(id=cached_blog.id)
            #         # print(db_blog.shares_count)
            #         # print(cached_blog.shares_count)
            #         if cached_blog.shares_count != db_blog.shares_count:
            #             print(True)
            #             # Update the cached blog if it doesn't match the database instance                        
            #             cache.set(no_user_auth_key, serialized_blog_data)
                        
            #     blog = deserial(blog_data)
            # else:
            #     blog = deserial(blog_data)
        
    # Category post instance
    all_categ = Category.objects.all()
    
    # Randomize database query results
    all_categ_articles = Category.objects.order_by('?')
    
    # To test for query outputs if cached or not
    # cache.clear() 
    topics_cache_key = f"Hot--Topics--{current_user}"
    # Retrieves the value from the cache assigned with the custom key.
    images_data = cache.get(topics_cache_key)
    
    # If executes if images_data returns none
    if not images_data:
        serialized_data  = serializers.serialize('json', all_categ_articles)
        
        # Cache the image data list for 2 hours
        cache.set(topics_cache_key, serialized_data , timeout = 7200)
        
        # Custom function to deserialize serialized data
        images_data = deserial(serialized_data)
        random.shuffle(images_data)
        
    else:
        # Condtion runs when cache is created
        # Custom function to deserialize serialized data
        images_data = deserial(images_data)
        random.shuffle(images_data)
    
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
    
    user_subscribed = subscribe_check(request)
    
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
        username = request.POST.get('username').strip().title()
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        
        userexists = User.objects.filter(username=username).exists()
        emailexists = User.objects.filter(email=email).exists()
        
        try:
            if password != confirm_password:
                return JsonResponse({'password': True, 'message': 'Passwords does not match'})
            
            elif userexists:
                return JsonResponse({'userexists': True, 'message': 'Username is taken'})
            
            elif emailexists:
                return JsonResponse({'emailexists': True, 'message': 'Email is taken'})
            
            else:
                user = User.objects.create_user(
                        username=username,
                        email=email,
                )
                user.set_password(password)
                user.save()
                Newsletter.objects.create(user=user, subscribe=False)
                
                return JsonResponse({'success': True, 'message': 'Registration successful', 'redirect_url': reverse('login')})
            
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            return JsonResponse({'exceptionError': True, 'message': 'Exception error'})
        
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
        # data = request.body
        # Ajax_data = json.loads(data.decode('utf-8'))
        
        username = request.POST.get('username').strip().title()
        password = request.POST.get('password').strip()
        
        user_check = User.objects.filter(username=username).exists()
        if user_check:
            usid = user_check
        else:
            return JsonResponse({'userError': True, 'message': 'Username or Password is incorrect'})
        
        try:
            user = authenticate(request, username=username, password=password)
            
            if user.is_authenticated:
                login(request, user)
                
                post_slug = request.session.get('post_slug')
                cat_name = request.session.get('cat_name')
                
                if post_slug and cat_name:
                    url = reverse('postpage', kwargs={'name': cat_name, 'slug': post_slug})
                    return JsonResponse({'successpostpage': True, 'message': 'Login successful', 'redirect_url': url})
                    # return redirect(url)
                
                    # response = postpage(request, name=cat_name, slug=post_slug)
                    # request.session.flush()
                    # return response
                
                # return JsonResponse({'success': True, 'message': 'Login successful'})
                return JsonResponse({'success': True, 'message': 'Login successful', 'redirect_url': reverse('home')})
            
            else:
                return JsonResponse({'passworderror': True, 'message': 'Username or Password is incorrect'})
        
        except Exception as e:
            # return HttpResponse(str(e))
            return JsonResponse({'exceptionError': True, 'message': 'Username or Password is incorrect'})
        
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
                
    user_subscribed = subscribe_check(request)
    
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
    
    user_subscribed = subscribe_check(request)
    
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
        
    user_subscribed = subscribe_check(request)
    
    return render(request, 'postpage.html', locals())

def profile(request):
    user_subscribed = subscribe_check(request)
    try:
        user = request.user
        all_user_likes = user.like_post.all()
        
        return render(request , 'profile.html', locals())
    except:
        return redirect('home')
    
def verify(request):
    all_categ = Category.objects.all()
    try:
        if request.method == 'POST':
            
            email = request.POST.get('email')
            user = User.objects.filter(email=email).first()

            if user:
                token = PasswordResetToken.objects.create(user=user)
                reset_link = request.build_absolute_uri(reverse('reset-password', kwargs={'token': str(token.token)}))

                send_mail(
                    subject='Password Reset Link',
                    message=f'Click the link to reset your password(Link will expire in 15minutes\n{reset_link}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )

                return JsonResponse({'success': True, 'message': 'Password reset link sent to {email}'})
            else:
                return JsonResponse({'fail': True, 'message': 'Mail is not available'})
        
        return render(request, 'verify.html', locals())
        
    except Exception as e:
        # logger.error(f"Exception occurred: {e}")
        return JsonResponse({'error': True, 'message': f'An error occurred: {e}'})

def reset_password(request, token):
    all_categ = Category.objects.all()
    
    if request.method == "POST":
        return redirect('home')
        password = request.POST.get('password')
        print(password)
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            return JsonResponse({'password': True, 'message': 'Passwords does not match'})
        
        try:
            token = PasswordResetToken.objects.get(token=token)
            if token.is_valid():
                user = token.user
                user.set_password(password)
                user.save()
                token.delete()
                return JsonResponse({'success': True, 'message': 'Password reset successful', 'redirect_url': reverse('login')})
            else:
                return JsonResponse({'fail': True, 'message': 'Token link has expired'})
        except:
            return JsonResponse({'fail': True, 'message': 'Invalid requqest, try again.'})
    
    return render(request, 'passreset.html', locals())