from django.shortcuts import render, redirect, HttpResponse

def default(request):
    user = request.user
    username = user.username
    content={
        "username":username,
    }
    return render(request, "ltab/default.html", content)

