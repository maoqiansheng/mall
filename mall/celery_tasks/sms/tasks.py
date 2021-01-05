from libs.yuntongxun.sms import CCP
from celery_tasks.main import celery_app


@celery_app.task
def send_sms_code(mobile, sms_code):
    # 发送短信
    ccp = CCP()
    ccp.send_template_sms(mobile, [sms_code, 5], 1)
    pass