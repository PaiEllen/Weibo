#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from Infrastructure.myqueue import Rebbitmq
from Infrastructure.myredis import Redis
from Repertory.models import *
import datetime
import json
import os
def index(request):
    return render(request,'index.html')

def home(request):
    if  not request.session.get('is_login',None):
        return redirect('/index/')

    session=request.session
    # wb_list=[{'text':'了答上来了，充值卡芯片冷冻食品【奥氮平骚婆是的','pics':['static/wb_pic/2/pic/1_xlm289348.jpg', 'static/wb_pic/2/pic/005M94J9jw1f825c28mchj30m80chdi7.jpg']}]
    return render(request,'logined_index.html',locals())


def  load_wb(request):
    redis=Redis()
    user_id=request.session.get('user_id')
    user_dict=redis.get_user(user_id)
    length=len(user_dict['wb_list'])
    print(user_dict)
    wb_list=[]
     # user_dict 存的是 用户所关注的 微博
    for wb_id in  user_dict['wb_list'][::-1]:
        user=UserProfile.objects.filter(weibo__id=wb_id).values('head_img','name').first()
        wb=redis.get_wb(wb_id)
        wb['user_head']=user['head_img']
        wb['name']=user['name']
        wb_list.append(wb)
        print('wb',wb)
    return HttpResponse(json.dumps(wb_list))

def add_comment(request):
    if request.method =='POST':

        comment_dict={'comment':None,'to_wb_id':None,'user_id':None,'comment_type':0,'date':datetime.datetime.now()}

        comment_dict['comment']=request.POST.get('comment',None)
        comment_dict['to_wb_id']=request.POST.get('wb_id',None)
        comment_dict['user_id']=request.session.get('user_id',None)
        if None not in comment_dict.keys():
            comment_dict['p_comment'] = request.session.get('user_id')
            Comment.objects.create(**comment_dict)

def upload_img(request):
    files = request.FILES.getlist('files')
    print('1',files)
    # files = request.FILES["files"]
    # print('2',files)
    print( request.FILES)
    img_list=[]
    for file in files:
        # file = request.FILES.getlist('file')
        user_id=request.session.get('user_id')
        # user_id=str(2)
        img_list.append('/static/wb_pic/%s/temp/%s'%(user_id,file.name))
        path=os.path.join('C:\\Users\\shenwenlong\\PycharmProjects\\sina\\static\\wb_pic',str(user_id),'temp',file.name)
        destination = open(path, 'wb+')
        print(path)
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    return HttpResponse(json.dumps(img_list))

def create_wb(request):
    if request.method == "POST":
        wb_data=json.loads(request.POST.get('data'))
        print(wb_data)
        user_id=request.session.get('user_id')
        wb_data['user_id']=user_id
        queue=Rebbitmq()
        jsondata=queue.create_wb(wb_data)
        print(jsondata)
        return HttpResponse(jsondata)

def upload_head(request):
    if request.method == "POST":
        import time
        file = request.FILES['head_file']
        user_id=request.session.get('user_id')
        path='/static/head_img/'+str(time.time())
        destination = open('.'+path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        print('path',path)
        UserProfile.objects.filter(id=user_id).update(head_img=path)
        request.session['user_head']=path
        return HttpResponse(path)