import json
from django.shortcuts import render,redirect, get_object_or_404
from django.core import serializers
from datetime import datetime
from django.core.cache import cache
from django import template
from django.urls import reverse
from requests import request
from django.http import JsonResponse, HttpResponse
from App.models import *
import random
from itertools import chain
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Count
import re

# Function scripts
def subscribe_check(request):
    try:
        current_user = request.user if request.user.is_authenticated else None
        user_subscribed = Newsletter.objects.get(user=current_user)
        user_subscribed = True if user_subscribed and user_subscribed.subscribe else False
        return user_subscribed
    except:
        return False

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
                print(user.is_authenticated)                
                if user.is_authenticated and user.email != emailVal:
                    return JsonResponse({'success': False, 'message': 'Email is not associated with this account!'})
                
                elif not Newsletter.objects.filter(email=emailVal).exists():
                    return JsonResponse({'success': False, 'message': 'Email is not on subscribtion list. Send us a mail to fix the issue.'})
                
                elif user.is_authenticated:
                    subscribe = Newsletter.objects.get(user=user)
                    subscribe.subscribe = True
                    subscribe.email = emailVal
                    subscribe.save()
                    return JsonResponse({'success': True, 'message': 'Subscribed successfully!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Sign in to subscribe!'})
            except:
                return JsonResponse({'success': False, 'message': 'Sign in to subscribe!'})
            
def update_shares(request):
    """
    Logic script to update blog shares count feature directly with ajax request 
    """
    if request.method == "POST":
        data = request.body
        Ajax_data = json.loads(data.decode('utf-8'))
        post_id = int(Ajax_data.get('post_id'))
        blog = Blog.objects.get(id=post_id)
        user = request.user
        
        session_share_key = f'viewed_post_{post_id}_'
        if not request.session.get(session_share_key):
            request.session[session_share_key] = True
            if blog:
                blog.shares_count += 1
                blog.save()
                return JsonResponse({'success': True, 'message': 'Blog count updated successfully!'})
            
        else:
            return JsonResponse({'success': False, 'message': 'Too many requests!'})

def update_suboption(request):
    """
    Logic script to update user subscription option directly with ajax request 
    """
    if request.method == "POST":
        data = request.body
        Ajax_data = json.loads(data.decode('utf-8'))
        user = request.user
        suboption = Ajax_data.get('suboption').lower()
    
        try:
            subscribe = Newsletter.objects.get(user=user)
            subscribe.subscribe = True if suboption == 'subscribe' else False
            subscribe.save()
            print(suboption)
            if suboption == 'subscribe':
                return JsonResponse({'subscribe': True, 'message': 'You have successfully subscribed'})
            else:
                return JsonResponse({'unsubscribe': True, 'message': 'You have successfully unsubscribed'})
        except:
            return JsonResponse({'success': False, 'message': 'Error updating subscription option!'})
        
html_content = """
    <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .email-container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    background-color: #3498db;
                    color: #ffffff;
                    padding: 20px;
                    border-radius: 8px 8px 0 0;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .body {{
                    padding: 20px;
                    color: #333;
                }}
                .body p {{
                    font-size: 16px;
                    line-height: 1.6;
                }}
                .btn {{
                    display: inline-block;
                    padding: 12px 20px;
                    margin: 20px 0;
                    background-color: #3498db;
                    color: #ffffff;
                    text-decoration: none;
                    font-size: 18px;
                    border-radius: 5px;
                    text-align: center;
                    transition: background-color 0.3s ease;
                }}
                .btn:hover {{
                    background-color: #2980b9;
                }}
                .footer {{
                    text-align: center;
                    font-size: 14px;
                    color: #7f8c8d;
                    margin-top: 20px;
                }}
                .footer a {{
                    color: #3498db;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Welcome to Your App Name!</h1>
                </div>
                <div class="body">
                    <p>Hello,</p>
                    <p>Thank you for registering with us! Please click the button below to verify your email address and complete your registration process.</p>
                    <a href="{verification_url}" class="btn">Verify My Email</a>
                    <p>If you did not create an account, please ignore this message.</p>
                </div>
                <div class="footer">
                    <p>Best regards,</p>
                    <p>Your App Name Team</p>
                    <p><a href="https://yourwebsite.com">Visit our website</a></p>
                </div>
            </div>
        </body>
    </html>
"""