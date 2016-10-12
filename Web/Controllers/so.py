#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from Repertory.models import Weibo
from Infrastructure import myredis

def wb(request):
    word=request.GET.get('word')
    if word:
        wb_list=[]
        redis=myredis.Redis()
        ret=Weibo.objects.filter(text__contains=word).values('id','user__name','user__head_img','pictures_link_id')
        for w in ret[::-1]:
            wb = redis.get_wb(w['id'])
            if wb:
                wb['user__head_img'] = w['user__head_img']
                wb['user__name'] = w['user__name']
                wb['pictures_link_id'] = w['pictures_link_id']
                wb_list.append(wb)
                print(wb)

    return render(request,'sou.html',locals())