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
    notions = Notion.objects.filter(user=request.user)

    if len(username) > 5:
        username = username[:5]
        username += ".."
    else:
        username = username
    try :
        notions = Notion.objects.filter(user=request.user)
        parent = parent_find(notions[0])
        print(parent);
        border_list = '<div style=" color: rgba(55, 53, 47, 0.8); font-size:14px; font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol";">'
        for notion in notions:
            if notion.parent == None:
                border_list += borderListFunction(notion, parent)
        border_list += "</div>"
    
        content={
            "notions": notions,
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

        list_html = '<div class="family" style="width:100%;">'
        if parent.url == notion.url:
            print('parent==notion')
            # list_html += f"<div class='listbutton'><div style='display: inline' onclick='toggleChildren({notion.id})'>▽ </div><a href='/notion/{notion.url}' style='color:#37352FCC; z-index:2px;' class='text-decoration-none' onclick='toggleChildren({notion.id})'><span id='{notion.id}'>{title or '제목없음'}</span></a><a href='/notion/remove/{ notion.id }' id='removeId' style='z-index:2px' class='text-decoration-none'><div style='margin-right:15px;float:right;'><svg role='graphics-symbol' viewBox='0 0 16 16' class='trash' style='width: 16px; height: 16px; display: block; fill: rgba(55, 53, 47, 0.85); flex-shrink: 0;'><path d='M4.8623 15.4287H11.1445C12.1904 15.4287 12.8672 14.793 12.915 13.7402L13.3799 3.88965H14.1318C14.4736 3.88965 14.7402 3.62988 14.7402 3.28809C14.7402 2.95312 14.4736 2.69336 14.1318 2.69336H11.0898V1.66797C11.0898 0.62207 10.4268 0 9.29199 0H6.69434C5.56641 0 4.89648 0.62207 4.89648 1.66797V2.69336H1.86133C1.5332 2.69336 1.25977 2.95312 1.25977 3.28809C1.25977 3.62988 1.5332 3.88965 1.86133 3.88965H2.62012L3.08496 13.7471C3.13281 14.7998 3.80273 15.4287 4.8623 15.4287ZM6.1543 1.72949C6.1543 1.37402 6.40039 1.14844 6.7832 1.14844H9.20312C9.58594 1.14844 9.83203 1.37402 9.83203 1.72949V2.69336H6.1543V1.72949ZM4.99219 14.2188C4.61621 14.2188 4.34277 13.9453 4.32227 13.542L3.86426 3.88965H12.1152L11.6709 13.542C11.6572 13.9453 11.3838 14.2188 10.9941 14.2188H4.99219ZM5.9834 13.1182C6.27051 13.1182 6.45508 12.9336 6.44824 12.667L6.24316 5.50293C6.23633 5.22949 6.04492 5.05176 5.77148 5.05176C5.48438 5.05176 5.2998 5.23633 5.30664 5.50293L5.51172 12.667C5.51855 12.9404 5.70996 13.1182 5.9834 13.1182ZM8 13.1182C8.28711 13.1182 8.47852 12.9336 8.47852 12.667V5.50293C8.47852 5.23633 8.28711 5.05176 8 5.05176C7.71289 5.05176 7.52148 5.23633 7.52148 5.50293V12.667C7.52148 12.9336 7.71289 13.1182 8 13.1182ZM10.0166 13.1182C10.29 13.1182 10.4746 12.9404 10.4814 12.667L10.6934 5.50293C10.7002 5.23633 10.5088 5.05176 10.2285 5.05176C9.95508 5.05176 9.76367 5.22949 9.75684 5.50293L9.54492 12.667C9.53809 12.9336 9.72949 13.1182 10.0166 13.1182Z'></path></svg></div></a></div>"
            list_html += f'<div onclick="location.href=`/notion/{notion.url}`;" role="button" tabindex="0" class="showPage" aria-controls="addPage" aria-expanded="false" style="user-select: none; transition: background 20ms ease-in 0s; display: flex; align-items: center; border-radius: 6px; height: 30px;"><div onclick="event.stopPropagation();toggleChildren(this,{notion.id})" style="margin-left: 3px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; flex-grow: 0; width: 22px; height: 18px; margin-right: 8px; position: relative; z-index:3;"><div style="display: grid;"><div style="grid-area: 1 / 1; z-index: 1; order: 0; opacity: 0; transition: opacity 150ms ease 0s;"><div role="button" class="alterBtn" tabindex="0" aria-describedby=":rn:" aria-expanded="false" aria-label="열기" style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; position: relative z-index=3; display: flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 4px;"><svg role="graphics-symbol" viewBox="0 0 12 12" class="chevronDownRoundedThick" style="width: 12px; height: 12px; display: block; fill: rgba(55, 53, 47, 0.35); flex-shrink: 0; rotate:0deg; transition: rotate 200ms ease-out 0s; opacity: 1;"><path d="M6.02734 8.80274C6.27148 8.80274 6.47168 8.71484 6.66211 8.51465L10.2803 4.82324C10.4268 4.67676 10.5 4.49609 10.5 4.28125C10.5 3.85156 10.1484 3.5 9.72363 3.5C9.50879 3.5 9.30859 3.58789 9.15234 3.74902L6.03223 6.9668L2.90722 3.74902C2.74609 3.58789 2.55078 3.5 2.33105 3.5C1.90137 3.5 1.55469 3.85156 1.55469 4.28125C1.55469 4.49609 1.62793 4.67676 1.77441 4.82324L5.39258 8.51465C5.58789 8.71973 5.78808 8.80274 6.02734 8.80274Z"></path></svg></div></div><div style="grid-area: 1 / 1; opacity: 1; transition: opacity 150ms ease 0s; order: 1;"><div class="notion-record-icon notranslate" style="display: flex; align-items: center; justify-content: center; height: 20px; width: 20px; border-radius: 0.25em; flex-shrink: 0;"><span role="img" aria-label="페이지 아이콘 변경"><svg role="graphics-symbol" viewBox="0 0 16 16" style="width: 18px; height: 18px; display: block; fill: rgb(145, 145, 142); flex-shrink: 0;"><path d="M4.35645 15.4678H11.6367C13.0996 15.4678 13.8584 14.6953 13.8584 13.2256V7.02539C13.8584 6.0752 13.7354 5.6377 13.1406 5.03613L9.55176 1.38574C8.97754 0.804688 8.50586 0.667969 7.65137 0.667969H4.35645C2.89355 0.667969 2.13477 1.44043 2.13477 2.91016V13.2256C2.13477 14.7021 2.89355 15.4678 4.35645 15.4678ZM4.46582 14.1279C3.80273 14.1279 3.47461 13.7793 3.47461 13.1436V2.99219C3.47461 2.36328 3.80273 2.00781 4.46582 2.00781H7.37793V5.75391C7.37793 6.73145 7.86328 7.20312 8.83398 7.20312H12.5186V13.1436C12.5186 13.7793 12.1836 14.1279 11.5205 14.1279H4.46582ZM8.95703 6.02734C8.67676 6.02734 8.56055 5.9043 8.56055 5.62402V2.19238L12.334 6.02734H8.95703ZM10.4336 9.00098H5.42969C5.16992 9.00098 4.98535 9.19238 4.98535 9.43164C4.98535 9.67773 5.16992 9.86914 5.42969 9.86914H10.4336C10.6797 9.86914 10.8643 9.67773 10.8643 9.43164C10.8643 9.19238 10.6797 9.00098 10.4336 9.00098ZM10.4336 11.2979H5.42969C5.16992 11.2979 4.98535 11.4893 4.98535 11.7354C4.98535 11.9746 5.16992 12.1592 5.42969 12.1592H10.4336C10.6797 12.1592 10.8643 11.9746 10.8643 11.7354C10.8643 11.4893 10.6797 11.2979 10.4336 11.2979Z"></path></svg></span></div></div></div></div><div style="padding: 5px 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"><span id="titleSpan_{notion.id}" style="text-transform: initial; font-size: 14px; line-height: 1; color: rgb(145, 145, 142); font-weight: 500; transition: color 100ms ease-out 0s;">{title or '제목없음'}</span></div><div style="margin-left: auto;"><div class="addpage" style="display: flex; align-items: center; pointer-events: pointer; opacity: 0; transition: opacity 150ms ease 0s;"><div onclick="event.stopPropagation();location.href=`/notion/createChild/{notion.id}/{notion.url}/`" role="button" tabindex="0" class="addpage shadow-cursor-new-page-sidebar" aria-label="페이지 추가" style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 1; height: 20px; width: 20px; border-radius: 4px; margin-right: 6px;"><span></span><svg role="graphics-symbol" viewBox="0 0 14 14" class="plusThick" style="width: 14px; height: 14px; display: block; fill: rgba(55, 53, 47, 0.45); flex-shrink: 0;"><path d="M2 7.16357C2 7.59692 2.36011 7.95093 2.78735 7.95093H6.37622V11.5398C6.37622 11.9731 6.73022 12.3271 7.16357 12.3271C7.59692 12.3271 7.95093 11.9731 7.95093 11.5398V7.95093H11.5398C11.9731 7.95093 12.3271 7.59692 12.3271 7.16357C12.3271 6.73022 11.9731 6.37622 11.5398 6.37622H7.95093V2.78735C7.95093 2.36011 7.59692 2 7.16357 2C6.73022 2 6.37622 2.36011 6.37622 2.78735V6.37622H2.78735C2.36011 6.37622 2 6.73022 2 7.16357Z"></path></svg></div></div></div></div>'
            children_html = get_children_html_active(notion, 1)
        else:
            print('parent!=notion')
            list_html += f'<div onclick="location.href=`/notion/{notion.url}`;" role="button" tabindex="0" class="showPage" aria-controls="addPage" aria-expanded="false" style="user-select: none; transition: background 20ms ease-in 0s; display: flex; align-items: center; border-radius: 6px; height: 30px;"><div onclick="event.stopPropagation();toggleChildren(this,{notion.id})" style="margin-left: 3px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; flex-grow: 0; width: 22px; height: 18px; margin-right: 8px; position: relative;"><div style="display: grid;"><div style="grid-area: 1 / 1; z-index: 1; order: 0; opacity: 0; transition: opacity 150ms ease 0s;"><div role="button" class="alterBtn" tabindex="0" aria-describedby=":rn:" aria-expanded="false" aria-label="열기" style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; position: relative z-index=3; display: flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 4px;"><svg role="graphics-symbol" viewBox="0 0 12 12" class="chevronDownRoundedThick" style="width: 12px; height: 12px; display: block; fill: rgba(55, 53, 47, 0.35); flex-shrink: 0; rotate:0deg; transition: rotate 200ms ease-out 0s; opacity: 1;"><path d="M6.02734 8.80274C6.27148 8.80274 6.47168 8.71484 6.66211 8.51465L10.2803 4.82324C10.4268 4.67676 10.5 4.49609 10.5 4.28125C10.5 3.85156 10.1484 3.5 9.72363 3.5C9.50879 3.5 9.30859 3.58789 9.15234 3.74902L6.03223 6.9668L2.90722 3.74902C2.74609 3.58789 2.55078 3.5 2.33105 3.5C1.90137 3.5 1.55469 3.85156 1.55469 4.28125C1.55469 4.49609 1.62793 4.67676 1.77441 4.82324L5.39258 8.51465C5.58789 8.71973 5.78808 8.80274 6.02734 8.80274Z"></path></svg></div></div><div style="grid-area: 1 / 1; opacity: 1; transition: opacity 150ms ease 0s; order: 1;"><div class="notion-record-icon notranslate" style="display: flex; align-items: center; justify-content: center; height: 20px; width: 20px; border-radius: 0.25em; flex-shrink: 0;"><span role="img" aria-label="페이지 아이콘 변경"><svg role="graphics-symbol" viewBox="0 0 16 16" style="width: 18px; height: 18px; display: block; fill: rgb(145, 145, 142); flex-shrink: 0;"><path d="M4.35645 15.4678H11.6367C13.0996 15.4678 13.8584 14.6953 13.8584 13.2256V7.02539C13.8584 6.0752 13.7354 5.6377 13.1406 5.03613L9.55176 1.38574C8.97754 0.804688 8.50586 0.667969 7.65137 0.667969H4.35645C2.89355 0.667969 2.13477 1.44043 2.13477 2.91016V13.2256C2.13477 14.7021 2.89355 15.4678 4.35645 15.4678ZM4.46582 14.1279C3.80273 14.1279 3.47461 13.7793 3.47461 13.1436V2.99219C3.47461 2.36328 3.80273 2.00781 4.46582 2.00781H7.37793V5.75391C7.37793 6.73145 7.86328 7.20312 8.83398 7.20312H12.5186V13.1436C12.5186 13.7793 12.1836 14.1279 11.5205 14.1279H4.46582ZM8.95703 6.02734C8.67676 6.02734 8.56055 5.9043 8.56055 5.62402V2.19238L12.334 6.02734H8.95703ZM10.4336 9.00098H5.42969C5.16992 9.00098 4.98535 9.19238 4.98535 9.43164C4.98535 9.67773 5.16992 9.86914 5.42969 9.86914H10.4336C10.6797 9.86914 10.8643 9.67773 10.8643 9.43164C10.8643 9.19238 10.6797 9.00098 10.4336 9.00098ZM10.4336 11.2979H5.42969C5.16992 11.2979 4.98535 11.4893 4.98535 11.7354C4.98535 11.9746 5.16992 12.1592 5.42969 12.1592H10.4336C10.6797 12.1592 10.8643 11.9746 10.8643 11.7354C10.8643 11.4893 10.6797 11.2979 10.4336 11.2979Z"></path></svg></span></div></div></div></div><div style="padding: 5px 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"><span id="titleSpan_{notion.id}" style="text-transform: initial; font-size: 14px; line-height: 1; color: rgb(145, 145, 142); font-weight: 500; transition: color 100ms ease-out 0s;">{title or '제목없음'}</span></div><div style="margin-left: auto;"><div class="addpage" style="display: flex; align-items: center; pointer-events: pointer; opacity: 0; transition: opacity 150ms ease 0s;"><div onclick="event.stopPropagation();location.href=`/notion/createChild/{notion.id}/{notion.url}/`" role="button" tabindex="0" class="addpage shadow-cursor-new-page-sidebar" aria-label="페이지 추가" style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 1; height: 20px; width: 20px; border-radius: 4px; margin-right: 6px;"><span></span><svg role="graphics-symbol" viewBox="0 0 14 14" class="plusThick" style="width: 14px; height: 14px; display: block; fill: rgba(55, 53, 47, 0.45); flex-shrink: 0;"><path d="M2 7.16357C2 7.59692 2.36011 7.95093 2.78735 7.95093H6.37622V11.5398C6.37622 11.9731 6.73022 12.3271 7.16357 12.3271C7.59692 12.3271 7.95093 11.9731 7.95093 11.5398V7.95093H11.5398C11.9731 7.95093 12.3271 7.59692 12.3271 7.16357C12.3271 6.73022 11.9731 6.37622 11.5398 6.37622H7.95093V2.78735C7.95093 2.36011 7.59692 2 7.16357 2C6.73022 2 6.37622 2.36011 6.37622 2.78735V6.37622H2.78735C2.36011 6.37622 2 6.73022 2 7.16357Z"></path></svg></div></div></div></div>'
            # list_html += f"<div class='listbutton'><div style='display: inline' onclick='toggleChildren({notion.id})'>▽ </div><a href='/notion/{notion.url}' style='color:#37352FCC; z-index:2px;' class='text-decoration-none' onclick='toggleChildren({notion.id})'><span id='{notion.id}'>{title or '제목없음'}</span></a><a href='/notion/remove/{ notion.id }' id='removeId' style='z-index:2px' class='text-decoration-none'><div style='margin-right:15px;float:right;'><svg role='graphics-symbol' viewBox='0 0 16 16' class='trash' style='width: 16px; height: 16px; display: block; fill: rgba(55, 53, 47, 0.85); flex-shrink: 0;'><path d='M4.8623 15.4287H11.1445C12.1904 15.4287 12.8672 14.793 12.915 13.7402L13.3799 3.88965H14.1318C14.4736 3.88965 14.7402 3.62988 14.7402 3.28809C14.7402 2.95312 14.4736 2.69336 14.1318 2.69336H11.0898V1.66797C11.0898 0.62207 10.4268 0 9.29199 0H6.69434C5.56641 0 4.89648 0.62207 4.89648 1.66797V2.69336H1.86133C1.5332 2.69336 1.25977 2.95312 1.25977 3.28809C1.25977 3.62988 1.5332 3.88965 1.86133 3.88965H2.62012L3.08496 13.7471C3.13281 14.7998 3.80273 15.4287 4.8623 15.4287ZM6.1543 1.72949C6.1543 1.37402 6.40039 1.14844 6.7832 1.14844H9.20312C9.58594 1.14844 9.83203 1.37402 9.83203 1.72949V2.69336H6.1543V1.72949ZM4.99219 14.2188C4.61621 14.2188 4.34277 13.9453 4.32227 13.542L3.86426 3.88965H12.1152L11.6709 13.542C11.6572 13.9453 11.3838 14.2188 10.9941 14.2188H4.99219ZM5.9834 13.1182C6.27051 13.1182 6.45508 12.9336 6.44824 12.667L6.24316 5.50293C6.23633 5.22949 6.04492 5.05176 5.77148 5.05176C5.48438 5.05176 5.2998 5.23633 5.30664 5.50293L5.51172 12.667C5.51855 12.9404 5.70996 13.1182 5.9834 13.1182ZM8 13.1182C8.28711 13.1182 8.47852 12.9336 8.47852 12.667V5.50293C8.47852 5.23633 8.28711 5.05176 8 5.05176C7.71289 5.05176 7.52148 5.23633 7.52148 5.50293V12.667C7.52148 12.9336 7.71289 13.1182 8 13.1182ZM10.0166 13.1182C10.29 13.1182 10.4746 12.9404 10.4814 12.667L10.6934 5.50293C10.7002 5.23633 10.5088 5.05176 10.2285 5.05176C9.95508 5.05176 9.76367 5.22949 9.75684 5.50293L9.54492 12.667C9.53809 12.9336 9.72949 13.1182 10.0166 13.1182Z'></path></svg></div></a></div>"
            children_html = get_children_html(notion, 1)
        if children_html:
            if parent.url == notion.url:
                list_html += f"<div class='childarea' id='children-{notion.id}'>{children_html}</div>"
            else :
                list_html += f"<div class='childarea' id='children-{notion.id}' style='display: none;'>{children_html}</div>"
        list_html += '</div>'
        return list_html
    return ''

def get_children_html(notion, num):
    print('get_children_html')
    children_html = ""
    for child in notion.children.all():
        title = '';
        if child.title != '':
            title = child.title[:10]
            if len(title) == 10:
                title = title + '...'
        print('title:', title)
        
        children_html += f'<div onclick="location.href=`/notion/{child.url}`;" role="button" tabindex="0" class="showPage" onclick="location.href=`/notion/{child.url}`" aria-controls="addPage" aria-expanded="false" style="user-select: none; transition: background 20ms ease-in 0s; display: flex; align-items: center; border-radius: 6px; height: 30px;"><div onclick="event.stopPropagation();toggleChildren(this,{child.id})" style="margin-left:{12*num}px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; flex-grow: 0; width: 22px; height: 18px; margin-right: 8px; position: relative;"><div style="display: grid;"><div style="grid-area: 1 / 1; z-index: 1; order: 0; opacity: 0; transition: opacity 150ms ease 0s;"><div role="button" class="alterBtn" tabindex="0" aria-describedby=":rn:" aria-expanded="false" aria-label="열기" style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; position: relative; display: flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 4px; z-index=3;"><svg role="graphics-symbol" viewBox="0 0 12 12" class="chevronDownRoundedThick" style="width: 12px; height: 12px; display: block; fill: rgba(55, 53, 47, 0.35); flex-shrink: 0; rotate:0deg; transition: rotate 200ms ease-out 0s; opacity: 1;"><path d="M6.02734 8.80274C6.27148 8.80274 6.47168 8.71484 6.66211 8.51465L10.2803 4.82324C10.4268 4.67676 10.5 4.49609 10.5 4.28125C10.5 3.85156 10.1484 3.5 9.72363 3.5C9.50879 3.5 9.30859 3.58789 9.15234 3.74902L6.03223 6.9668L2.90722 3.74902C2.74609 3.58789 2.55078 3.5 2.33105 3.5C1.90137 3.5 1.55469 3.85156 1.55469 4.28125C1.55469 4.49609 1.62793 4.67676 1.77441 4.82324L5.39258 8.51465C5.58789 8.71973 5.78808 8.80274 6.02734 8.80274Z"></path></svg></div></div><div style="grid-area: 1 / 1; opacity: 1; transition: opacity 150ms ease 0s; order: 1;"><div class="notion-record-icon notranslate" style="display: flex; align-items: center; justify-content: center; height: 20px; width: 20px; border-radius: 0.25em; flex-shrink: 0;"><span role="img" aria-label="페이지 아이콘 변경"><svg role="graphics-symbol" viewBox="0 0 16 16" style="width: 18px; height: 18px; display: block; fill: rgb(145, 145, 142); flex-shrink: 0;"><path d="M4.35645 15.4678H11.6367C13.0996 15.4678 13.8584 14.6953 13.8584 13.2256V7.02539C13.8584 6.0752 13.7354 5.6377 13.1406 5.03613L9.55176 1.38574C8.97754 0.804688 8.50586 0.667969 7.65137 0.667969H4.35645C2.89355 0.667969 2.13477 1.44043 2.13477 2.91016V13.2256C2.13477 14.7021 2.89355 15.4678 4.35645 15.4678ZM4.46582 14.1279C3.80273 14.1279 3.47461 13.7793 3.47461 13.1436V2.99219C3.47461 2.36328 3.80273 2.00781 4.46582 2.00781H7.37793V5.75391C7.37793 6.73145 7.86328 7.20312 8.83398 7.20312H12.5186V13.1436C12.5186 13.7793 12.1836 14.1279 11.5205 14.1279H4.46582ZM8.95703 6.02734C8.67676 6.02734 8.56055 5.9043 8.56055 5.62402V2.19238L12.334 6.02734H8.95703ZM10.4336 9.00098H5.42969C5.16992 9.00098 4.98535 9.19238 4.98535 9.43164C4.98535 9.67773 5.16992 9.86914 5.42969 9.86914H10.4336C10.6797 9.86914 10.8643 9.67773 10.8643 9.43164C10.8643 9.19238 10.6797 9.00098 10.4336 9.00098ZM10.4336 11.2979H5.42969C5.16992 11.2979 4.98535 11.4893 4.98535 11.7354C4.98535 11.9746 5.16992 12.1592 5.42969 12.1592H10.4336C10.6797 12.1592 10.8643 11.9746 10.8643 11.7354C10.8643 11.4893 10.6797 11.2979 10.4336 11.2979Z"></path></svg></span></div></div></div></div><div style="padding: 5px 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"><span id="titleSpan_{child.id}" style="text-transform: initial; font-size: 14px; line-height: 1; color: rgb(145, 145, 142); font-weight: 500; transition: color 100ms ease-out 0s;">{title or '제목없음'}</span></div><div style="margin-left: auto;"><div class="addpage" style="display: flex; align-items: center; pointer-events: pointer; opacity: 0; transition: opacity 150ms ease 0s;"><div onclick="event.stopPropagation();location.href=`/notion/createChild/{child.id}/{child.url}/`" role="button" tabindex="0" class="addpage shadow-cursor-new-page-sidebar" aria-label="페이지 추가" style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 1; height: 20px; width: 20px; border-radius: 4px; margin-right: 6px;"><span></span><svg role="graphics-symbol" viewBox="0 0 14 14" class="plusThick" style="width: 14px; height: 14px; display: block; fill: rgba(55, 53, 47, 0.45); flex-shrink: 0;"><path d="M2 7.16357C2 7.59692 2.36011 7.95093 2.78735 7.95093H6.37622V11.5398C6.37622 11.9731 6.73022 12.3271 7.16357 12.3271C7.59692 12.3271 7.95093 11.9731 7.95093 11.5398V7.95093H11.5398C11.9731 7.95093 12.3271 7.59692 12.3271 7.16357C12.3271 6.73022 11.9731 6.37622 11.5398 6.37622H7.95093V2.78735C7.95093 2.36011 7.59692 2 7.16357 2C6.73022 2 6.37622 2.36011 6.37622 2.78735V6.37622H2.78735C2.36011 6.37622 2 6.73022 2 7.16357Z"></path></svg></div></div></div></div>'

        # children_html += f"<div class='listbutton'>{'&nbsp;&nbsp;&nbsp;' * num}<div style='display: inline' onclick='toggleChildren({child.id})'>▷ </div><a href='/notion/{child.url}' style='color:#37352FCC;' class='text-decoration-none' onclick='toggleChildren({child.id})'><span id='{child.id}'  >{title or '제목없음'}</span></a><a href='/notion/remove/{ child.id }' id='removeId' class='text-decoration-none'><div style='margin-right:15px;float:right;'><svg role='graphics-symbol' viewBox='0 0 16 16' class='trash' style='width: 16px; height: 16px; display: block; fill: rgba(55, 53, 47, 0.85); flex-shrink: 0;'><path d='M4.8623 15.4287H11.1445C12.1904 15.4287 12.8672 14.793 12.915 13.7402L13.3799 3.88965H14.1318C14.4736 3.88965 14.7402 3.62988 14.7402 3.28809C14.7402 2.95312 14.4736 2.69336 14.1318 2.69336H11.0898V1.66797C11.0898 0.62207 10.4268 0 9.29199 0H6.69434C5.56641 0 4.89648 0.62207 4.89648 1.66797V2.69336H1.86133C1.5332 2.69336 1.25977 2.95312 1.25977 3.28809C1.25977 3.62988 1.5332 3.88965 1.86133 3.88965H2.62012L3.08496 13.7471C3.13281 14.7998 3.80273 15.4287 4.8623 15.4287ZM6.1543 1.72949C6.1543 1.37402 6.40039 1.14844 6.7832 1.14844H9.20312C9.58594 1.14844 9.83203 1.37402 9.83203 1.72949V2.69336H6.1543V1.72949ZM4.99219 14.2188C4.61621 14.2188 4.34277 13.9453 4.32227 13.542L3.86426 3.88965H12.1152L11.6709 13.542C11.6572 13.9453 11.3838 14.2188 10.9941 14.2188H4.99219ZM5.9834 13.1182C6.27051 13.1182 6.45508 12.9336 6.44824 12.667L6.24316 5.50293C6.23633 5.22949 6.04492 5.05176 5.77148 5.05176C5.48438 5.05176 5.2998 5.23633 5.30664 5.50293L5.51172 12.667C5.51855 12.9404 5.70996 13.1182 5.9834 13.1182ZM8 13.1182C8.28711 13.1182 8.47852 12.9336 8.47852 12.667V5.50293C8.47852 5.23633 8.28711 5.05176 8 5.05176C7.71289 5.05176 7.52148 5.23633 7.52148 5.50293V12.667C7.52148 12.9336 7.71289 13.1182 8 13.1182ZM10.0166 13.1182C10.29 13.1182 10.4746 12.9404 10.4814 12.667L10.6934 5.50293C10.7002 5.23633 10.5088 5.05176 10.2285 5.05176C9.95508 5.05176 9.76367 5.22949 9.75684 5.50293L9.54492 12.667C9.53809 12.9336 9.72949 13.1182 10.0166 13.1182Z'></path></svg></div></a>"
        if child.children.exists():
            children_html += f"<div class='childarea' id='children-{child.id}' style='display: none;'>{get_children_html(child, num+1)}</div>"
    return children_html

def get_children_html_active(notion, num):
    print('get_children_html_active')
    children_html = ""
    for child in notion.children.all():
        title = '';
        if child.title != '':
            title = child.title[:10]
            if len(title) == 10:
                title = title + '...'
        print('title:', title)
        children_html += f'<div onclick="location.href=`/notion/{child.url}`;" role="button" tabindex="0" class="showPage" aria-controls="addPage" aria-expanded="false" style="user-select: none; transition: background 20ms ease-in 0s; display: flex; align-items: center; border-radius: 6px; height: 30px;"><div onclick="event.stopPropagation();toggleChildren(this,{child.id})" style="margin-left:{12*num}px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; flex-grow: 0; width: 22px; height: 18px; margin-right: 8px; position: relative;"><div style="display: grid;"><div style="grid-area: 1 / 1; z-index: 1; order: 0; opacity: 0; transition: opacity 150ms ease 0s;"><div role="button" class="alterBtn" tabindex="0" aria-describedby=":rn:" aria-expanded="false" aria-label="열기" style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; position: relative; display: flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 4px; z-index=3;"><svg role="graphics-symbol" viewBox="0 0 12 12" class="chevronDownRoundedThick" style="width: 12px; height: 12px; display: block; fill: rgba(55, 53, 47, 0.35); flex-shrink: 0; rotate:0deg; transition: rotate 200ms ease-out 0s; opacity: 1;"><path d="M6.02734 8.80274C6.27148 8.80274 6.47168 8.71484 6.66211 8.51465L10.2803 4.82324C10.4268 4.67676 10.5 4.49609 10.5 4.28125C10.5 3.85156 10.1484 3.5 9.72363 3.5C9.50879 3.5 9.30859 3.58789 9.15234 3.74902L6.03223 6.9668L2.90722 3.74902C2.74609 3.58789 2.55078 3.5 2.33105 3.5C1.90137 3.5 1.55469 3.85156 1.55469 4.28125C1.55469 4.49609 1.62793 4.67676 1.77441 4.82324L5.39258 8.51465C5.58789 8.71973 5.78808 8.80274 6.02734 8.80274Z"></path></svg></div></div><div style="grid-area: 1 / 1; opacity: 1; transition: opacity 150ms ease 0s; order: 1;"><div class="notion-record-icon notranslate" style="display: flex; align-items: center; justify-content: center; height: 20px; width: 20px; border-radius: 0.25em; flex-shrink: 0;"><span role="img" aria-label="페이지 아이콘 변경"><svg role="graphics-symbol" viewBox="0 0 16 16" style="width: 18px; height: 18px; display: block; fill: rgb(145, 145, 142); flex-shrink: 0;"><path d="M4.35645 15.4678H11.6367C13.0996 15.4678 13.8584 14.6953 13.8584 13.2256V7.02539C13.8584 6.0752 13.7354 5.6377 13.1406 5.03613L9.55176 1.38574C8.97754 0.804688 8.50586 0.667969 7.65137 0.667969H4.35645C2.89355 0.667969 2.13477 1.44043 2.13477 2.91016V13.2256C2.13477 14.7021 2.89355 15.4678 4.35645 15.4678ZM4.46582 14.1279C3.80273 14.1279 3.47461 13.7793 3.47461 13.1436V2.99219C3.47461 2.36328 3.80273 2.00781 4.46582 2.00781H7.37793V5.75391C7.37793 6.73145 7.86328 7.20312 8.83398 7.20312H12.5186V13.1436C12.5186 13.7793 12.1836 14.1279 11.5205 14.1279H4.46582ZM8.95703 6.02734C8.67676 6.02734 8.56055 5.9043 8.56055 5.62402V2.19238L12.334 6.02734H8.95703ZM10.4336 9.00098H5.42969C5.16992 9.00098 4.98535 9.19238 4.98535 9.43164C4.98535 9.67773 5.16992 9.86914 5.42969 9.86914H10.4336C10.6797 9.86914 10.8643 9.67773 10.8643 9.43164C10.8643 9.19238 10.6797 9.00098 10.4336 9.00098ZM10.4336 11.2979H5.42969C5.16992 11.2979 4.98535 11.4893 4.98535 11.7354C4.98535 11.9746 5.16992 12.1592 5.42969 12.1592H10.4336C10.6797 12.1592 10.8643 11.9746 10.8643 11.7354C10.8643 11.4893 10.6797 11.2979 10.4336 11.2979Z"></path></svg></span></div></div></div></div><div style="padding: 5px 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"><span id="titleSpan_{child.id}" style="text-transform: initial; font-size: 14px; line-height: 1; color: rgb(145, 145, 142); font-weight: 500; transition: color 100ms ease-out 0s;">{title or '제목없음'}</span></div><div style="margin-left: auto;"><div class="addpage" style="display: flex; align-items: center; pointer-events: pointer; opacity: 0; transition: opacity 150ms ease 0s;"><div onclick="event.stopPropagation();location.href=`/notion/createChild/{child.id}/{child.url}/`" role="button" tabindex="0" class="addpage shadow-cursor-new-page-sidebar" aria-label="페이지 추가" style="user-select: none; transition: background 20ms ease-in 0s; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 1; height: 20px; width: 20px; border-radius: 4px; margin-right: 6px;"><span></span><svg role="graphics-symbol" viewBox="0 0 14 14" class="plusThick" style="width: 14px; height: 14px; display: block; fill: rgba(55, 53, 47, 0.45); flex-shrink: 0;"><path d="M2 7.16357C2 7.59692 2.36011 7.95093 2.78735 7.95093H6.37622V11.5398C6.37622 11.9731 6.73022 12.3271 7.16357 12.3271C7.59692 12.3271 7.95093 11.9731 7.95093 11.5398V7.95093H11.5398C11.9731 7.95093 12.3271 7.59692 12.3271 7.16357C12.3271 6.73022 11.9731 6.37622 11.5398 6.37622H7.95093V2.78735C7.95093 2.36011 7.59692 2 7.16357 2C6.73022 2 6.37622 2.36011 6.37622 2.78735V6.37622H2.78735C2.36011 6.37622 2 6.73022 2 7.16357Z"></path></svg></div></div></div></div>'


        # children_html += f"<div class='listbutton'>{'&nbsp;&nbsp;&nbsp;' * num}<div style='display: inline' onclick='toggleChildren({child.id})'>▷ </div><a href='/notion/{child.url}' style='color:#37352FCC;' class='text-decoration-none' onclick='toggleChildren({child.id})'><span id='{child.id}'  >{title or '제목없음'}</span></a><a href='/notion/remove/{ child.id }' id='removeId' class='text-decoration-none'><div style='margin-right:15px;float:right;'><svg role='graphics-symbol' viewBox='0 0 16 16' class='trash' style='width: 16px; height: 16px; display: block; fill: rgba(55, 53, 47, 0.85); flex-shrink: 0;'><path d='M4.8623 15.4287H11.1445C12.1904 15.4287 12.8672 14.793 12.915 13.7402L13.3799 3.88965H14.1318C14.4736 3.88965 14.7402 3.62988 14.7402 3.28809C14.7402 2.95312 14.4736 2.69336 14.1318 2.69336H11.0898V1.66797C11.0898 0.62207 10.4268 0 9.29199 0H6.69434C5.56641 0 4.89648 0.62207 4.89648 1.66797V2.69336H1.86133C1.5332 2.69336 1.25977 2.95312 1.25977 3.28809C1.25977 3.62988 1.5332 3.88965 1.86133 3.88965H2.62012L3.08496 13.7471C3.13281 14.7998 3.80273 15.4287 4.8623 15.4287ZM6.1543 1.72949C6.1543 1.37402 6.40039 1.14844 6.7832 1.14844H9.20312C9.58594 1.14844 9.83203 1.37402 9.83203 1.72949V2.69336H6.1543V1.72949ZM4.99219 14.2188C4.61621 14.2188 4.34277 13.9453 4.32227 13.542L3.86426 3.88965H12.1152L11.6709 13.542C11.6572 13.9453 11.3838 14.2188 10.9941 14.2188H4.99219ZM5.9834 13.1182C6.27051 13.1182 6.45508 12.9336 6.44824 12.667L6.24316 5.50293C6.23633 5.22949 6.04492 5.05176 5.77148 5.05176C5.48438 5.05176 5.2998 5.23633 5.30664 5.50293L5.51172 12.667C5.51855 12.9404 5.70996 13.1182 5.9834 13.1182ZM8 13.1182C8.28711 13.1182 8.47852 12.9336 8.47852 12.667V5.50293C8.47852 5.23633 8.28711 5.05176 8 5.05176C7.71289 5.05176 7.52148 5.23633 7.52148 5.50293V12.667C7.52148 12.9336 7.71289 13.1182 8 13.1182ZM10.0166 13.1182C10.29 13.1182 10.4746 12.9404 10.4814 12.667L10.6934 5.50293C10.7002 5.23633 10.5088 5.05176 10.2285 5.05176C9.95508 5.05176 9.76367 5.22949 9.75684 5.50293L9.54492 12.667C9.53809 12.9336 9.72949 13.1182 10.0166 13.1182Z'></path></svg></div></a>"
        if child.children.exists():
            children_html += f"<div class='childarea' id='children-{child.id}'>{get_children_html_active(child, num+1)}</div>"
    return children_html



def parent_find(notion):
    # 부모가 없으면 현재 노션이 최상위 부모임
    if notion.parent is None:
        return notion
    # 부모가 있으면 부모를 찾아서 계속 재귀 호출
    return parent_find(notion.parent)

def parentList(list, notion):
    if notion.parent is None:
        return list
    # 부모가 있으면 부모를 찾아서 계속 재귀 호출
    else:
        list.append(notion.parent)
        return parentList(list, notion.parent)


def pageNum(request, pageNum):
    if request.user.is_active:
        # 현재 사용자와 관련된 모든 Notion 객체 가져오기
        notions = Notion.objects.filter(user=request.user)
        # 현재 페이지와 관련된 Notion 객체 가져오기
        now = get_object_or_404(Notion, url=pageNum)
        
        parent = parent_find(now)
        parents = []
        parents = parentList(parents, now)

        border_list = '<div style=" color: rgba(55, 53, 47, 0.8); font-size:14px; font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol";">'
        for notion in notions:
            if notion.parent == None:
                border_list += borderListFunction(notion, parent)
        border_list += "</div>"
        username = request.user.username
        username_ = ''
        if len(username) > 5:
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
            'parents':parents,
            'reparents':reversed(parents),
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
    if notion.title == "":
        notion.title = '제목없음'
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


