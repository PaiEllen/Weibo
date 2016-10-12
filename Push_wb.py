#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sina.settings")
import django
django.setup()

import pika
import json
from Repertory.models import Weibo
from Infrastructure.myredis import Redis
from Repertory.models import UserProfile

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.11.43'))
channel = connection.channel()
channel.queue_declare(queue='New_wb')
redis=Redis()
def callback(ch, method, properties, body):
    print(body)
    body=json.loads(str(body,encoding='utf-8'))
    user=UserProfile.objects.filter(id=body["user_id"]).first()
    print('user',user)
    fans_list=user.my_followers.select_related()
    print(fans_list)
    img_list=body['img_list']
    del body['img_list']
    ret = Weibo(**body)
    ret.save()
    if img_list:
        ret.pictures_link_id =ret.id
        ret.save()
    new_imgs=[]
    for img in img_list:
        path=img.split('/')
        to_path_list=path[1:4]+[str(ret.id),img]
        if img_list.index(img)==0:
            os.mkdir('/'.join(to_path_list[0:-1]))
        to_path='/'.join(path[1:4]+[str(ret.id),path[-1]])
        print('.' + img, to_path)
        new_imgs.append('/'+to_path)
        os.rename('.' + img, to_path)
    body['img_list']=new_imgs
    redis.add_wb(ret.id, body)
    for fans in fans_list:
        id=fans.id
        is_login=redis.get_login(id)
        print('is_login',is_login)
        if is_login:
            user_cache = redis.get_user(id)
            user_cache['wb_list'].insert(0, body['wb_id'])
            user_cache['count'] += 1
            print(user_cache)
            redis.update_user(id, user_cache)

channel.basic_consume(callback, queue='New_wb', no_ack=True)
channel.start_consuming()