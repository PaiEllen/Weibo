#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Services.Userservice import IUserRepertory
from Repertory.models import UserProfile
from Repertory.models import User


class Userm(IUserRepertory):
    def get_user_info(self,nid):
        # UserProfile.objects.filter(id=nid).values('name','brief','sex','age','email','head_img')
        ret=UserProfile.objects.filter(user__id=nid).first()
        # 通过get_sex_display获取到choice的值   c.sex_caption=c.get_sex_display()
        return ret

    def get_fans_follow_count(self,nid):
        user=UserProfile.objects.filter(id=nid).first()
        follow_count=user.follow_list.count()
        fans_count=user.my_followers.count()
        return {'follow_count':follow_count,'fans_count':fans_count}

    def register(self,username,password,email):
        User.objects.create(username=username,password=password,email=email)

    def existence(self,username):
        ret = User.objects.filter(username=username).first()
        return ret

    def search_user(self,keyword):
        pass