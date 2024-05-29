from django.contrib import admin
from .models import Page

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'pagepath', 'content', 'title', 'created_at', 'updated_at')


admin.site.register(Page, PageAdmin)