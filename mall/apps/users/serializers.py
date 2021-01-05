import re

from rest_framework import serializers
from .models import User
from django_redis import get_redis_connection


class RegisterCreateUserSerializer(serializers.ModelSerializer):
    """
    需要校验6个参数， mobile, username, password, password2, sms_code, allow（是否同意协议）
    """
    password2 = serializers.CharField(label='确认密码')
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, required=True)
    allow = serializers.CharField(label='是否同意协议', required=True)

    # ModelSerializer自动生成字段的时候是根据fileds来生成
    def create(self, validated_data):

        # 删除多余字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = super().create(validated_data)

        return user

    class Meta:
        model = User
        fields = ['mobile', 'password', 'username']

    def validate_mobile(self, value):
        if not re.match('1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号规则不正确')
        return value

    def validate_allow(self, value):
        if value != True:
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
