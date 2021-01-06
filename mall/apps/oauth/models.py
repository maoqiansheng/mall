from django.db import models

from django.db import models
from utils.models import BaseModel
# Create your models here.


class OAuthQQUser(BaseModel):
    """
    QQ登录用户数据
    """
    # 如果我们使用到了其他子应用的模型类，需要使用'子应用.模型类名'
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name
