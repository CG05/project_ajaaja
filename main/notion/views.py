from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.conf import settings
import shutil, os
from random import randint
from .models import Notion
import datetime, json
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import json
from django.conf import settings

def index(request):
    username = request.user.username
    if len(username) >= 5:
        username = username[:5]
        username += ".."
    else:
        username = username
    try :
        notions = Notion.objects.filter(user=request.user)
        parent = parent_find(notions[0])
    
        border_list = '<div class="px-4">'
        for notion in notions:
            if notion.parent == None:
                border_list += borderListFunction(notion, parent)
        border_list += "</div>"
    
        content={
            "username":username,
            "borderList":border_list,
        }
        return render(request, "home.html", content)
    except:
        content={
            "username":username,
        }
        return render(request, "home.html", content) 

def createNewPage(request):
    if not request.user.is_active:
        msg = "<script>"
        msg += "alert('로그인 후 사용 가능합니다.');";
        msg += 'location.href="/account/login";'
        msg += "</script>";
        return HttpResponse(msg);
    else :
        username = request.user.username;
        originFilePath = os.path.join(settings.BASE_DIR, "template");
        originFile = originFilePath + "/notion/origin.html"
        destinationPath = os.path.join(originFilePath, 'notion/'+ username);
        pageNum = randint(1, 9999999999);
        pageNum = str(f'{pageNum:0>10}') + ".html";

        if not os.path.isdir(destinationPath):
            os.mkdir(destinationPath)

        n = Notion();
        n.user = username;
        n.url = f'{pageNum}';
        n.date = datetime.datetime.now()
        n.save()

        shutil.copyfile(originFile, os.path.join(destinationPath, pageNum))
        return redirect(f'/notion/{pageNum}')

