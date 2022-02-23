from random import choice
import pdb
from django.shortcuts import render
from rest_framework import viewsets,status,authentication
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,RetrieveModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


from .models import VerifyCodede
from .seralizers import SmsSerializer,UserRegSerializer,UserDetailSerializer,AuthtokenSerializer
from utils.yunpian import YunPian
from utils import permissions
from Zhicheng.settings import APIKEY

from django.contrib.auth import get_user_model

User = get_user_model()

class SmsCodeView(CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = SmsSerializer
    # queryset = VerifyCodede.objects.all()
    def generate_identifying(self):
        """
        生成四位数字的验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)#如果serializer没有值的话，那么直接抛出异常

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        identifying = self.generate_identifying()

        sms_status = yun_pian.send_sms(identifying=identifying, mobile=mobile)

        if sms_status["code"] != 0:#这里的code是云片网返回的code
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            identifying_record = VerifyCodede(identifying=identifying, mobile=mobile)
            identifying_record.save()#验证码保存到数据库
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

class RegisterViewSet(CreateModelMixin,viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.username if user.name else user.username


        # AuthtokenSerializer(key = jwt_encode_handler(payload))
        # AuthtokenSerializer.save()


        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)#re_dict返回到前端的登录数据

    # 重写该方法，不管传什么id，都只返回当前用户
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()




from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from rest_framework_jwt.settings import api_settings
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class LoginViewset(ObtainJSONWebToken):
    '''
    重写JWT中的post方法，为了向前端返回错误信息
    '''
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)#验证数据库中数据与前端post的数据是否一致

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')

            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response
        else:
            return Response({
                "error_msg": '用户名或密码错误',
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)