from django.core.mail import send_mail

from users.utils import generate_verify_url
from celery_tasks.main import celery_app


@celery_app.task(name='send_verify_email')
def send_verify_email(user_id, email):

    subject = '美多商城邮箱验证'
    message = ''
    from_mail = '美多商城<18137803201@163.com>'
    verify_url = generate_verify_url(user_id, email)
    html_massage = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
    send_mail(subject=subject,
              message=message,
              from_email=from_mail,
              recipient_list=[email],
              html_message=html_massage)