#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse
from Infrastructure.myjson import CJsonEncoder
from Infrastructure.myredis import Redis
from Infrastructure.myqueue import Rebbitmq
from Repertory.models import *
import json
redis=Redis()
def new(request):
    if request.method == "POST":
        result={'status':False,'wb_list':[]}
        user_id = request.POST.get('user_id', None)
        ret=redis.get_user(user_id)
        count=ret['count']
        if ret['count'] !=0:
            result['status']=True
            for i in ret['wb_list'][0:count]:
                wb=redis.get_wb(i)
                result['wb_list'].append(wb)
            ret['count']=0
            redis.update_user(user_id,ret)
        return HttpResponse(json.dumps(result))

def count(request):
    if request.method == "POST":
        user_id = request.session.get('user_id', None)
        ret = redis.get_user(user_id)
        return ret['count']

# def create(request):
#     if request.method == "POST":
#         wb_data=json.loads(request.session.get('wb_data'))
#         queue=Rebbitmq()
#         jsondata=queue.create_wb(wb_data)
#         return HttpResponse(jsondata)

def get_comment(request):
    wb_id = request.POST.get('wb_id')
    ret=Comment.objects.filter(comment_type=0,to_weibo_id=wb_id).values('p_comment__id','user__name',
                            'user__head_img','comment','date','id')
    ret=ret[:]
    return HttpResponse(json.dumps(ret,cls=CJsonEncoder))
