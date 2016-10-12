#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from Repertory import models

class Form1(forms.Form):
    username = forms.CharField(
        error_messages={'required': '用户名不能为空'}, )
    password = forms.CharField(max_length=8, min_length=4,error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误',})
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})


