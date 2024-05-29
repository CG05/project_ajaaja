from django.shortcuts import render, HttpResponse

def default(request):
    return render(request, "utab/utab.html")

def tab1(request):
    return HttpResponse("https://www.notion.so/3-066abf1ec70245c1abe0b5f65ccd381c")

def tab2(request):
    return HttpResponse("https://www.notion.so/KG-815185992e024e41af2dcc1e7ad88358/")

def tab3(request):
    return HttpResponse("https://www.notion.so/c5d4ac256188454c9a6eb780385e9f7e")

def tab4(request):
    return HttpResponse("pagepath")