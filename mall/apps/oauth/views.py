from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
# Create your views here.
from rest_framework_jwt.settings import api_settings

from mall import settings
from .models import OAuthQQUser
from .utils import generate_save_token
from .serializers import OauthQQUserSerializer
"""
用户点击QQ登陆的时候，前端发送一个ajax请求，后端把生成的url返回给前端

GET /oauth/qq/statues/
"""


class OauthQQURLView(APIView):
    """生成url"""
    """
        提供QQ登录页面网址

        """

    def get(self, request):
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        state = request.query_params.get('state')
        if not state:
            state = '/'

        # 获取QQ登录页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=state)
        login_url = oauth.get_qq_url()

        return Response({'login_url': login_url})


"""
    当用户扫描成功，腾讯服务器会生成一个code,前端需要将code返回给后端，
    后端接收code,生成token
    GET oauth/qq/users/?code=xxx

"""


class OauthQQUserView(APIView):
    def get(self, request):

        code = request.query_params.get('code')
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 通过code 获取token
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)
            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception:
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        # 获取到openid之后，我们需要查询下数据库，如果数据哭中有openid,s说明绑定过了
            # 使用openid查询该QQ用户是否在美多商城中绑定过用户
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果openid没绑定美多商城用户，创建用户并绑定到openid
            # 为了能够在后续的绑定用户操作中前端可以使用openid，在这里将openid签名后响应给前端
            access_token_openid = generate_save_token(openid)
            return Response({'access_token': access_token_openid})
        else:
            # 如果openid已绑定美多商城用户，直接生成JWT token，并返回
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 获取oauth_user关联的user
            user = oauth_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })

            return response

    def post(self, request):
        """
        QQ绑定用户
        """
        """openid绑定到用户"""

        # 获取序列化器对象
        serializer = OauthQQUserSerializer(data=request.data)
        # 开启校验
        serializer.is_valid(raise_exception=True)
        # 保存校验结果，并接收
        user = serializer.save()

        # 生成JWT token，并响应
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

        return response



