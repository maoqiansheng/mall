from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

# Create your views here.
from users.serializers import RegisterCreateUserSerializer, EmailSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCenterInfoSerializer
from .utils import generate_verify_url, check_active_token

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


# 注册接口

class RegisterCreateUserView(APIView):
    def post(self, request):
        # 接收参数
        data = request.data
        # 序列化校验
        serializer = RegisterCreateUserSerializer(data=data)
        # 序列化校验
        serializer.is_valid(raise_exception=True)
        # 保存到数据库
        serializer.save()

        return Response(serializer.data)


# 个人中心接口，只能登陆用户访问，前端通过在header中添加token
class UserCenterView(APIView):
    # 只能登陆用户访问
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 根据token获取用户对象
        user = request.user
        # 创建序列化器
        serializer = UserCenterInfoSerializer(user)
        return Response(serializer.data)


class EmailView(APIView):
    """
    保存邮箱
    PUT /users/emails/
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = request.data
        user = request.user
        email = data.get('email')
        serializer = EmailSerializer(instance=user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 发送邮件163授权码#RJUNSTDKWDMYWRLB
        # from django.core.mail import send_mail
        # subject = '美多商城邮箱验证'
        # message = ''
        # from_mail = '美多商城<18137803201@163.com>'
        # verify_url = generate_verify_url(user.id, email)
        # html_massage = '<p>尊敬的用户您好！</p>' \
        #                '<p>感谢您使用美多商城。</p>' \
        #                '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
        #                '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
        # send_mail(subject=subject,
        #           message=message,
        #           from_email=from_mail,
        #           recipient_list=[email],
        #           html_message=html_massage)

        # 使用celery_tasks异步发送邮件
        from celery_tasks.email.tasks import send_verify_email
        send_verify_email(user.id, email)
        return Response(serializer.data)


class UserEmailActiveView(APIView):
    """
    用户点击邮箱链接，激活邮箱，数据库tb_users中的email_active为1
    """
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_id = check_active_token(token)
        user = User.objects.get(id=user_id)
        user.email_active = True
        user.save()
        return Response({"msg": "ok"})



