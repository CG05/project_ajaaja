from django.shortcuts import render, redirect, HttpResponse
from page.models import Page

def default(request):
    user = request.user
    username = user.username
    pages = Page.objects.filter(username=username)
    pageList = list(pages)
    content={
        "username":username,
        "pageList":pageList,
    }
    return render(request, "ltab/default.html", content)

def newpage(request):
    user = request.user
    username = user.username
    
    new = Page()
    new.username = username
    new.title = "Untitled"
    new.pagepath = "newpage"
    new.save();
    new = Page.objects.get(pagepath="newpage")
    new.pagepath = new.id
    new.save();

    return redirect(f"/page/{new.id}/");