def borderListFunction(notion, parent):
    if notion.parent is None:
        title = '';
        if notion.title != '':
            title = notion.title[:10]
            if len(title) == 10:
                title = title + '...';

        list_html = '<div style="padding: 0;">'
        if parent.url == notion.url:
            list_html += f"<div role='button' class='align-left'><span onclick='toggleChildren({notion.id})'>▽ </span><a href='/notion/{notion.url}' style='color:#37352FCC;' class='text-decoration-none' onclick='toggleChildren({notion.id})'><span id='{notion.id}'>{title or '제목없음'}</span></a><a href='/notion/remove/{ notion.id }' id='removeId' style='color:#37352FCC; margin-left:auto;' class='text-decoration-none'><div style='margin-right:15px;'><svg role='graphics-symbol' viewBox='0 0 16 16' class='trash' style='width: 16px; height: 16px; display: block; fill: rgba(55, 53, 47, 0.85); flex-shrink: 0;'><path d='M4.8623 15.4287H11.1445C12.1904 15.4287 12.8672 14.793 12.915 13.7402L13.3799 3.88965H14.1318C14.4736 3.88965 14.7402 3.62988 14.7402 3.28809C14.7402 2.95312 14.4736 2.69336 14.1318 2.69336H11.0898V1.66797C11.0898 0.62207 10.4268 0 9.29199 0H6.69434C5.56641 0 4.89648 0.62207 4.89648 1.66797V2.69336H1.86133C1.5332 2.69336 1.25977 2.95312 1.25977 3.28809C1.25977 3.62988 1.5332 3.88965 1.86133 3.88965H2.62012L3.08496 13.7471C3.13281 14.7998 3.80273 15.4287 4.8623 15.4287ZM6.1543 1.72949C6.1543 1.37402 6.40039 1.14844 6.7832 1.14844H9.20312C9.58594 1.14844 9.83203 1.37402 9.83203 1.72949V2.69336H6.1543V1.72949ZM4.99219 14.2188C4.61621 14.2188 4.34277 13.9453 4.32227 13.542L3.86426 3.88965H12.1152L11.6709 13.542C11.6572 13.9453 11.3838 14.2188 10.9941 14.2188H4.99219ZM5.9834 13.1182C6.27051 13.1182 6.45508 12.9336 6.44824 12.667L6.24316 5.50293C6.23633 5.22949 6.04492 5.05176 5.77148 5.05176C5.48438 5.05176 5.2998 5.23633 5.30664 5.50293L5.51172 12.667C5.51855 12.9404 5.70996 13.1182 5.9834 13.1182ZM8 13.1182C8.28711 13.1182 8.47852 12.9336 8.47852 12.667V5.50293C8.47852 5.23633 8.28711 5.05176 8 5.05176C7.71289 5.05176 7.52148 5.23633 7.52148 5.50293V12.667C7.52148 12.9336 7.71289 13.1182 8 13.1182ZM10.0166 13.1182C10.29 13.1182 10.4746 12.9404 10.4814 12.667L10.6934 5.50293C10.7002 5.23633 10.5088 5.05176 10.2285 5.05176C9.95508 5.05176 9.76367 5.22949 9.75684 5.50293L9.54492 12.667C9.53809 12.9336 9.72949 13.1182 10.0166 13.1182Z'></path></svg></div></a></div>"
            children_html = get_children_html_active(notion, 1)
        else:
            list_html += f"<div role='button' class='align-left'><span onclick='toggleChildren({notion.id})'>▷ </span><a href='/notion/{notion.url}' style='color:#37352FCC;' class='text-decoration-none' onclick='toggleChildren({notion.id})'><span id='{notion.id}'>{title or '제목없음'}</span></a><a href='/notion/remove/{ notion.id }' id='removeId' style='color:#37352FCC; margin-left:auto;' class='text-decoration-none'><div style='margin-right:15px;'><svg role='graphics-symbol' viewBox='0 0 16 16' class='trash' style='width: 16px; height: 16px; display: block; fill: rgba(55, 53, 47, 0.85); flex-shrink: 0;'><path d='M4.8623 15.4287H11.1445C12.1904 15.4287 12.8672 14.793 12.915 13.7402L13.3799 3.88965H14.1318C14.4736 3.88965 14.7402 3.62988 14.7402 3.28809C14.7402 2.95312 14.4736 2.69336 14.1318 2.69336H11.0898V1.66797C11.0898 0.62207 10.4268 0 9.29199 0H6.69434C5.56641 0 4.89648 0.62207 4.89648 1.66797V2.69336H1.86133C1.5332 2.69336 1.25977 2.95312 1.25977 3.28809C1.25977 3.62988 1.5332 3.88965 1.86133 3.88965H2.62012L3.08496 13.7471C3.13281 14.7998 3.80273 15.4287 4.8623 15.4287ZM6.1543 1.72949C6.1543 1.37402 6.40039 1.14844 6.7832 1.14844H9.20312C9.58594 1.14844 9.83203 1.37402 9.83203 1.72949V2.69336H6.1543V1.72949ZM4.99219 14.2188C4.61621 14.2188 4.34277 13.9453 4.32227 13.542L3.86426 3.88965H12.1152L11.6709 13.542C11.6572 13.9453 11.3838 14.2188 10.9941 14.2188H4.99219ZM5.9834 13.1182C6.27051 13.1182 6.45508 12.9336 6.44824 12.667L6.24316 5.50293C6.23633 5.22949 6.04492 5.05176 5.77148 5.05176C5.48438 5.05176 5.2998 5.23633 5.30664 5.50293L5.51172 12.667C5.51855 12.9404 5.70996 13.1182 5.9834 13.1182ZM8 13.1182C8.28711 13.1182 8.47852 12.9336 8.47852 12.667V5.50293C8.47852 5.23633 8.28711 5.05176 8 5.05176C7.71289 5.05176 7.52148 5.23633 7.52148 5.50293V12.667C7.52148 12.9336 7.71289 13.1182 8 13.1182ZM10.0166 13.1182C10.29 13.1182 10.4746 12.9404 10.4814 12.667L10.6934 5.50293C10.7002 5.23633 10.5088 5.05176 10.2285 5.05176C9.95508 5.05176 9.76367 5.22949 9.75684 5.50293L9.54492 12.667C9.53809 12.9336 9.72949 13.1182 10.0166 13.1182Z'></path></svg></div></a></div>"
            children_html = get_children_html(notion, 1)
        if children_html:
            if parent.url == notion.url:
                list_html += f"<div role='button' id='children-{notion.id}'>{children_html}</div>"
            else :
                list_html += f"<div role='button' id='children-{notion.id}' style='display: none;'>{children_html}</div>"
        list_html += '</div>'
        return list_html
    return ''

