from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
# Create your views here.
from mall import settings

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
            print(access_token)

            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
            print(openid)
        except Exception:
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
