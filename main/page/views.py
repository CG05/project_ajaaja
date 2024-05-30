from django.shortcuts import render
from .models import Page
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def default(request):
    return render(request, "page/default.html")

def getpage(request, pageid):
    page = Page.objects.get(id=pageid)
    
    return render(request, "page/page.html", {"pageid": pageid, "page": page})

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