def get_children_html(notion, num):
    children_html = ""
    for child in notion.children.all():
        title = '';
        if child.title != '':
            title = child.title[:10]
            if len(title) == 10:
                title = title + '...'

        children_html += f"<div><span onclick='toggleChildren({child.id})'>▷ </span><a href='/notion/{child.url}' class='text-decoration-none' style='color:#37352FCC;' onclick='toggleChildren({child.id})'><span id='{child.id}'  >{title or '제목없음'}</span></a><a href='/notion/remove/{ child.id }' id='removeId' style='color:#37352FCC; margin-left:auto;' class='text-decoration-none'><div style='margin-right:15px;'><svg role='graphics-symbol' viewBox='0 0 16 16' class='trash' style='width: 16px; height: 16px; display: block; fill: rgba(55, 53, 47, 0.85); flex-shrink: 0;'><path d='M4.8623 15.4287H11.1445C12.1904 15.4287 12.8672 14.793 12.915 13.7402L13.3799 3.88965H14.1318C14.4736 3.88965 14.7402 3.62988 14.7402 3.28809C14.7402 2.95312 14.4736 2.69336 14.1318 2.69336H11.0898V1.66797C11.0898 0.62207 10.4268 0 9.29199 0H6.69434C5.56641 0 4.89648 0.62207 4.89648 1.66797V2.69336H1.86133C1.5332 2.69336 1.25977 2.95312 1.25977 3.28809C1.25977 3.62988 1.5332 3.88965 1.86133 3.88965H2.62012L3.08496 13.7471C3.13281 14.7998 3.80273 15.4287 4.8623 15.4287ZM6.1543 1.72949C6.1543 1.37402 6.40039 1.14844 6.7832 1.14844H9.20312C9.58594 1.14844 9.83203 1.37402 9.83203 1.72949V2.69336H6.1543V1.72949ZM4.99219 14.2188C4.61621 14.2188 4.34277 13.9453 4.32227 13.542L3.86426 3.88965H12.1152L11.6709 13.542C11.6572 13.9453 11.3838 14.2188 10.9941 14.2188H4.99219ZM5.9834 13.1182C6.27051 13.1182 6.45508 12.9336 6.44824 12.667L6.24316 5.50293C6.23633 5.22949 6.04492 5.05176 5.77148 5.05176C5.48438 5.05176 5.2998 5.23633 5.30664 5.50293L5.51172 12.667C5.51855 12.9404 5.70996 13.1182 5.9834 13.1182ZM8 13.1182C8.28711 13.1182 8.47852 12.9336 8.47852 12.667V5.50293C8.47852 5.23633 8.28711 5.05176 8 5.05176C7.71289 5.05176 7.52148 5.23633 7.52148 5.50293V12.667C7.52148 12.9336 7.71289 13.1182 8 13.1182ZM10.0166 13.1182C10.29 13.1182 10.4746 12.9404 10.4814 12.667L10.6934 5.50293C10.7002 5.23633 10.5088 5.05176 10.2285 5.05176C9.95508 5.05176 9.76367 5.22949 9.75684 5.50293L9.54492 12.667C9.53809 12.9336 9.72949 13.1182 10.0166 13.1182Z'></path></svg></div></a>"
        if child.children.exists():
            children_html += f"<div id='children-{child.id}' style='display: none;'>{get_children_html(child, num+1)}</div>"
        children_html += "</div>"
    return children_html

