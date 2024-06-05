from django.contrib import admin
from .models import Notion
# Register your models here.
class NotionAdmin(admin.ModelAdmin):
    list_display = ('user','title','url','content','parent','date')


admin.site.register(Notion, NotionAdmin)