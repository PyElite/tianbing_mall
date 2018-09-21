from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers


# CreateAPIView继承了CreateModelMixin和GenericAPIView,其提供了post方法增加创建
from users.models import User


class UserView(CreateAPIView):
    """
    用户注册:url(r"^users/$", views.UserView.as_view())
    """
    serializer_class = serializers.CreateUserSerializer


# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """
    用户名是否唯一处理:仅仅是对当前用户名进行数据库过滤查询,再将count返回,无其他逻辑,因此只需集成APIView
    """
    # url路径传参需要函数接收;url查询字符串用request.query_params接收;request.data中则是对post,put,patch解析之后的(文件和非文件)数据
    def get(self, request, username):
        """
        将前端请求的用户名总数数据返回
        """
        count = User.objects.filter(username=username).count()
        data = {
            "username": username,
            "count": count
        }
        # GET：返回资源对象的列表（数组）
        # POST：返回新生成的资源对象
        # PUT：返回完整的资源对象
        # PATCH：返回完整的资源对象
        # DELETE：返回一个空文档
        return Response(data)


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    电话是否唯一处理:相当与判断当前手机号是否已经注册
    """
    def get(self, request, mobile):

        count = User.objects.filter(mobile=mobile).count()
        data = {
            "mobile": mobile,
            "count": count
        }
        return Response(data)



















