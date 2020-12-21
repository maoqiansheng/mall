from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from users.models import User

"""
用户名接口逻辑分析：
前端：
  当前端光标离开用户名框的时候，前端会发送一个ajax请求，这个请求会携带用户输入的用户名

后端：
  # 1、接受参数
  # 2、判断用户名是否已经存在
  # 3、返回响应
  
请求方式：GET
url（遵循restful风格）：/users/usernames/(?P<username>\w{5,20})/count/
    
"""
# 需要分析用哪一个视图
# APIView
# Generic APIView
# ListAPIView, RetireveAPIView


class RegisterUsernameView(APIView):
    def get(self, request, username):
        # 1、接受参数
        # 2、判断用户名是否已经存在
        # 根据查询的结果判断用户是否存在
        count = User.objects.filter(username=username).count()
        # 3、返回响应
        return Response({"count": count, "username": username})
