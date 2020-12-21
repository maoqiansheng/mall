from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants
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
        # 2、生成图片和图片验证码，把验证码保存到redis中
        text, image = captcha.generate_captcha()
        # redis的链接设置，是根据"code",来找到redis的2号苦的
        redis_conn = get_redis_connection("code")
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_EXPIRE_TIME, text)
        # 3、返回响应
        return HttpResponse(image, content_type='image/jpeg')

