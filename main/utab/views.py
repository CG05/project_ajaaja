from django.shortcuts import render

def default(request):
    return render(request, "utab/utab.html")

def openTab(request, tab1):
    return