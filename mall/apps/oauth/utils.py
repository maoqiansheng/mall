from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
from mall import settings


def generate_save_token(openid):

    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    data = {'openid': openid}
    token = serializer.dumps(data)
    return token.decode()


def check_save_token(token):
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    try:
        result = serializer.loads(token)
    except BadSignature:
        return None
    else:
        return result.get('openid')