def get_children_html_active(notion, num):
    children_html = ""
    for child in notion.children.all():
        title = '';
        if child.title != '':
            title = child.title[:10]
            if len(title) == 10:
                title = title + '...'

        children_html += f"<div style='width:{213 - 20 * num}px'><span onclick='toggleChildren({child.id})'>▷ </span><a href='/notion/{child.url}' class='text-decoration-none' style='color:#37352FCC;' onclick='toggleChildren({child.id})'><span id='{child.id}'  >{title or '제목없음'}</span></a><a href='/notion/remove/{ child.id }' id='removeId' style='color:#37352FCC;' class='text-decoration-none'><div><svg role='graphics-symbol' viewBox='0 0 16 16' class='trash' style='width: 16px; height: 16px; display: block; fill: rgba(55, 53, 47, 0.85); flex-shrink: 0;'><path d='M4.8623 15.4287H11.1445C12.1904 15.4287 12.8672 14.793 12.915 13.7402L13.3799 3.88965H14.1318C14.4736 3.88965 14.7402 3.62988 14.7402 3.28809C14.7402 2.95312 14.4736 2.69336 14.1318 2.69336H11.0898V1.66797C11.0898 0.62207 10.4268 0 9.29199 0H6.69434C5.56641 0 4.89648 0.62207 4.89648 1.66797V2.69336H1.86133C1.5332 2.69336 1.25977 2.95312 1.25977 3.28809C1.25977 3.62988 1.5332 3.88965 1.86133 3.88965H2.62012L3.08496 13.7471C3.13281 14.7998 3.80273 15.4287 4.8623 15.4287ZM6.1543 1.72949C6.1543 1.37402 6.40039 1.14844 6.7832 1.14844H9.20312C9.58594 1.14844 9.83203 1.37402 9.83203 1.72949V2.69336H6.1543V1.72949ZM4.99219 14.2188C4.61621 14.2188 4.34277 13.9453 4.32227 13.542L3.86426 3.88965H12.1152L11.6709 13.542C11.6572 13.9453 11.3838 14.2188 10.9941 14.2188H4.99219ZM5.9834 13.1182C6.27051 13.1182 6.45508 12.9336 6.44824 12.667L6.24316 5.50293C6.23633 5.22949 6.04492 5.05176 5.77148 5.05176C5.48438 5.05176 5.2998 5.23633 5.30664 5.50293L5.51172 12.667C5.51855 12.9404 5.70996 13.1182 5.9834 13.1182ZM8 13.1182C8.28711 13.1182 8.47852 12.9336 8.47852 12.667V5.50293C8.47852 5.23633 8.28711 5.05176 8 5.05176C7.71289 5.05176 7.52148 5.23633 7.52148 5.50293V12.667C7.52148 12.9336 7.71289 13.1182 8 13.1182ZM10.0166 13.1182C10.29 13.1182 10.4746 12.9404 10.4814 12.667L10.6934 5.50293C10.7002 5.23633 10.5088 5.05176 10.2285 5.05176C9.95508 5.05176 9.76367 5.22949 9.75684 5.50293L9.54492 12.667C9.53809 12.9336 9.72949 13.1182 10.0166 13.1182Z'></path></svg></div></a>"
        if child.children.exists():
            children_html += f"<div id='children-{child.id}'>{get_children_html_active(child, num+1)}</div>"
        children_html += "</div>"
    return children_html

def parent_find(notion):
    # 부모가 없으면 현재 노션이 최상위 부모임
    if notion.parent is None:
        return notion
    # 부모가 있으면 부모를 찾아서 계속 재귀 호출
    return parent_find(notion.parent)

