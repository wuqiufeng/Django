# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect, HttpResponseRedirect

from models import *
from hashlib import sha1
from django.http import JsonResponse

# Create your views here.
def register(request):
    return render(request, 'df_user/register.html')

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    if upwd != upwd2:
        return redirect('/user/register/')

    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    user= UserInfo()
    user.uname = uname
    user.upasswd = upwd3
    user.uemail=uemail
    user.save()
    return redirect('/user/login/')

# 判断用户是否已经存在
def register_exist(requset):
    uname = requset.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})

# 登录界面
def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

# 登录处理
def login_handle(request):
    port = request.POST
    uname = port.get('username')
    upwd = port.get('pwd')
    remember=port.get('remember',0)
    #根据用户名查询对象
    users=UserInfo.objects.filter(uname=uname)
    #判断用户和密码
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upasswd:
            print 12345678
            red = HttpResponseRedirect('/user/info/')
            #记住用户名
            if remember != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            contest={'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html', contest)
    else:
        contest = {'title': '用户登录', 'error_name': 1, 'error_pwd':1, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', contest)


def info(request):
    return render(request, 'df_user/user_center_info.html')