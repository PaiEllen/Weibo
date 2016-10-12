#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc

class IWeiboRepertory(metaclass=abc):

    @abc.abstractmethod
    def add_weibo(self,userid,data):
        pass

    @abc.abstractmethod
    def get_weibo_by_userid(self,userid):
        pass

    @abc.abstractmethod
    def get_weibo_follow(self,userid):
        # 获取我关注人的微博，根据自己的id 首页使用
        pass

    @abc.abstractmethod
    def get_weibo_hot(self):
        # 获取热门微博
        pass

    @abc.abstractmethod
    def search_weibo(self,keyword):
        pass