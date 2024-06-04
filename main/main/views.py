from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.hashers import check_password
def createAccount(request):
    if request.method == 'GET':
        return render(request, "registration/register.html")
    elif request.method == 'POST':
        username = request.POST.get("username");
        password = request.POST.get("password");
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        
        if not all([username, password, first_name, last_name, email]):
            msg = "<script>"
            msg += "alert('빈 칸이 있습니다. 모든 정보를 입력해주세요.');"
            msg += "location.href='/account/register';"
            msg += "</script>"
            return HttpResponse(msg)
        
        try:
            User.objects.create_user(username, email, password, 
            first_name=first_name, last_name=last_name)

            return redirect('login')
        except:
            msg = "<script>";
            msg += "alert('같은 아이디가 존재합니다. 다시 가입하세요.');";
            msg += "location.href='/account/register';";
            msg += "</script>";
            return HttpResponse(msg);

def login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html');
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password);

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            msg = "<script>";
            msg += "alert('로그인 아이디/비밀번호가 틀립니다. 다시 로그인 하세요.');";
            msg += "location.href='/account/login';";
            msg += "</script>";
            return HttpResponse(msg);

def logout(request):
    auth.logout(request);
    msg = "<script>";
    msg += "alert('로그아웃 되었습니다.');";
    msg += "location.href='/';";
    msg += "</script>";
    return HttpResponse(msg);

def index(request):
    if request.user.is_active:
        return redirect("/page/");
    else:
        return render(request, "main.html")