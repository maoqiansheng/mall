from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants
from rest_framework.response import Response
from .serializers import RegisterSmscodeSerializer
from random import randint
from rest_framework import status
from libs.yuntongxun.sms import CCP

# Create your views here.
"""
前端需要生成一个UUID，传递给我们后端，我们后台生成图片，和包含图片验证码内容保存到redis中

1、接收参数
2、生成图片和图片验证码，把验证码保存到redis中
3、返回响应

GET /varifications/imagecodes/uuid/(?P<image_code_id>.+)/
"""


class RegisterImageCodeView(APIView):
    def get(self, request, image_code_id):
        # 1、接收参数
        # 2、captcha生成图片和图片验证码，把验证码保存到redis中
        text, image = captcha.generate_captcha()
        # redis的链接设置，是根据"code",来找到redis的2号库
        redis_conn = get_redis_connection("code")
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_EXPIRE_TIME, text)
        # 3、返回响应
        return HttpResponse(image, content_type='image/jpeg')


# 短信验证码,用序列化器进行校验
class RegisterSmscodeView(APIView):
    def get(self, request, mobile):
        # get的方式接收参数
        params = request.query_params
        # 使用序列化器进行参数校验
        serializer = RegisterSmscodeSerializer(data=params)
        # 执行校验
        serializer.is_valid(raise_exception=True)
        # redis
        redis_conn = get_redis_connection('code')
        # 判断该用户是否频繁获取
        if redis_conn.get('sms_flag_%s' % mobile):
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        # 生成短信验证码
        sms_code = '%06d' % randint(0, 999999)
        # redis增加记录
        redis_conn.setex('sms_%s' % mobile, 5 * 60, sms_code)
        redis_conn.setex('sms_flag_%s' % mobile, 60, 1)
        # 发送短信
        ccp = CCP()
        ccp.send_template_sms(mobile, [sms_code, 5], 1)
        # 返回响应
        return Response({'message': 'ok'})