from rest_framework.validators import UniqueValidator

import re
from datetime import datetime, timedelta
from Zhicheng.settings import REGEX_MOBILE
from .models import VerifyCodede
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
import pdb
from rest_framework.authtoken import models

User = get_user_model()

class AuthtokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Token
        fields = "__all__"

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码(函数名称必须为validate_ + 字段名)
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 添加时间大于一分钟以前。也就是距离现在还不足一分钟
        if VerifyCodede.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """

    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
    '''
    identifying将密码设置为密文 write_only将返回到前端设置为false，这样前端就会将密码隐藏,将不会与前端字段进行对比，
    使用的models是user，而不是verifycode,如果不设置write_only，则会将identifying拿到user中进行序列化查找，找不到后将会报错
    '''
    identifying = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 },
                                 help_text="四位数字验证码,必填！")
    username = serializers.CharField(label="用户名", help_text="用户名，必填！", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    mobile = serializers.CharField(label="手机号码", help_text="手机号码，必填！", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="该手机号已被注册")])

    #将密码设置为密文 write_only将返回到前端设置为false，这样前端就会将密码隐藏,将不会与前端字段进行对比，使用的models是user，而不是
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    city = serializers.CharField(required=True,label='所在城市',help_text='必填信息',error_messages={
        'blank':'请输入城市',
        'required':'请输入城市',
    })

    # 调用父类的create方法，该方法会返回当前model的实例化对象即user。
    # 将密码加密保存到数据库
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_identifying(self, identifying):

        # 验证码在数据库中是否存在，用户从前端post过来的值都会放入initial_data里面，排序(最新一条)。
        verify_records = VerifyCodede.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            # 获取到最新一条
            last_record = verify_records[0]

            # 有效期为30分钟。
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=30, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.identifying != identifying:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    # 不加字段名的验证器作用于所有字段之上。attrs是字段 validate之后返回的总的dict,验证完identifying后将数据库中的identifying删除掉
    def validate(self, attrs):
        attrs["mobile"] = attrs["mobile"]
        del attrs["identifying"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "identifying", "mobile", "password",'city')