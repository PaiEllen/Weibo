#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import json
import datetime
from Infrastructure.myjson import CJsonEncoder

class Rebbitmq:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.11.39'))
        self.channel = self.connection.channel()


    def create_wb(self,data):
        self.channel.queue_declare(queue = 'New_wb')
        time=datetime.datetime.now()
        data['date']=time
        jsondata=json.dumps(data, cls=CJsonEncoder)
        self.channel.basic_publish(exchange = '', routing_key='New_wb', body =jsondata)
        self.connection.close()
        return jsondata

if __name__ == '__main__':
    a=Rebbitmq()
    date=datetime.datetime.now()
    data={"text":"大叔大婶打死的撒按时","pictures_link_id":5,"user_id":"1",'date':date}
    a.create_wb(data)