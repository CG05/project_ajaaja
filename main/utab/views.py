from django.shortcuts import render, HttpResponse

def default(request):
    return render(request, "utab/utab.html")

def tab1(request):
    return HttpResponse("tab1")

def tab2(request):
    return HttpResponse("tab2")