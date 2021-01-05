"""
1、创建一个celery对象
2、任务
    任务中的包名必须是tasks.py, 因为我们的celery可以自动检测任务
    任务其实就是一个函数
    这个任务必须被celery的实例对象的task 装饰器装饰
3、broker
4、worker

"""
from celery import Celery
# 为celery使用django配置文件进行设置,需要放到celery对象创建前
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'


celery_app = Celery(main='celery_tasks')
celery_app.config_from_object('celery_tasks.config')
celery_app.autodiscover_tasks(['celery_tasks.sms'])

# worker 其实就是一条指令, 这条指令需要在我们的虚拟环境中执行

# celery -A celery_tasks.main worker -l info