def pageNum(request, pageNum):
    if request.user.is_active:
        # 현재 사용자와 관련된 모든 Notion 객체 가져오기
        notions = Notion.objects.filter(user=request.user)
        # 현재 페이지와 관련된 Notion 객체 가져오기
        now = get_object_or_404(Notion, url=pageNum)
        
        parent = parent_find(now)

        border_list = '<div style=" color: rgba(55, 53, 47, 0.8); font-size:14px; font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol";">'
        for notion in notions:
            if notion.parent == None:
                border_list += borderListFunction(notion, parent)
        border_list += "</div>"
        username = request.user.username
        username_ = ''
        if len(username) >= 5:
            username_ = username[:5]
            username_ += ".."
        else:
            username_ = username
        content = {
            'notions': notions,
            'now': now,
            'borderList':border_list,
            'parent':parent,
            'username':username_,
        }
        return render(request, f'notion/{username}/{pageNum}', content)
    else:
        msg = "<script>"
        msg += "alert('로그인 후 사용 가능합니다.');"
        msg += 'location.href="/account/login";'
        msg += "</script>"
        return HttpResponse(msg)

def save(request, notionId):
    notion = Notion.objects.get(id=notionId)
    data = json.loads(request.body)
    notion.title = data['title'];
    notion.save();
    
    return JsonResponse({"message" : data['title']}, status=200)

def saveBody(request, notionId):
    notion = Notion.objects.get(id=notionId)
    data = json.loads(request.body)
    notion.content = data['content']
    notion.save();
    
    return JsonResponse({"message" : data['content']}, status=200)

def sendEmail(request):
    url = request.GET.get('url');

    subject = f'{request.user.username}님 notion 공유'
    message = f'안녕하세요. {request.user.username} 님이 공유하신 페이지 입니다.\n'
    message += f'http://localhost:8000/notion/guest/{request.user.username}/{url}/'
    email_from = '관리자 <admin@test.com>'
    email = EmailMessage(subject, message, email_from)

    toEmail = request.GET.get('emails')
    email.to = toEmail.split(',')
    result = email.send()


    msg = '<script>'
    try :
        if result :
            msg += 'alert("이메일 전송이 완료 되었습니다.");'
        else:
            msg += 'alert("이메일 전송에 실패 했습니다.");'
    except:
        msg += 'alert("이메일 주소를 확인하세요.");'
    
    msg += f'location.href="/notion/{url}";'
    msg += "</script>"

    return HttpResponse(msg);


def guest(request, user, pageNum):  
    notion = Notion.objects.filter(user=user).values()
    now = Notion.objects.filter(url=f'{pageNum}').values()
    username = user;
    content = {
        'notion':notion,
        'now':now[0],
    }
    return render(request, f'notion/{username}/{pageNum}', content);
    
def createChild(request, notionId, url):
    
    username = request.user.username
    originFilePath = os.path.join(settings.BASE_DIR, "template")
    originFile = os.path.join(originFilePath, "notion/origin.html")
    destinationPath = os.path.join(originFilePath, 'notion/' + username)
    pageNum = randint(1, 9999999999)
    pageNum = f'{pageNum:0>10}.html'

    if not os.path.isdir(destinationPath):
        os.mkdir(destinationPath)

    # 부모 Notion 객체 가져오기
    parent_notion = get_object_or_404(Notion, id=notionId)

    # 자식 Notion 생성
    child_notion = Notion.objects.create(user=username, url=pageNum, date=datetime.datetime.now(), parent=parent_notion)
    
    shutil.copyfile(originFile, os.path.join(destinationPath, pageNum))
    return redirect(f'/notion/{pageNum}')


def remove(request, notionId):
    notion = Notion.objects.get(id=notionId);
    title = notion.title;
    if title == "":
        title = '제목없음'
    notion.delete()
    msg = "<script>"
    msg += f"alert('{title} 제목의 글을 삭제했습니다.');"
    msg += "location.href='/';"
    msg += "</script>"
    return HttpResponse(msg);


