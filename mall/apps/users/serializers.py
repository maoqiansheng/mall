import re

from rest_framework import serializers
from .models import User
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings


class RegisterCreateUserSerializer(serializers.ModelSerializer):
    """
    需要校验6个参数， mobile, username, password, password2, sms_code, allow（是否同意协议）
    """
    # write_only 只在反序列化输入的时候起作用
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, write_only=True)
    allow = serializers.CharField(label='是否同意协议', write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段
    # ModelSerializer自动生成字段的时候是根据fileds来生成

    def create(self, validated_data):

        # 删除多余字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = super().create(validated_data)
        # 修改密码
        user.set_password(validated_data['password'])
        user.save()
        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user

    class Meta:
        model = User
        fields = ['id', 'mobile', 'password', 'username', 'password2', 'sms_code', 'allow', 'token']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        if not re.match('1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号规则不正确')
        return value

    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError('你没有同意协议')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        sms_code = attrs.get('sms_code')
        mobile = attrs.get('mobile')
        if password2 != password:
            raise serializers.ValidationError('密码不一致')
        redis_conn = get_redis_connection('code')
        redis_text = redis_conn.get('sms_%s' % mobile)
        if not redis_text:
            raise serializers.ValidationError('手机验证码已经过期')
        if redis_text.decode() != sms_code:
            raise serializers.ValidationError('图片验证码不一致')
        return attrs


class UserCenterInfoSerializer(serializers.ModelSerializer):
    """
        用户详细信息序列化器
        """

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class EmailSerializer(serializers.ModelSerializer):
    """
    邮箱序列化器
    """

    class Meta:
        model = User
        fields = ('id', 'email',)
        extra_kwargs = {
            'email':{
                'required':True
            }
        }

    def update(self, instance, validated_data):

        email = validated_data['email']
        instance.email = validated_data['email']
        instance.save()
        return instance
