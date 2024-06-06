from django.shortcuts import render, redirect, HttpResponse
from page.models import Page
from django.http import JsonResponse
from notion.models import Notion
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def search_notion(request):
    if request.method == 'POST':
        # POST 요청의 본문에서 검색어 추출
        data = json.loads(request.body)
        search_text = data.get('search_text')
        print(search_text)
        # 검색어가 포함된 Notion 모델을 찾습니다.
        notions = Notion.objects.filter(user=request.user, title__icontains=search_text)

        # 검색 결과를 리스트로 변환
        search_results = [{'title': notion.title, 'url': '/notion/' + str(notion.url)} for notion in notions]
        print(search_results)
        return JsonResponse({'results': search_results})
    else:
        # POST 요청이 아닌 경우에는 오류 응답을 반환
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
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



