#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc


class Userservice:
    def check_login(self):
        pass

    def register(self, username, password, email):
        pass

    def get_user_info(self, nid):
        pass

    def get_fans_follow_count(self, userid):
        pass


class IUserRepertory(metaclass=abc):

    # @abc.abstractmethod
    # def check_login(self):
    #     pass

    @abc.abstractmethod
    def register(self,username,password,email):
        pass

    @abc.abstractmethod
    def get_user_info(self,nid):
        pass

    @abc.abstractmethod
    def existence(self,username):
        pass

    @abc.abstractmethod
    def get_fans_follow_count(self,userid):
        pass

    @abc.abstractmethod
    def search_user(self,keyword):
        pass