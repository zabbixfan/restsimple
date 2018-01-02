#!/usr/bin/env python
#coding:utf-8
# from rest1.serializers import Data, DataSerializer
# from rest_framework.renderers import JSONRenderer  # 用于 JSON 渲染及解析
# from rest_framework.parsers import JSONParser
# from django.utils.six import BytesIO
#
# instance = Data(content="test")
# instance.save()
#
# serializer = DataSerializer(instance)
# print(JSONRenderer().render(serializer.data))  # b'{"id":1,"content":"test"}'
#
# raw = b'{"id":2,"content":"another"}'
# stream = BytesIO(raw)  # 将 JSON 数据变成 Python dict
# data = JSONParser().parse(stream)
#
# serializer = DataSerializer(data=data)
# ins = serializer.save()  # <Data: Data object>
# print(ins.__dict__)