#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
import os
register = template.Library()

@register.simple_tag
def wbimg(wb_id):
    path=os.path.join('/static/wb_pic', str(wb_id), 'pic')
    aa = path.split('\\')
    b = '/'.join(aa[-4:])
    pics=os.listdir(path)
    return map(lambda x:b+x,pics)

def wbimg_count(wb_id):
    path=os.path.join('/static/wb_pic', str(wb_id), 'pic')

    pics=os.listdir(path)
    return len(pics)