#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from Services import Login
from django.contrib.auth.models import User


def login(request):
    """
    使用方法
    POST 提交username，password，email 注册用户
    GET  提交username，password  用户名密码验证，验证成功写入session
    OPTION 用户注销

    """
    # 用户把微博提交过了
    # 创建用户
    result = {"status": False, "message": {}}
    if request.method == "POST":
        caret_result = Login.creat_user(request,User,result)

        print(caret_result)
        return HttpResponse(caret_result)

    # 用户登录
    if request.method == "GET":
        login_result = Login.user_login(request,result)
        return HttpResponse(login_result)

def CHECK_CODE(request):

    if request.method == "GET":

        # 生成图片并且返回
        import io
        from Infrastructure import check_code
        mstream = io.BytesIO()
        # 创建图片，并写入验证码
        img, code = check_code.create_validate_code()
        # 将图片对象写入到mstream，
        img.save(mstream, "GIF")
        # 为每个用户保存其验证码
        request.session["CheckCode"] = code
        return HttpResponse(mstream.getvalue())