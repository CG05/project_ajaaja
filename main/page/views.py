from django.shortcuts import render
from .models import Page
import json 

def default(request):
    return render(request, "page/default.html")

def getpage(request, pageid):
    page = Page.objects.get(id=pageid)
    
    return render(request, "page/page.html", {"page": page})