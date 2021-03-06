from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    # /users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.RegisterUsernameView.as_view(), name='username'),
    url(r'^$', views.RegisterCreateUserView.as_view(), name='user'),
    url(r'auths/', obtain_jwt_token, name='auths'),
    url(r'^infos/$', views.UserCenterView.as_view()),
    url(r'^emails/$', views.EmailView.as_view()),
    url(r'^emails/verification/$', views.UserEmailActiveView.as_view()),

]
