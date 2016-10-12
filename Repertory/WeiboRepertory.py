#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Services.Weiboservice import IWeiboRepertory
from Repertory.models import Weibo
from Repertory.models import Comment
from django.db.models import Count

class Weibom(IWeiboRepertory):

    def add_weibo(self,userid,data):
        Weibo.objects.create(**data)

    def get_weibo_by_userid(self,userid):
        # 访问自己主页时
        ret=Weibo.objects.filter(user__id=userid).values('wb_type','forward_or_collect_from','user__name','user__head_img',
                                                         'text','pictures_link_id','perm','date')
        return ret

    def get_weibo_follow(self,userid):
        # 获取我关注人的微博，根据自己的id 首页使用
        pass

    def get_weibo_hot(self):
        # 获取热门微博
        ret=Comment.objects.filter(comment_type=1).values('to_weibo__id').annotate(Count('id'))
        weiboid_list=list(map(lambda x:x['to_weibo__id'],ret))
        ret=Weibo.objects.filter(id__in=weiboid_list)
        return ret

    def search_weibo(self,keyword):
        ret=Weibo.objects.filter(text__contains=keyword)
        return ret
