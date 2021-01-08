from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
from mall import settings
from users.models import User


def generate_verify_url(user_id, email):

    serializer = Serializer(settings.SECRET_KEY, 3600)

    data = {
        'id': user_id,
        'email': email
    }

    token = serializer.dumps(data).decode()
    verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
    return verify_url


def check_active_token(token):

    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        result = serializer.loads(token)
    except BadSignature:
        return None
    user_id = result.get('id')
    email = result.get('email')
    try:
        user = User.objects.get(id=user_id, email=email)
    except User.DoesNotExist:
        user = None
    else:
        return user.id
