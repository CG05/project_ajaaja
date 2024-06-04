from django.shortcuts import render
from .models import Page
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    user = request.user
    username = user.username
    pages = Page.objects.filter(username=username)
    pageList = list(pages)
    content={
        "username":username,
        "pageList":pageList,
    }
    
    return render(request, "home.html", content)

def getpage(request, pageid):
    user = request.user
    username = user.username
    pages = Page.objects.filter(username=username)
    pageList = list(pages)
    page = Page.objects.get(id=pageid)
    content={
        "username":username,
        "pageList":pageList,
        "page":page,
        "pageid":pageid,
    }
    
    return render(request, "page/page.html", content)



@csrf_exempt
def savepage(request, pageid):
    if request.method == 'POST':
        try:
            page = Page.objects.get(id=pageid)

            data = json.loads(request.body)
            content = data.get('content')
            title = content.get('title')
            contents = json.loads(content.get('contents'));

            page.title = title
            page.content = contents
            page.save()

            return JsonResponse({'message': 'Data saved successfully!'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)