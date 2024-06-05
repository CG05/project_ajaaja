from django.shortcuts import render, redirect, HttpResponse
from page.models import Page

def default(request):
    user = request.user
    username = ''
    if len(username) >= 5:
        username = user.username[:5]
        username += ".."
        print(username)
    else:
        username = user.username
        print(username)
    pages = Page.objects.filter(username=username)
    pageList = list(pages)
    content={
        "username":username,
        "pageList":pageList,
        "userid":user.id
    }
    return render(request, "ltab/default.html", content)

def new_page(request):
    user = request.user
    username = user.username
    
    new = Page();
    new.username = username
    new.title = "Untitled"
    new.pagepath = "newpage"
    new.save();
    new = Page.objects.get(pagepath="newpage")
    
    new.pagepath = new.id
    new.save();

    return redirect(f"/page/{new.id}/");

def newpage(request, pageid):
    pagepath = Page.objects.get(id=pageid).pagepath + "_"
    
    user = request.user
    username = user.username
    
    new = Page()
    new.username = username
    new.title = "Untitled"
    new.pagepath = "newpage"
    new.save();
    new = Page.objects.get(pagepath="newpage")
    
    new.pagepath = f'{pagepath}{new.id}'
    new.save();

    return redirect(f"/page/{new.id}/");



