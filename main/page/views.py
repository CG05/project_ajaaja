from django.shortcuts import render

def default(request):
    return render(request, "page/default.html")
# Create your views here.
