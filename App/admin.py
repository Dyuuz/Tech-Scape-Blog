from django.contrib import admin
from .models import *

# Register your models here.
class NewsletterAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'subscribe', 'email',)
    list_display = ('user', 'subscribe', 'email',)
    
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comments)
admin.site.register(Newsletter,NewsletterAdmin)