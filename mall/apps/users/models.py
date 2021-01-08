from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
"""
1、自己去定义模型
2、我们发现django自带了用户模型类，只是没有个别字段，例如手机号
"""


class User(AbstractUser):
    # 在继承AbstractUser的基础上额外扩展一些属性mobile
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name