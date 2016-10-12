#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Infrastructure.forms import Form1
import json
import time
from Repertory.models import UserProfile
import os
from Infrastructure.myredis import Redis
# 创建用户
redis = Redis()
def creat_user(request,User,user_result):

    # 验证参数是否法
    f = Form1(request.POST)
    # 传入参数合法
    if f.is_valid():
        set_user_information = f.cleaned_data
        # f.cleaned_data  获取到的数据格式{'username': 'sadfasdf', 'email': '123@123.com', 'password': '111'}
        # 判断用户是否已经注册过  通过用户名唯一
        try:
            # 用户存在
            # 不存在会报错
            user = User.objects.get(username=set_user_information["username"])
            user_result["message"]["username"]= "用户名已经注册"
            return json.dumps(user_result)
        except:
            # 用户不存在可以直接注册
            # 创建用户
            user = User.objects.create_user(username=set_user_information["username"],
                                            password=set_user_information["password"],
                                            email=set_user_information["email"],
                                            last_login=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            user.save()
            user=UserProfile.objects.create(user=user,name=set_user_information["username"],
                                       head_img='/static/head_img/default.gif')
            user.follow_list.add(user)
            user_result["status"]=True

            request.session['user_head'] = str(user.head_img)
            redis.add_login(user.id)
            request.session['user_id'] = user.id
            request.session['name'] = user.name
            request.session['is_login']=True
            print('ok')
            path=os.path.join('C:\\Users\\shenwenlong\\PycharmProjects\\sina\\static\\wb_pic',str(user.id),'temp')
            os.makedirs(path)
            return json.dumps(user_result)
    # 传入参数不合法
    else:
        for i in f.errors:
            user_result["message"][i] = f.errors[i][0]
        return json.dumps(user_result)

def user_login(request,result):
    from django.contrib import auth
    # 获取出入的值:
    try:
        # 获取用户名密码
        username = request.GET["user"]
        password = request.GET["pwd"]


        # 去数据库查找是否存在
        # 返回一个对象，里面包含了所有用户信息
        look_result = auth.authenticate(username=username, password=password)
        # 查找到了用户
        user=UserProfile.objects.get(user__username=username)
        if look_result:
            request.session['user_head'] = str(user.head_img)
            request.session['user_id'] = str(user.id)
            request.session['name'] = user.name
            request.session['is_login'] = True
            request.session["id"] = look_result.id
            result["status"] = True
            redis.add_login(user.id)
            print('ok')
            return json.dumps(result)
        else:
            result["message"]={"user":"用户名或密码错误"}
            return json.dumps(result)
            # 判断用户是否已经登陆
    except:
        result["message"] = {"code": "验证码不能为空"}
        return json.dumps(result)


