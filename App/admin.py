from django.contrib import admin
from .models import Category, Blog, PasswordReset, Newsletter, Comments, VerifyUser, Client

# Register your models here.
class NewsletterAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'email',)
    list_display = ('user', 'subscribe', 'email',)
    
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'time')
    search_fields = ('user__username', 'token')
    
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(VerifyUser)
admin.site.register(Client)
admin.site.register(Comments)
admin.site.register(PasswordReset, PasswordResetTokenAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
