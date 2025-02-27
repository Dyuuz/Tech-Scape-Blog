from django.contrib import admin
from .models import Category, Blog, PasswordReset, Newsletter, Comments, VerifyUser, Client
from django.db import models
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


# Register your models here.
class BlogAdminForm (forms.ModelForm):
    class Meta:
        model = Blog
        fields="__all__"
        widgets = { "body": CKEditor5Widget (config_name="default"),}

class BlogAdmin (admin.ModelAdmin):
    form = BlogAdminForm

class NewsletterAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'email',)
    list_display = ('user', 'subscribe', 'email',)
    
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'time')
    search_fields = ('user__username', 'token')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified')
    search_fields = ('username', 'email')
class VerifyUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user',)
    readonly_fields = ('user', 'token', 'created_at',)
    
admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(VerifyUser, VerifyUserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Comments)
admin.site.register(PasswordReset, PasswordResetTokenAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
