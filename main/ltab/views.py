from django.shortcuts import render

def default(request):
    user = request.user
    username = user.username
    content={
        "username":username,
    }
    return render(request, "ltab/default.html", content)


def pagePM(request):
    
    pass
