# from rest_framework_jwt.utils import jwt_response_payload_handler
from django.contrib.auth.backends import ModelBackend
import re

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class UsernameMoblieModelBackend(ModelBackend):
    # 重写登陆校验方法
    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            if re.match(r'1[345789]\d{9}', username):
                user = User.objects.get(mobile=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None and user.check_password(password):
            return user

