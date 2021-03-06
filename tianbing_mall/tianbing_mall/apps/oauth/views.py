from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from carts.utils import merge_cart_cookie_to_redis
from oauth.exceptions import OAuthQQAPIError
from oauth.models import OAuthQQUser
from oauth.serializers import OAuthQQUserSerializer
from oauth.utils import OAuthQQ


# 请求方式： GET /oauth/qq/authorization/?next=xxx
class QQAuthURLView(APIView):
    """
    获取qq登录url视图:用不到序列化器,只需继承APIView
    """
    def get(self, request):
        # 1.获取next参数
        next = request.query_params.get("next")

        # 2.拼接qq登录的网址
        # 从自定义类中获取qq认证页面的url
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_qq_login_url()

        # 3.返回login_url: https://graph.qq.com/oauth2.0/authorize?next=/  如:user_center_info.js
        return Response({"login_url": login_url})


class QQAuthUserView(CreateAPIView):
    """
    qq登录界面跳转后的用户视图:CreateAPIView实现了post方法
    """
    # 指定用于qq登录后跳转的绑定页面创建用户的序列化器
    serializer_class = OAuthQQUserSerializer

    def get(self, request):
        """
        接收:code,是qq返回的授权凭证code
        返回:access_token:用户第一次使用QQ登录时需要返回,包含openid,用于跳转到绑定身份界面
                            通过itsdangerous生成access_token
            token:用户不是第一次使用QQ登录时需要返回,通过JWTtoken
            username & user_id:用户不是第一次使用QQ登录时返回
        """
        # 取参
        code = request.query_params.get("code")
        # 校参
        if not code:
            return Response({"message": "缺少code"}, status=status.HTTP_400_BAD_REQUEST)
        # 实例化QQ认证辅助工具类:
        oauth_qq = OAuthQQ()
        try:
            # 通过code获取access_token
            access_token = oauth_qq.get_access_token(code)
            # 通过access_token获取openid
            openid = oauth_qq.get_openid(access_token)
        except OAuthQQAPIError:
            return Response({"message": "访问QQ接口获取access_token/openid异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 此时已经获取了openid;接下来从数据库读取qq用户openid数据
        try:
            oauth_qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果qq用户数据不存在,则通过openid生成假的access_token并返回
            # 方法内部使用isdangerous
            access_token = oauth_qq.generate_bind_user_access_token(openid)
            return Response({"access_token": access_token})
        else:
            # 尝试查询成功,表明用户已经绑定过身份,则签发jwt token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 通过三方表的外键获取当前用户对象
            user = oauth_qq_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            # 响应数据:登录注册都一样:
            #   以下数据将在Response中放在第一个参数data中,前端通过request.data获取数据
            # return Response({
            #     "username": user.username,
            #     "user_id": user.id,
            #     "token": token
            # })
            # 已绑定用户:返回response前,调用合并购物车数据的公共方法,并接受返回值作为response
            response = Response({
                "username": user.username,
                "user_id": user.id,
                "token": token
            })
            response = merge_cart_cookie_to_redis(request, user, response)

            return response

    #
    def post(self, request, *args, **kwargs):
        """
        qq登录跳转后:未绑定用户:创建新用户
        """

        response = super().post(request, *args, **kwargs)

        # 当调用上面父类的方法后,获取user:
        #   1,如果是自定义的序列化器,可以在序列化器内给context字典中给view添加user属性,在视图函数内user=self.user
        #   2,如果不是自定义的序列化器,则从序列化器校验后的数据中取出user

        user = self.user  # 采用第1种,去改写自定义的序列化器,返回前:赋值self.context["view"].user=user

        # 调用合并购物车数据的公共方法,接收返回值作为response
        response = merge_cart_cookie_to_redis(request, user, response)

        return response


















