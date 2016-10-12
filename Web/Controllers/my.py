#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from Repertory.models import UserProfile,Weibo
from Infrastructure import myredis
def my(request):
    if request.method=='POST':
        pass
    redis = myredis.Redis()
    id=request.GET.get('user')
    if not id:id=request.session.get('user_id')
    ret = Weibo.objects.filter(user__id=id).values('id', 'user__name', 'user__head_img', 'pictures_link_id')
    print(id)
    user = UserProfile.objects.get(id=id)
    wb_list=[]
    fans_list = user.my_followers.select_related()
 #### 看自己是否是别人的Fenix
    for w in ret[::-1]:
        wb = redis.get_wb(w['id'])
        if wb:
            wb['user__head_img'] = w['user__head_img']
            wb['user__name'] = w['user__name']
            wb['pictures_link_id'] = w['pictures_link_id']
            wb_list.append(wb)
    return render(request,'my.html',locals())

def guan(request):
    if request.method == 'POST':
        id=request.session.get('user_id')
        to_id=request.POST.get('user_id')
        print('id',id,  'to_id',to_id)
        user=UserProfile.objects.get(id=id)
        to_user=UserProfile.objects.get(id=to_id)
        user.my_followers.add(to_user)
        print('ok')
        return HttpResponse('ok')