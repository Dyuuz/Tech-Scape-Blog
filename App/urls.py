from App import admin
from Blog.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home , name = 'home'),
    path('login', views.login_view, name = 'login'),
    path('logout', views.logout_view, name = 'logout'),
    path('reset-link', views.verify, name = 'reset-link'),
    path('verify/<str:User>/<uuid:tokenID>/', views.verify_user, name='verify_user'),
    path('reset-password/<uuid:tokenID>/', views.reset_password, name = 'reset-password'),
    path('comment', views.comment, name = 'comment'),
    path('profile', views.profile, name = 'profile'),
    path('recent-posts', views.recentposts, name = 'recentposts'),
    path('update-profile/', views.update_profile, name = 'update-profile'),
    path('update-like/', views.update_like, name = 'update-like'),
    path('update-shares/', views.update_shares, name = 'update-shares'),
    path('update-subscribe/', views.update_subscribe, name = 'update-subscribe'),
    path('subscribe-option/', views.update_suboption, name = 'subscribe-option'),
    path('update-bookmark/', views.update_bookmark, name = 'update-bookmark'),
    path('register', views.register, name = 'register'),
    path('loginsession/<slug:slug>/<slug:name>', views.loginsession, name = 'loginsession'),
    path('category/<str:cat>', views.category, name = 'category'),
    path('categories', views.categories, name = 'categories'),
    path('categories/<str:name>', views.category_detail, name = 'category_detail'),
    path('<slug:name>/<slug:slug>', views.postpage, name = 'postpage'),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)